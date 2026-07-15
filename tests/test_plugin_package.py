#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILL = ROOT / "skills" / "econ-write"
CLAUDE_MIRROR = ROOT / ".claude" / "skills" / "econ-write"
CODEX_MIRROR = ROOT / ".agents" / "skills" / "econ-write"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
NPX_SKILLS_VERSION = "1.5.17"
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def strict_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def frontmatter(path: Path) -> str:
    match = re.match(
        r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)",
        path.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if match is None:
        raise ValueError(f"missing YAML frontmatter: {path}")
    return match.group(1).replace("\r\n", "\n")


def skill_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def write_local_catalog(catalog: Path) -> Path:
    package = catalog / "plugins" / "econ-write"
    for relative in (
        Path(".claude-plugin"),
        Path(".codex-plugin"),
        Path(".claude/skills/econ-write"),
        Path(".agents/skills/econ-write"),
        Path("skills/econ-write"),
    ):
        shutil.copytree(ROOT / relative, package / relative)
    shutil.copy2(ROOT / "LICENSE", package / "LICENSE")

    catalog_manifest = {
        "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
        "name": "openeconai",
        "description": "OpenEconAI plugins for economics research and writing.",
        "owner": {"name": "OpenEconAI", "url": "https://openecon.ai"},
        "plugins": [
            {
                "name": "econ-write",
                "description": strict_json(CLAUDE_MANIFEST)["description"],
                "source": "./plugins/econ-write",
                "homepage": "https://openecon.ai",
            }
        ],
    }
    manifest = catalog / ".claude-plugin" / "marketplace.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(json.dumps(catalog_manifest, indent=2) + "\n", encoding="utf-8")
    return package


