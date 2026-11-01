"""Adversarial URL eligibility tests; no network or scientific-quality assertions."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "science-research" / "scripts" / "check_source.py"
SPEC = importlib.util.spec_from_file_location("check_source", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)

POLICY = {
    "version": 1,
    "rules": [
        {"id": "science", "lane": "science-candidate", "hosts": ["research.example.org"], "path_prefixes": ["/pubs"]},
        {"id": "forums", "lane": "anecdote-candidate", "hosts": ["forum.example.org"], "path_prefixes": ["/"]},
        {"id": "index", "lane": "discovery-only", "hosts": ["index.example.org"], "path_prefixes": ["/"]},
    ],
}


class SourcePolicyTests(unittest.TestCase):
    def lane(self, url):
        return CHECKER.evaluate_url(url, POLICY)["lane"]

    def test_exact_host_and_path_boundary(self):
        for url in ("https://research.example.org/pubs", "https://research.example.org/pubs/paper-1", "https://RESEARCH.EXAMPLE.ORG:443/pubs/paper.pdf#results"):
            with self.subTest(url=url):
                self.assertEqual(self.lane(url), "science-candidate")
        for url in ("https://research.example.org/pubstuff", "https://research.example.org/", "https://sub.research.example.org/pubs", "https://research.example.org.evil.org/pubs"):
            with self.subTest(url=url):
                self.assertEqual(self.lane(url), "blocked")

    def test_lanes_do_not_merge(self):
        self.assertEqual(self.lane("https://forum.example.org/thread/1"), "anecdote-candidate")
        self.assertEqual(self.lane("https://index.example.org/record/1"), "discovery-only")
        result = CHECKER.evaluate_url("https://research.example.org/pubs/paper", POLICY)
        self.assertEqual(result["rule"], "science")
        self.assertIsNone(CHECKER.evaluate_url("https://unknown.example.org/", POLICY)["rule"])

    def test_spoofing_and_ambiguous_authorities_are_blocked(self):
        urls = [
            "http://research.example.org/pubs", "//research.example.org/pubs", "/pubs",
            "https://research.example.org@evil.org/pubs", "https://user@research.example.org/pubs",
            "https://research.example.org:444/pubs", "https://research.example.org:0443/pubs",
            "https://research.example.org:/pubs", "https://research.example.org./pubs",
            "https://research%2eexample.org/pubs", "https://xn--research-9jg.example.org/pubs",
            "https://reseаrch.example.org/pubs", "https://127.0.0.1/pubs", "https://[::1]/pubs",
            "https://research.example.org\\@evil.org/pubs", " https://research.example.org/pubs",
            "https://research.example.org/pubs\n", "https://research.example.org/pubs\x00",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.lane(url), "blocked")

    def test_path_normalization_cannot_bypass_policy(self):
        urls = [
            "https://research.example.org/pubs/../private", "https://research.example.org/./pubs/paper",
            "https://research.example.org/pubs//paper", "https://research.example.org//pubs/paper",
            "https://research.example.org/pubs/%2e%2e/private", "https://research.example.org/%70ubs/paper",
            "https://research.example.org/pubs%2fpaper", "https://research.example.org/pubs/%252e%252e/private",
            "https://research.example.org/pubs;private", "https://research.example.org/pubs/paper?x=%0d%0aevil",
            "https://research.example.org/pubs/paper?x=%GG",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.lane(url), "blocked")

    def test_query_does_not_approve_a_redirect_target(self):
        url = "https://research.example.org/pubs/paper?next=https%3A%2F%2Fevil.org%2F"
        self.assertEqual(self.lane(url), "science-candidate")
        self.assertEqual(self.lane("https://evil.org/"), "blocked")
        self.assertEqual(self.lane("https://research.example.org/pubs/paper?q=study%20one"), "science-candidate")

    def test_invalid_policies_fail_closed(self):
        invalid = [None, {}, {"version": True, "rules": []}, {"version": 2, "rules": []}, {"version": 1, "rules": {}}, {"version": 1, "rules": [], "allow_all": True}]
        for key, value in (("id", "bad id"), ("lane", "approved"), ("hosts", ["*.example.org"]), ("hosts", ["EXAMPLE.ORG"]), ("hosts", ["xn--exmple-cua.org"]), ("hosts", []), ("hosts", ["example.org", "example.org"]), ("path_prefixes", ["/pubs/../private"]), ("path_prefixes", ["/pubs%2f"]), ("path_prefixes", ["pubs"]), ("path_prefixes", [])):
            policy = copy.deepcopy(POLICY)
            policy["rules"][0][key] = value
            invalid.append(policy)
        for policy in invalid:
            with self.subTest(policy=policy):
                with self.assertRaises(ValueError):
                    CHECKER.evaluate_url("https://research.example.org/pubs/paper", policy)

    def test_duplicate_and_conflicting_rules_fail_closed(self):
        for changed in ({"id": "science"}, {"id": "another"}, {"id": "conflict", "lane": "anecdote-candidate", "path_prefixes": ["/pubs/subset"]}):
            policy = copy.deepcopy(POLICY)
            rule = copy.deepcopy(policy["rules"][0])
            rule.update(changed)
            policy["rules"].append(rule)
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                CHECKER.validate_policy(policy)

    def test_empty_allowlist_approves_nothing(self):
        self.assertEqual(CHECKER.evaluate_url("https://research.example.org/pubs/paper", {"version": 1, "rules": []})["lane"], "blocked")

    def test_trailing_slash_prefix_and_specific_same_lane_rule(self):
        policy = copy.deepcopy(POLICY)
        policy["rules"][0]["path_prefixes"] = ["/pubs/"]
        self.assertEqual(CHECKER.evaluate_url("https://research.example.org/pubs/paper", policy)["lane"], "science-candidate")
        self.assertEqual(CHECKER.evaluate_url("https://research.example.org/pubs", policy)["lane"], "blocked")
        policy["rules"].append({"id": "specific", "lane": "science-candidate", "hosts": ["research.example.org"], "path_prefixes": ["/pubs/special"]})
        self.assertEqual(CHECKER.evaluate_url("https://research.example.org/pubs/special/paper", policy)["rule"], "specific")

    def test_cli_exit_status_and_json(self):
        with tempfile.TemporaryDirectory() as directory:
            policy_path = Path(directory) / "policy.json"
            policy_path.write_text(json.dumps(POLICY), encoding="utf-8")
            def run(*urls):
                return subprocess.run([sys.executable, str(SCRIPT), *urls, "--policy", str(policy_path)], capture_output=True, text=True)
            good = run("https://research.example.org/pubs/paper", "https://forum.example.org/thread/1")
            self.assertEqual(good.returncode, 0, good.stderr)
            self.assertEqual([item["lane"] for item in json.loads(good.stdout)], ["science-candidate", "anecdote-candidate"])
            for url in ("https://index.example.org/record", "https://evil.org/"):
                self.assertEqual(run(url).returncode, 1)
            self.assertEqual(run().returncode, 2)
            policy_path.write_text("{invalid", encoding="utf-8")
            self.assertEqual(run("https://research.example.org/pubs").returncode, 2)
            policy_path.write_text(json.dumps({"version": True, "rules": []}), encoding="utf-8")
            self.assertEqual(run("https://research.example.org/pubs").returncode, 2)


if __name__ == "__main__":
    unittest.main()
