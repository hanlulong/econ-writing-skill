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
        self.assertEqual(claude["version"], "0.1.1")
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
            r"### Paste this into your agent \(recommended\).*?```text\n(.*?)\n```",
            readme,
            re.DOTALL,
        )
        self.assertIsNotNone(prompt_match)
        prompt = prompt_match.group(1) if prompt_match is not None else ""

        required_prompt_text = (
            "Install or update Econ Write for me.",
            "https://github.com/hanlulong/econ-writing-skill/blob/main/INSTALL.md",
            "Handle every step yourself, including migration and verification.",
            "Do not ask me to run commands.",
            "Finish with a concise result.",
        )
        for text in required_prompt_text:
            with self.subTest(text=text):
                self.assertIn(text, prompt)
        self.assertLessEqual(len(prompt.split()), 45)

        required_fallback_commands = (
            "claude plugin marketplace add OpenEconAI/plugins",
            "claude plugin install econ-write@openeconai --scope user",
            "codex plugin marketplace add OpenEconAI/plugins",
            "codex plugin add econ-write@openeconai",
        )
        for command in required_fallback_commands:
            with self.subTest(command=command):
                self.assertIn(command, readme)

        installation_section = readme.split("## Installation", 1)[1].split(
            "## Usage", 1
        )[0]
        self.assertLess(
            installation_section.index("### Paste this into your agent"),
            installation_section.index("### Native commands"),
        )
        self.assertIn("[Installation and updates](INSTALL.md)", readme)
        self.assertNotIn("curl -fsSL", installation_section)
        self.assertNotIn("npx skills add", installation_section)
        self.assertNotIn("### Manual Installation", installation_section)
        self.assertNotIn("~/.claude/skills/econ-write", installation_section)

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
            "The workflow is idempotent",
            "Do not install into both clients unless the user explicitly asks for both.",
            "OpenEconAI/plugins",
            "do not load code from that source",
            "claude plugin marketplace update openeconai",
            "claude plugin update econ-write@openeconai --scope user",
            "claude plugin details econ-write@openeconai",
            "claude plugin uninstall econ-write@openeconai --scope user",
            "codex plugin marketplace upgrade openeconai",
            "codex plugin add econ-write@openeconai --json",
            "codex plugin list --marketplace openeconai --json",
            "codex plugin remove econ-write@openeconai",
            "never guess a cache path",
            "remove only scopes that the listing actually reports",
            "--scope <scope> --keep-data",
            "<project>/.claude/skills/econ-write",
            "Never remove or move a tracked path",
            "For an ordinary directory",
            "byte-for-byte",
            "~/.openeconai/backups/econ-write/<timestamp>/",
            "Do not give the user more installation commands.",
            "npx skills add hanlulong/econ-writing-skill",
            "main/scripts/install.sh | bash",
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

        installer = INSTALLER.read_text(encoding="utf-8")
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
import os
import pathlib
import sys

counter = pathlib.Path(os.environ["FAKE_CURL_COUNTER"])
count = int(counter.read_text() if counter.exists() else "0") + 1
counter.write_text(str(count))
destination = pathlib.Path(sys.argv[sys.argv.index("-o") + 1])
if count == 3:
    raise SystemExit(22)
destination.write_text(f"download {count}\\n")
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            env = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
                "FAKE_CURL_COUNTER": str(temporary_root / "curl-count"),
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
            self.assertIn("existing installation was not changed", result.stdout)
            self.assertEqual(skill_files(installed), before)
            self.assertEqual(
                list(installed.parent.glob(".econ-write-install.*")), []
            )

    def test_direct_installer_rejects_ambiguous_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            env = {**os.environ, "HOME": temporary}
            cases = (
                ["--unknown"],
                ["target-without-local"],
                ["--local", "first", "second"],
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
            self.assertIn("Local source is incomplete", result.stderr)
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
            fake_curl = fake_bin / "curl"
            fake_curl.write_text(
                """#!/usr/bin/env python3
import os
import pathlib
import shutil
import sys

url = next(arg for arg in sys.argv if arg.startswith("https://"))
destination = pathlib.Path(sys.argv[sys.argv.index("-o") + 1])
shutil.copy2(pathlib.Path(os.environ["FAKE_REMOTE_SKILL"]) / url.rsplit("/", 1)[-1], destination)
""",
                encoding="utf-8",
            )
            fake_curl.chmod(0o755)
            home = temporary_root / "home"
            env = {
                **os.environ,
                "HOME": str(home),
                "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
                "FAKE_REMOTE_SKILL": str(CANONICAL_SKILL),
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

    def test_legacy_backup_failure_is_reported_without_false_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            legacy = home / ".codex/skills/econ-write"
            shutil.copytree(CANONICAL_SKILL, legacy)
            (legacy / "local-notes.md").write_text("keep me\n", encoding="utf-8")
            (home / ".openeconai").write_text(
                "blocks creation of the backup directory\n", encoding="utf-8"
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
