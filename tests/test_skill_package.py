"""Check the shipped policy, portable artifact, and runtime references together."""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "science-research"
SPEC = importlib.util.spec_from_file_location("source_checker", SKILL / "scripts" / "check_source.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class SkillPackageTests(unittest.TestCase):
    def test_default_policy_preserves_source_lanes(self):
        policy = json.loads((SKILL / "references" / "source-policy.json").read_text())
        CHECKER.validate_policy(policy)
        cases = {
            "https://pubmed.ncbi.nlm.nih.gov/33865376/": "science-candidate",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC8053283/": "science-candidate",
            "https://www.epa.gov/indoor-air-quality-iaq/air-cleaners-and-air-filters-home": "science-candidate",
            "https://www.nice.org.uk/guidance/ng202": "science-candidate",
            "https://www.reddit.com/r/sleep/comments/example/": "anecdote-candidate",
            "https://connect.mayoclinic.org/discussion/example/": "anecdote-candidate",
            "https://news.ycombinator.com/item?id=123": "anecdote-candidate",
            "https://doi.org/10.1234/example": "discovery-only",
            "https://arxiv.org/abs/2601.00001": "discovery-only",
            "https://www.nature.com.evil.example/articles/example": "blocked",
            "https://www.nice.org.uk/guidance-store/example": "blocked",
            "https://unlisted-university.edu/paper": "blocked",
            "https://www.reddit.com.evil.example/r/sleep/": "blocked",
            "https://community.patient.info/t/example": "blocked",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                self.assertEqual(CHECKER.evaluate_url(url, policy)["lane"], expected)

    def test_entry_point_is_portable_and_complete(self):
        content = (SKILL / "SKILL.md").read_text()
        frontmatter = content.split("---", 2)[1]
        fields = dict(line.split(": ", 1) for line in frontmatter.strip().splitlines())
        self.assertEqual(fields["name"], SKILL.name)
        self.assertLessEqual(len(fields["description"]), 200)
        self.assertNotIn("[TODO:", content)
        self.assertNotIn("/Users/", content)

    def test_runtime_reference_links_resolve_within_skill(self):
        for source in SKILL.rglob("*.md"):
            links = re.findall(r"\]\(([^)]+)\)", source.read_text())
            for target in links:
                if "://" in target or target.startswith("#"):
                    continue
                path = (source.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(source=source, target=target):
                    self.assertTrue(path.is_relative_to(SKILL.resolve()))
                    self.assertTrue(path.is_file())

    def test_package_contains_current_runtime_and_is_reproducible(self):
        spec = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts" / "package_skill.py")
        packager = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(packager)
        with tempfile.TemporaryDirectory() as directory:
            first = packager.build_package(Path(directory) / "first.zip")
            second = packager.build_package(Path(directory) / "second.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with ZipFile(first) as archive:
                self.assertIsNone(archive.testzip())
                names = archive.namelist()
                self.assertIn("science-research/SKILL.md", names)
                self.assertIn("science-research/references/source-policy.json", names)
                self.assertIn("science-research/scripts/check_source.py", names)
                self.assertTrue(all(name.startswith("science-research/") for name in names))
                self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in names))
                for name in names:
                    self.assertEqual(archive.read(name), (ROOT / name).read_bytes())
                extracted = Path(directory) / "extracted"
                archive.extractall(extracted)
            check = subprocess.run([
                sys.executable, str(extracted / "science-research/scripts/check_source.py"),
                "https://www.reddit.com/r/science/comments/example/",
            ], capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertEqual(json.loads(check.stdout)[0]["lane"], "anecdote-candidate")


if __name__ == "__main__":
    unittest.main()