class PluginPackageTests(unittest.TestCase):
    def test_manifests_are_synchronized_and_release_ready(self) -> None:
        claude = strict_json(CLAUDE_MANIFEST)
        codex = strict_json(CODEX_MANIFEST)

        shared_fields = (
            "name",
            "version",
            "description",
            "author",
            "homepage",
            "repository",
            "license",
            "keywords",
            "skills",
        )
        for field in shared_fields:
            with self.subTest(field=field):
                self.assertEqual(claude[field], codex[field])

        self.assertEqual(claude["name"], "econ-write")
        self.assertEqual(claude["version"], "0.1.0")
        self.assertRegex(claude["version"], SEMVER)
        self.assertEqual(claude["license"], "MIT")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Permission is hereby granted, free of charge", license_text)
        self.assertEqual(claude["homepage"], "https://openecon.ai")
        self.assertEqual(
            claude["repository"], "https://github.com/hanlulong/econ-writing-skill"
        )
        self.assertEqual(claude["skills"], "./skills/")
        self.assertEqual(codex["interface"]["displayName"], "Econ Write")
        self.assertEqual(codex["interface"]["websiteURL"], "https://openecon.ai")
        self.assertTrue(
            all("econ-write" in prompt for prompt in codex["interface"]["defaultPrompt"])
        )

    def test_canonical_and_direct_skill_trees_are_byte_identical(self) -> None:
        canonical = skill_files(CANONICAL_SKILL)
        self.assertEqual(
            set(canonical),
            {
                "SKILL.md",
                "identification-strategies.md",
                "latex-tips.md",
                "review-checklist.md",
                "specialized-tasks.md",
            },
        )
        self.assertEqual(canonical, skill_files(CLAUDE_MIRROR))
        self.assertEqual(canonical, skill_files(CODEX_MIRROR))
        self.assertEqual(
            frontmatter(CANONICAL_SKILL / "SKILL.md"),
            frontmatter(CLAUDE_MIRROR / "SKILL.md"),
        )

    def test_plugin_layout_has_no_embedded_marketplace_or_unsafe_links(self) -> None:
        self.assertFalse((ROOT / ".claude-plugin" / "marketplace.json").exists())
        required = (
            CLAUDE_MANIFEST,
            CODEX_MANIFEST,
            CANONICAL_SKILL / "SKILL.md",
            CLAUDE_MIRROR / "SKILL.md",
            ROOT / "LICENSE",
        )
        for path in required:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertTrue(path.is_file())
                self.assertFalse(path.is_symlink())

        for base in (CANONICAL_SKILL, CLAUDE_MIRROR, CODEX_MIRROR):
            for path in base.rglob("*"):
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    self.assertFalse(path.is_symlink())

    def test_readme_documents_one_catalog_and_both_clients(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        required = (
            "/plugin marketplace add OpenEconAI/plugins",
            "/plugin install econ-write@openeconai",
            "claude plugin marketplace update openeconai",
            "claude plugin update econ-write@openeconai",
            "claude plugin uninstall econ-write@openeconai",
            "codex plugin marketplace add OpenEconAI/plugins",
            "codex plugin add econ-write@openeconai",
            "codex plugin marketplace upgrade openeconai",
            "codex plugin remove econ-write@openeconai",
        )
        for command in required:
            with self.subTest(command=command):
                self.assertIn(command, readme)
        self.assertIn("direct installer", readme.lower())
        self.assertIn("main/skills/econ-write/SKILL.md", readme)

        installer = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn('$REPO_URL/skills/econ-write/$file', installer)
        self.assertNotIn('$REPO_URL/.claude/skills/econ-write/$file', installer)

    @unittest.skipUnless(shutil.which("claude"), "Claude Code CLI is not installed")
    def test_claude_strict_validation_and_external_catalog_install(self) -> None:
        claude = shutil.which("claude")
        assert claude is not None
        validate = subprocess.run(
            [claude, "plugin", "validate", "--strict", str(ROOT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(validate.returncode, 0, validate.stdout + validate.stderr)

        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            catalog = temporary_root / "catalog"
            installed_package = write_local_catalog(catalog)
            home = temporary_root / "claude-home"
            env = {**os.environ, "CLAUDE_CONFIG_DIR": str(home)}
            for command in (
                [claude, "plugin", "marketplace", "add", str(catalog)],
                [claude, "plugin", "install", "econ-write@openeconai"],
                [claude, "plugin", "details", "econ-write@openeconai"],
            ):
                result = subprocess.run(
                    command,
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = (
                home
                / "plugins"
                / "cache"
                / "openeconai"
                / "econ-write"
                / strict_json(CLAUDE_MANIFEST)["version"]
            )
            self.assertTrue((installed / "skills/econ-write/SKILL.md").is_file())
            self.assertTrue((installed / ".claude/skills/econ-write/SKILL.md").is_file())
            self.assertEqual(
                skill_files(installed / "skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(installed / ".claude/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(installed / ".agents/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(installed_package / "skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            uninstall = subprocess.run(
                [claude, "plugin", "uninstall", "econ-write@openeconai"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                uninstall.returncode, 0, uninstall.stdout + uninstall.stderr
            )

    @unittest.skipUnless(shutil.which("codex"), "Codex CLI is not installed")
    def test_codex_external_catalog_install(self) -> None:
        codex = shutil.which("codex")
        assert codex is not None
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            catalog = temporary_root / "catalog"
            write_local_catalog(catalog)
            home = temporary_root / "codex-home"
            home.mkdir()
            env = {**os.environ, "CODEX_HOME": str(home)}
            add_catalog = subprocess.run(
                [codex, "plugin", "marketplace", "add", str(catalog), "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                add_catalog.returncode,
                0,
                add_catalog.stdout + add_catalog.stderr,
            )
            install = subprocess.run(
                [codex, "plugin", "add", "econ-write@openeconai", "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(install.returncode, 0, install.stdout + install.stderr)
            record = json.loads(install.stdout)
            installed = Path(record["installedPath"])
            self.assertEqual(installed.name, strict_json(CODEX_MANIFEST)["version"])
            self.assertTrue((installed / "skills/econ-write/SKILL.md").is_file())
            self.assertTrue((installed / ".claude/skills/econ-write/SKILL.md").is_file())
            self.assertEqual(
                skill_files(installed / "skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(installed / ".claude/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(installed / ".agents/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            remove = subprocess.run(
                [codex, "plugin", "remove", "econ-write@openeconai", "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(remove.returncode, 0, remove.stdout + remove.stderr)

    def test_direct_installer_still_installs_all_supported_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            env = {**os.environ, "HOME": temporary}
            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), "--global", "--all"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            home = Path(temporary)
            for installed in (
                home / ".claude/skills/econ-write",
                home / ".agents/skills/econ-write",
                home / ".codex/skills/econ-write",
            ):
                with self.subTest(path=installed.as_posix()):
                    self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))

    @unittest.skipUnless(
        os.environ.get("ECON_WRITE_RUN_NPX_SMOKE") == "1",
        "set ECON_WRITE_RUN_NPX_SMOKE=1 for the pinned network release smoke test",
    )
    @unittest.skipUnless(shutil.which("npx"), "npx is not installed")
    def test_pinned_npx_skills_release_install(self) -> None:
        npx = shutil.which("npx")
        assert npx is not None
        with tempfile.TemporaryDirectory() as temporary:
            env = {
                **os.environ,
                "HOME": temporary,
                "CODEX_HOME": str(Path(temporary) / ".codex"),
                "CI": "1",
                "DO_NOT_TRACK": "1",
                "NPM_CONFIG_UPDATE_NOTIFIER": "false",
            }
            result = subprocess.run(
                [
                    npx,
                    "--yes",
                    f"skills@{NPX_SKILLS_VERSION}",
                    "add",
                    str(ROOT),
                    "--skill",
                    "econ-write",
                    "--agent",
                    "codex",
                    "--global",
                    "--yes",
                    "--copy",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = Path(temporary) / ".agents/skills/econ-write"
            self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))


if __name__ == "__main__":
    unittest.main()
