#!/usr/bin/env python3
"""Check URL eligibility against a local allowlist. No network or quality checks."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


LANES = {"science-candidate", "anecdote-candidate", "discovery-only", "blocked"}
DEFAULT_POLICY = Path(__file__).resolve().parents[1] / "references" / "source-policy.json"
HOST_RE = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}\Z")
PATH_RE = re.compile(r"/[A-Za-z0-9/_~.,:+@()=\-]*\Z")


def _valid_host(host):
    return (isinstance(host, str) and len(host) <= 253
            and HOST_RE.fullmatch(host) is not None
            and not any(part.startswith("xn--") for part in host.split(".")))


def _valid_path(path):
    return (isinstance(path, str) and PATH_RE.fullmatch(path) is not None
            and "//" not in path
            and not any(part in {".", ".."} for part in path.split("/")))


def _matches(path, prefix):
    return prefix == "/" or path == prefix or path.startswith(prefix.rstrip("/") + "/")


def validate_policy(policy):
    """Raise ValueError for malformed or conflicting policies; return no approvals."""
    if not isinstance(policy, dict) or set(policy) != {"version", "rules"}:
        raise ValueError("policy must contain exactly version and rules")
    if type(policy["version"]) is not int or policy["version"] != 1:
        raise ValueError("policy version must be integer 1")
    if not isinstance(policy["rules"], list):
        raise ValueError("policy rules must be a list")
    ids = set()
    entries = []
    for rule in policy["rules"]:
        if not isinstance(rule, dict) or set(rule) != {"id", "lane", "hosts", "path_prefixes"}:
            raise ValueError("each rule must contain exactly id, lane, hosts, and path_prefixes")
        rule_id = rule["id"]
        if not isinstance(rule_id, str) or re.fullmatch(r"[a-z0-9][a-z0-9-]*", rule_id) is None:
            raise ValueError("rule id must use lowercase letters, numbers, and hyphens")
        if rule_id in ids:
            raise ValueError("rule ids must be unique")
        ids.add(rule_id)
        if not isinstance(rule["lane"], str) or rule["lane"] not in LANES:
            raise ValueError("unknown policy lane")
        for key, validator in (("hosts", _valid_host), ("path_prefixes", _valid_path)):
            values = rule[key]
            if not isinstance(values, list) or not values or not all(validator(v) for v in values):
                raise ValueError("invalid or empty " + key)
            if len(values) != len(set(values)):
                raise ValueError("duplicate " + key)
        for host in rule["hosts"]:
            for prefix in rule["path_prefixes"]:
                for other_host, other_prefix, other_lane in entries:
                    if host != other_host:
                        continue
                    if prefix == other_prefix:
                        raise ValueError("duplicate host and path rule")
                    if rule["lane"] != other_lane and (_matches(prefix, other_prefix) or _matches(other_prefix, prefix)):
                        raise ValueError("overlapping paths have conflicting lanes")
                entries.append((host, prefix, rule["lane"]))


def evaluate_url(url, policy):
    """Return eligibility only. Callers must verify content, publication status, and redirects."""
    validate_policy(policy)
    result = {"url": url, "lane": "blocked", "rule": None, "reason": ""}

    def blocked(reason):
        result["reason"] = reason
        return result

    if not isinstance(url, str) or not url:
        return blocked("URL must be a nonempty string")
    if any(ord(char) <= 32 or ord(char) >= 127 for char in url) or "\\" in url:
        return blocked("URL contains whitespace, controls, non-ASCII text, or backslashes")
    if re.search(r"%(?![0-9A-Fa-f]{2})", url) or re.search(r"%(?:0[0-9a-f]|1[0-9a-f]|7f)", url, re.I):
        return blocked("URL contains malformed or control-character encoding")
    try:
        parts = urlsplit(url)
        host = parts.hostname
        port = parts.port
    except ValueError:
        return blocked("URL cannot be parsed safely")
    if parts.scheme.lower() != "https" or not parts.netloc:
        return blocked("Only absolute HTTPS URLs are eligible")
    if parts.username is not None or parts.password is not None:
        return blocked("Credentials in URLs are not eligible")
    if port not in (None, 443) or re.fullmatch(r"[A-Za-z0-9.-]+(?::443)?", parts.netloc) is None:
        return blocked("URL authority or port is not canonical")
    if not _valid_host(host):
        return blocked("Host must be a canonical ASCII DNS name without IDNA labels")
    path = parts.path or "/"
    if not _valid_path(path):
        return blocked("Path is not canonical; encoded paths and dot segments need manual resolution")
    matches = []
    for rule in policy["rules"]:
        if host in rule["hosts"]:
            matches.extend((len(prefix), rule) for prefix in rule["path_prefixes"] if _matches(path, prefix))
    if not matches:
        return blocked("No exact host and path rule matches this URL")
    rule = max(matches, key=lambda match: match[0])[1]
    result.update(lane=rule["lane"], rule=rule["id"], reason="Exact host and path match only; content and publication quality are unverified")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", metavar="URL")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    args = parser.parse_args(argv)
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"))
        validate_policy(policy)
    except (OSError, ValueError) as error:
        print("Invalid policy: " + str(error), file=sys.stderr)
        return 2
    results = [evaluate_url(url, policy) for url in args.urls]
    print(json.dumps(results, indent=2))
    return 0 if all(item["lane"] in {"science-candidate", "anecdote-candidate"} for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())
