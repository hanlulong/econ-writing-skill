#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILL = ROOT / "skills" / "econ-write"
CLAUDE_MIRROR = ROOT / ".claude" / "skills" / "econ-write"
CODEX_MIRROR = ROOT / ".agents" / "skills" / "econ-write"
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
INSTALL_GUIDE = ROOT / "INSTALL.md"
INSTALLER = ROOT / "scripts" / "install.sh"
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


def write_source_archive(archive: Path) -> None:
    with tarfile.open(archive, "w:gz") as bundle:
        for path in sorted(CANONICAL_SKILL.iterdir()):
            if path.is_file():
                bundle.add(
                    path,
                    arcname=f"econ-writing-skill-main/skills/econ-write/{path.name}",
                )


def write_source_archive_with_linked_skill(archive: Path) -> None:
    with tarfile.open(archive, "w:gz") as bundle:
        for path in sorted(CANONICAL_SKILL.iterdir()):
            archive_name = f"econ-writing-skill-main/skills/econ-write/{path.name}"
            if path.name == "SKILL.md":
                link = tarfile.TarInfo(archive_name)
                link.type = tarfile.SYMTYPE
                link.linkname = "/etc/passwd"
                bundle.addfile(link)
            elif path.is_file():
                bundle.add(path, arcname=archive_name)


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
        self.assertEqual(claude["version"], "0.1.2")
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

    def test_readme_leads_with_one_paste_agent_install(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        prompt_match = re.search(
            r"## Installation.*?```text\n(.*?)\n```",
            readme,
            re.DOTALL,
        )
        self.assertIsNotNone(prompt_match)
        prompt = prompt_match.group(1) if prompt_match is not None else ""

        required_prompt_text = (
            "Install or update Econ Write as a standalone skill",
            "https://github.com/hanlulong/econ-writing-skill/blob/main/INSTALL.md",
            "Handle same-client migration, backups, and verification yourself.",
            "Do not install for or change the other client.",
            "Do not ask me to run commands.",
            "Finish with a concise result.",
        )
        for text in required_prompt_text:
            with self.subTest(text=text):
                self.assertIn(text, prompt)
        self.assertLessEqual(len(prompt.split()), 60)

        delegated_install_commands = (
            "main/scripts/install.sh | bash -s -- --global --claude",
            "main/scripts/install.sh | bash -s -- --global --codex",
            "claude plugin marketplace add OpenEconAI/plugins",
            "claude plugin install econ-write@openeconai --scope user",
            "codex plugin marketplace add OpenEconAI/plugins",
            "codex plugin add econ-write@openeconai",
        )
        for command in delegated_install_commands:
            with self.subTest(command=command):
                self.assertNotIn(command, readme)

        installation_section = readme.split("## Installation", 1)[1].split(
            "## Usage", 1
        )[0]
        self.assertEqual(installation_section.count("### "), 0)
        self.assertNotIn("### Recommended installation", installation_section)
        self.assertNotIn("### Standalone commands", installation_section)
        self.assertNotIn("### Native plugin installation", installation_section)
        self.assertIn("[Installation and updates](INSTALL.md)", readme)
        self.assertNotIn("/econ-write:econ-write", installation_section)
        self.assertNotIn("$econ-write:econ-write", installation_section)
        self.assertIn(
            "Use only one installation method\nper client", installation_section
        )

        usage_section = readme.split("## Usage", 1)[1].split(
            "## Common Use Cases", 1
        )[0]
        self.assertIn("/econ-write write introduction", usage_section)
        self.assertIn("$econ-write rewrite this abstract", usage_section)
        self.assertNotIn("/econ-write:econ-write", usage_section)
        self.assertNotIn("$econ-write:econ-write", usage_section)

    def test_install_guide_covers_updates_and_alternatives_without_old_catalogs(
        self,
    ) -> None:
        self.assertTrue(INSTALL_GUIDE.is_file())
        self.assertFalse((ROOT / "docs" / "INSTALL.md").exists())
        self.assertFalse((ROOT / "install.sh").exists())
        self.assertTrue(INSTALLER.is_file())
        self.assertTrue(os.access(INSTALLER, os.X_OK))
        guide = INSTALL_GUIDE.read_text(encoding="utf-8")
        normalized_guide = " ".join(guide.split())
        required = (
            "This is the canonical installation contract for Econ Write.",
            "Standalone skill installation is the default for Claude Code and Codex.",
            "Operate on only that client unless the user explicitly asks for both.",
            "Never inspect, remove, move, or back up the other client's installation paths.",
            "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/econ-write",
            "$HOME/.agents/skills/econ-write",
            "downloads one version-pinned source archive",
            "five required files",
            "No untracked same-client duplicate or same-client native plugin remains active.",
            "Native plugin installation (optional)",
            "OpenEconAI/plugins",
            "do not load code from it",
            "claude plugin marketplace update openeconai",
            "claude plugin update econ-write@openeconai --scope user",
            "claude plugin details econ-write@openeconai",
            "claude plugin uninstall econ-write@openeconai --scope user",
            "codex plugin marketplace upgrade openeconai",
            "codex plugin add econ-write@openeconai --json",
            "codex plugin list --marketplace openeconai --json",
            "codex plugin remove econ-write@openeconai",
            "remove only scopes actually reported by the JSON listing",
            "--scope <scope> --keep-data",
            "<project>/.claude/skills/econ-write",
            "Never remove or move a tracked path",
            "byte-for-byte",
            "~/.openeconai/backups/econ-write/<timestamp>/",
            "Do not give the user more installation commands.",
            "npx skills add hanlulong/econ-writing-skill",
            "main/scripts/install.sh | bash -s -- --global --claude",
            "main/scripts/install.sh | bash -s -- --global --codex",
            "/econ-write:econ-write",
            "$econ-write:econ-write",
            "Exactly one of `--claude`, `--codex`, or `--all` is required.",
            "skills/econ-write",
        )
        for text in required:
            with self.subTest(text=text):
                self.assertIn(" ".join(text.split()), normalized_guide)

        combined = (ROOT / "README.md").read_text(encoding="utf-8") + guide
        forbidden = (
            "econ-write@econ-paper-review",
            "econ-write@econ-review",
            "marketplace add hanlulong/econ-writing-skill",
        )
        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, combined)

        self.assertLess(
            guide.index("## Alternative direct standalone installation"),
            guide.index("## Native plugin installation (optional)"),
        )

        installer = INSTALLER.read_text(encoding="utf-8")
        self.assertIn('RELEASE_TAG="econ-write--v0.1.2"', installer)
        self.assertIn("REPO_ARCHIVE_URL=", installer)
        self.assertIn("codeload.github.com/hanlulong/econ-writing-skill/tar.gz", installer)
        self.assertIn("/refs/tags/$RELEASE_TAG", installer)
        self.assertNotIn("/refs/heads/main", installer)
        self.assertNotIn("/main/skills/econ-write/", installer)
        self.assertIn('PLATFORM=""', installer)

    def test_skill_metadata_preserves_implicit_and_explicit_standalone_invocation(
        self,
    ) -> None:
        metadata = frontmatter(CANONICAL_SKILL / "SKILL.md")
        self.assertIn("name: econ-write", metadata)
        description_match = re.search(r'^description: "(.*)"$', metadata, re.MULTILINE)
        self.assertIsNotNone(description_match)
        description = description_match.group(1) if description_match else ""
        self.assertLessEqual(len(description), 1024)
        for trigger in ("economics paper", "abstract", "results section", "referee response"):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, description)
        self.assertNotIn("disable-model-invocation", metadata)
        self.assertFalse((CANONICAL_SKILL / "agents" / "openai.yaml").exists())

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
                [claude, "plugin", "marketplace", "update", "openeconai"],
                [
                    claude,
                    "plugin",
                    "update",
                    "econ-write@openeconai",
                    "--scope",
                    "user",
                ],
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
            disable = subprocess.run(
                [
                    claude,
                    "plugin",
                    "disable",
                    "econ-write@openeconai",
                    "--scope",
                    "user",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(disable.returncode, 0, disable.stdout + disable.stderr)
            update_while_disabled = subprocess.run(
                [
                    claude,
                    "plugin",
                    "update",
                    "econ-write@openeconai",
                    "--scope",
                    "user",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                update_while_disabled.returncode,
                0,
                update_while_disabled.stdout + update_while_disabled.stderr,
            )
            disabled_list = subprocess.run(
                [claude, "plugin", "list", "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                disabled_list.returncode,
                0,
                disabled_list.stdout + disabled_list.stderr,
            )
            disabled_record = next(
                item
                for item in json.loads(disabled_list.stdout)
                if item["id"] == "econ-write@openeconai"
            )
            self.assertFalse(disabled_record["enabled"])
            enable = subprocess.run(
                [
                    claude,
                    "plugin",
                    "enable",
                    "econ-write@openeconai",
                    "--scope",
                    "user",
                ],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(enable.returncode, 0, enable.stdout + enable.stderr)
            enabled_list = subprocess.run(
                [claude, "plugin", "list", "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                enabled_list.returncode,
                0,
                enabled_list.stdout + enabled_list.stderr,
            )
            enabled_record = next(
                item
                for item in json.loads(enabled_list.stdout)
                if item["id"] == "econ-write@openeconai"
            )
            self.assertTrue(enabled_record["enabled"])
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
            reinstall = subprocess.run(
                [codex, "plugin", "add", "econ-write@openeconai", "--json"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                reinstall.returncode, 0, reinstall.stdout + reinstall.stderr
            )
            self.assertEqual(Path(json.loads(reinstall.stdout)["installedPath"]), installed)
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

    def test_direct_installer_uses_current_paths_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            env = {**os.environ, "HOME": temporary}
            results = [
                subprocess.run(
                    ["bash", str(INSTALLER), "--global", "--all"],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                for _ in range(2)
            ]
            for result in results:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            home = Path(temporary)
            for installed in (
                home / ".claude/skills/econ-write",
                home / ".agents/skills/econ-write",
            ):
                with self.subTest(path=installed.as_posix()):
                    self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))
            self.assertFalse((home / ".codex/skills/econ-write").exists())
            self.assertIn("Already current for Claude Code", results[1].stdout)
            self.assertIn("Already current for Codex", results[1].stdout)
            self.assertFalse((home / ".openeconai/backups").exists())

    def test_direct_installer_never_changes_the_other_client(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            codex = home / ".agents/skills/econ-write"
            legacy_codex = home / ".codex/skills/econ-write"
            codex.mkdir(parents=True)
            legacy_codex.mkdir(parents=True)
            (codex / "sentinel.txt").write_text("current codex\n", encoding="utf-8")
            (legacy_codex / "sentinel.txt").write_text(
                "legacy codex\n", encoding="utf-8"
            )
            codex_before = skill_files(codex)
            legacy_before = skill_files(legacy_codex)

            claude_result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--claude"],
                cwd=ROOT,
                env={**os.environ, "HOME": temporary},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                claude_result.returncode,
                0,
                claude_result.stdout + claude_result.stderr,
            )
            self.assertEqual(skill_files(codex), codex_before)
            self.assertEqual(skill_files(legacy_codex), legacy_before)
            self.assertFalse((home / ".openeconai/backups").exists())

        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            claude = home / ".claude/skills/econ-write"
            claude.mkdir(parents=True)
            (claude / "sentinel.txt").write_text("claude\n", encoding="utf-8")
            claude_before = skill_files(claude)

            codex_result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--codex"],
                cwd=ROOT,
                env={**os.environ, "HOME": temporary},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                codex_result.returncode,
                0,
                codex_result.stdout + codex_result.stderr,
            )
            self.assertEqual(skill_files(claude), claude_before)
            self.assertFalse((home / ".openeconai/backups").exists())

    def test_direct_installer_honors_absolute_claude_config_dir(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "home"
            config = Path(temporary) / "Claude Config With Spaces"
            env = {
                **os.environ,
                "HOME": str(home),
                "CLAUDE_CONFIG_DIR": str(config),
            }
            results = [
                subprocess.run(
                    ["bash", str(INSTALLER), "--global", "--claude"],
                    cwd=ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                for _ in range(2)
            ]
            for result in results:
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Claude Code: /econ-write", result.stdout)
                self.assertNotIn("Codex: $econ-write", result.stdout)
            self.assertEqual(
                skill_files(config / "skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertFalse((home / ".claude/skills/econ-write").exists())
            self.assertIn("Already current for Claude Code", results[1].stdout)

            relative = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--claude"],
                cwd=ROOT,
                env={
                    **os.environ,
                    "HOME": str(Path(temporary) / "other-home"),
                    "CLAUDE_CONFIG_DIR": "relative-config",
                },
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(relative.returncode, 2)
            self.assertIn("must be an absolute path", relative.stderr)
            self.assertFalse((ROOT / "relative-config").exists())

    def test_direct_installer_prints_only_selected_client_invocation(self) -> None:
        for platform, expected, forbidden in (
            ("--claude", "Claude Code: /econ-write", "Codex: $econ-write"),
            ("--codex", "Codex: $econ-write", "Claude Code: /econ-write"),
        ):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as temporary:
                result = subprocess.run(
                    ["bash", str(INSTALLER), "--global", platform],
                    cwd=ROOT,
                    env={**os.environ, "HOME": temporary},
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(expected, result.stdout)
                self.assertNotIn(forbidden, result.stdout)

    def test_direct_installer_deactivates_or_preserves_legacy_codex_copy(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            env = {**os.environ, "HOME": temporary}
            legacy = home / ".codex/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, legacy)

            identical = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--codex"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(
                identical.returncode, 0, identical.stdout + identical.stderr
            )
            self.assertFalse(legacy.exists())
            self.assertIn("Removed duplicate legacy Codex copy", identical.stdout)

        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            env = {**os.environ, "HOME": temporary}
            legacy = home / ".codex/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, legacy)
            custom_text = "local customization\n"
            (legacy / "local-notes.md").write_text(custom_text, encoding="utf-8")

            modified = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--codex"],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(modified.returncode, 0, modified.stdout + modified.stderr)
            self.assertFalse(legacy.exists())
            backups = list(
                (home / ".openeconai/backups/econ-write").rglob("local-notes.md")
            )
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), custom_text)
            self.assertRegex(
                backups[0].relative_to(home).parts[3],
                r"^\d{8}T\d{6}Z-\d+$",
            )

        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            project = temporary_root / "project"
            legacy = project / ".codex/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, legacy)
            result = subprocess.run(
                ["bash", str(INSTALLER), "--local", "--codex", str(project)],
                cwd=ROOT,
                env={**os.environ, "HOME": str(temporary_root / "home")},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(legacy.exists())
            self.assertEqual(
                skill_files(project / ".agents/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )

    def test_direct_installer_failed_download_does_not_change_existing_copy(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            home = temporary_root / "home"
            installed = home / ".claude/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, installed)
            (installed / "SKILL.md").write_text(
                "local version that must survive\n", encoding="utf-8"
            )
            before = skill_files(installed)

            standalone_installer = temporary_root / "install.sh"
            shutil.copy2(INSTALLER, standalone_installer)
            fake_bin = temporary_root / "bin"
            fake_bin.mkdir()
            fake_curl = fake_bin / "curl"
            fake_curl.write_text(
                """#!/usr/bin/env python3
raise SystemExit(22)
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            env = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
            }
            result = subprocess.run(
                ["bash", str(standalone_installer), "--global", "--claude"],
                cwd=temporary_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("existing installations were not changed", result.stderr)
            self.assertEqual(skill_files(installed), before)
            self.assertEqual(
                list(installed.parent.glob(".econ-write-install.*")), []
            )

    def test_direct_installer_rejects_ambiguous_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            env = {**os.environ, "HOME": temporary}
            cases = (
                [],
                ["--unknown"],
                ["--claude", "--codex"],
                ["--all", "--codex"],
                ["--claude", "target-without-local"],
                ["--local", "--claude", "first", "second"],
            )
            for arguments in cases:
                with self.subTest(arguments=arguments):
                    result = subprocess.run(
                        ["bash", str(INSTALLER), *arguments],
                        cwd=ROOT,
                        env=env,
                        capture_output=True,
                        text=True,
                        timeout=60,
                    )
                    self.assertEqual(result.returncode, 2)
            home = Path(temporary)
            self.assertFalse((home / ".claude").exists())
            self.assertFalse((home / ".agents").exists())
            self.assertFalse((home / ".codex").exists())

    def test_direct_installer_requires_complete_local_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            incomplete_repo = temporary_root / "incomplete-repo"
            incomplete_skill = incomplete_repo / "skills/econ-write"
            incomplete_skill.mkdir(parents=True)
            incomplete_scripts = incomplete_repo / "scripts"
            incomplete_scripts.mkdir()
            shutil.copy2(INSTALLER, incomplete_scripts / "install.sh")
            shutil.copy2(CANONICAL_SKILL / "SKILL.md", incomplete_skill / "SKILL.md")

            home = temporary_root / "home"
            installed = home / ".claude/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, installed)
            before = skill_files(installed)
            result = subprocess.run(
                [
                    "bash",
                    str(incomplete_scripts / "install.sh"),
                    "--global",
                    "--claude",
                ],
                cwd=incomplete_repo,
                env={**os.environ, "HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source is incomplete", result.stderr)
            self.assertEqual(skill_files(installed), before)

    def test_piped_installer_does_not_trust_working_directory_as_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            malicious_cwd = temporary_root / "untrusted project"
            malicious_skill = malicious_cwd / "skills/econ-write"
            malicious_skill.mkdir(parents=True)
            for filename in skill_files(CANONICAL_SKILL):
                (malicious_skill / filename).write_text(
                    f"untrusted {filename}\n", encoding="utf-8"
                )

            fake_bin = temporary_root / "bin"
            fake_bin.mkdir()
            remote_archive = temporary_root / "source.tar.gz"
            write_source_archive(remote_archive)
            fake_curl = fake_bin / "curl"
            fake_curl.write_text(
                """#!/usr/bin/env python3
import os
import pathlib
import shutil
import sys

destination = pathlib.Path(sys.argv[sys.argv.index("-o") + 1])
shutil.copy2(pathlib.Path(os.environ["FAKE_REMOTE_ARCHIVE"]), destination)
counter = pathlib.Path(os.environ["FAKE_CURL_COUNTER"])
counter.write_text(str(int(counter.read_text() if counter.exists() else "0") + 1))
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            home = temporary_root / "home"
            env = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
                "FAKE_REMOTE_ARCHIVE": str(remote_archive),
                "FAKE_CURL_COUNTER": str(temporary_root / "curl-count"),
            }
            result = subprocess.run(
                ["bash", "-s", "--", "--global", "--claude"],
                cwd=malicious_cwd,
                env=env,
                input=INSTALLER.read_text(encoding="utf-8"),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = home / ".claude/skills/econ-write"
            self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))
            self.assertNotEqual(skill_files(installed), skill_files(malicious_skill))
            self.assertEqual((temporary_root / "curl-count").read_text(), "1")

    def test_piped_all_client_install_uses_one_source_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            archive = temporary_root / "source.tar.gz"
            write_source_archive(archive)
            fake_bin = temporary_root / "bin"
            fake_bin.mkdir()
            fake_curl = fake_bin / "curl"
            fake_curl.write_text(
                """#!/usr/bin/env python3
import os
import pathlib
import shutil
import sys

destination = pathlib.Path(sys.argv[sys.argv.index("-o") + 1])
shutil.copy2(pathlib.Path(os.environ["FAKE_REMOTE_ARCHIVE"]), destination)
counter = pathlib.Path(os.environ["FAKE_CURL_COUNTER"])
counter.write_text(str(int(counter.read_text() if counter.exists() else "0") + 1))
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            home = temporary_root / "home"
            counter = temporary_root / "curl-count"
            result = subprocess.run(
                ["bash", "-s", "--", "--global", "--all"],
                cwd=temporary_root,
                env={
                    **os.environ,
                    "HOME": str(home),
                    "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
                    "FAKE_REMOTE_ARCHIVE": str(archive),
                    "FAKE_CURL_COUNTER": str(counter),
                },
                input=INSTALLER.read_text(encoding="utf-8"),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(counter.read_text(), "1")
            self.assertEqual(
                skill_files(home / ".claude/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )
            self.assertEqual(
                skill_files(home / ".agents/skills/econ-write"),
                skill_files(CANONICAL_SKILL),
            )

    def test_piped_installer_rejects_linked_required_archive_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            archive = temporary_root / "linked-source.tar.gz"
            write_source_archive_with_linked_skill(archive)
            fake_bin = temporary_root / "bin"
            fake_bin.mkdir()
            fake_curl = fake_bin / "curl"
            fake_curl.write_text(
                """#!/usr/bin/env python3
import os
import pathlib
import shutil
import sys

destination = pathlib.Path(sys.argv[sys.argv.index("-o") + 1])
shutil.copy2(pathlib.Path(os.environ["FAKE_REMOTE_ARCHIVE"]), destination)
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            home = temporary_root / "home"
            installed = home / ".claude/skills/econ-write"
            installed.mkdir(parents=True)
            (installed / "keep.txt").write_text("prior copy\n", encoding="utf-8")
            before = skill_files(installed)
            result = subprocess.run(
                ["bash", "-s", "--", "--global", "--claude"],
                cwd=temporary_root,
                env={
                    **os.environ,
                    "HOME": str(home),
                    "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
                    "FAKE_REMOTE_ARCHIVE": str(archive),
                },
                input=INSTALLER.read_text(encoding="utf-8"),
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source is incomplete", result.stderr)
            self.assertEqual(skill_files(installed), before)

    def test_direct_installer_handles_space_in_local_target(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            target = temporary_root / "project with spaces"
            result = subprocess.run(
                [
                    "bash",
                    str(INSTALLER),
                    "--local",
                    "--claude",
                    str(target),
                ],
                cwd=ROOT,
                env={**os.environ, "HOME": str(temporary_root / "home")},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            installed = target / ".claude/skills/econ-write"
            self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))

    @unittest.skipIf(os.name == "nt", "symlink creation is privilege-dependent on Windows")
    def test_direct_installer_refuses_linked_destination_ancestor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary) / "home"
            outside = Path(temporary) / "outside-agents"
            home.mkdir()
            outside.mkdir()
            (home / ".agents").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--codex"],
                cwd=ROOT,
                env={**os.environ, "HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsafe Codex", result.stderr)
            self.assertFalse((outside / "skills").exists())

    @unittest.skipIf(os.name == "nt", "symlink creation is privilege-dependent on Windows")
    def test_direct_installer_never_follows_linked_central_backup_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            home = root / "home"
            installed = home / ".claude/skills/econ-write"
            installed.mkdir(parents=True)
            (installed / "local-notes.md").write_text("preserve me\n", encoding="utf-8")
            outside = root / "outside-backups"
            outside.mkdir()
            (home / ".openeconai").symlink_to(outside, target_is_directory=True)
            result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--claude"],
                cwd=ROOT,
                env={**os.environ, "HOME": str(home)},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(skill_files(installed), skill_files(CANONICAL_SKILL))
            self.assertEqual(list(outside.rglob("local-notes.md")), [])
            preserved = list(
                (home / ".claude/.openeconai-inactive/econ-write").rglob(
                    "local-notes.md"
                )
            )
            self.assertEqual(len(preserved), 1)
            self.assertEqual(preserved[0].read_text(encoding="utf-8"), "preserve me\n")
            self.assertIn("original volume", result.stdout)

    def test_legacy_backup_failure_is_reported_without_false_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            legacy = home / ".codex/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, legacy)
            (legacy / "local-notes.md").write_text("keep me\n", encoding="utf-8")
            (home / ".openeconai").write_text(
                "blocks creation of the backup directory\n", encoding="utf-8"
            )
            (home / ".codex/.openeconai-inactive").write_text(
                "blocks the same-volume fallback\n", encoding="utf-8"
            )
            result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--codex"],
                cwd=ROOT,
                env={**os.environ, "HOME": temporary},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(legacy.is_dir())
            self.assertNotIn("Done!", result.stdout)
            self.assertIn("Could not deactivate", result.stdout)

    def test_current_install_backup_failure_restores_previous_copy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            installed = home / ".claude/skills/econ-write"
            installed.mkdir(parents=True)
            (installed / "local-notes.md").write_text("keep me\n", encoding="utf-8")
            before = skill_files(installed)
            (home / ".openeconai").write_text(
                "blocks creation of the backup directory\n", encoding="utf-8"
            )
            (home / ".claude/.openeconai-inactive").write_text(
                "blocks the same-volume fallback\n", encoding="utf-8"
            )
            result = subprocess.run(
                ["bash", str(INSTALLER), "--global", "--claude"],
                cwd=ROOT,
                env={**os.environ, "HOME": temporary},
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(skill_files(installed), before)
            self.assertNotIn("Done!", result.stdout)
            self.assertIn("restoring it", result.stdout)

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
