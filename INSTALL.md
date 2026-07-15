# Install or update Econ Write

This is the canonical installation contract for Econ Write. When a user sends
an agent here, the agent should complete the work itself and return a concise
result—not a list of commands for the user to run.

## Instructions for Codex and Claude Code agents

Follow every step below. The workflow is idempotent: it must work for a first
installation, an update, or an already-current installation.

1. Detect whether the current task is running in Claude Code or Codex. Use the
   native plugin CLI for that client and user scope. Do not install into both
   clients unless the user explicitly asks for both.
2. Inspect the current state before changing it. Treat each reported installation
   scope separately rather than assuming that one record represents every scope:
   - Claude Code: `claude plugin marketplace list` and
     `claude plugin list --json`.
   - Codex: `codex plugin marketplace list` and
     `codex plugin list --json`.
3. Ensure the GitHub marketplace `OpenEconAI/plugins` is registered with the
   marketplace name `openeconai`:
   - If it is absent, add it with the current client's marketplace command.
   - If it is present and points to `OpenEconAI/plugins`, refresh it.
   - If the name exists but points somewhere else, do not load code from that
     source, do not replace it automatically, and do not create a second entry
     with the same identity. Stop safely and report the source conflict as the
     only incomplete item.
4. Install or update the user-scoped `econ-write@openeconai`:
   - Claude Code, absent at user scope:
     `claude plugin install econ-write@openeconai --scope user`.
   - Claude Code, installed at user scope: first run
     `claude plugin marketplace update openeconai`, then
     `claude plugin update econ-write@openeconai --scope user`.
   - Codex: run `codex plugin marketplace upgrade openeconai`, then
     `codex plugin add econ-write@openeconai --json`. The add command installs
     an absent plugin or refreshes an existing installation from the current
     catalog snapshot.
   - If Claude Code reports the installed plugin as disabled, run
     `claude plugin enable econ-write@openeconai --scope user`. Confirm that it
     is enabled before continuing. Codex's add command should return the plugin
     to an installed, enabled state; verify this in its JSON listing.
   Use the native plugin manager only. Do not also use `curl`, `npx`, `git
   clone`, `scripts/install.sh`, or manual skill copies.
5. Obtain the installed plugin directory from structured CLI output; never
   guess a cache path. Claude Code exposes `installPath` in
   `claude plugin list --json`. Codex returns `installedPath` from
   `codex plugin add ... --json`. Before touching any standalone copy, verify
   that the client reports the native plugin as installed and enabled, its
   manifest has the expected name and a valid version, and its
   `skills/econ-write` tree contains `SKILL.md` plus the four companion Markdown
   files.
6. For Claude Code, inspect the structured listing for additional
   `econ-write@openeconai` records at `project` or `local` scope. After the
   user-scoped installation has passed step 5, remove only scopes that the
   listing actually reports, using
   `claude plugin uninstall econ-write@openeconai --scope <scope> --keep-data`.
   Do not run scoped removals speculatively. Recheck the JSON listing and confirm
   that exactly one enabled user-scoped record remains. Codex currently has no
   equivalent project/local plugin scope to migrate.
7. After the package-integrity check passes, inspect these exact standalone
   paths under the current user's home directory:
   - `~/.claude/skills/econ-write`
   - `~/.agents/skills/econ-write`
   - `~/.codex/skills/econ-write`

   Also inspect the following paths under the current project root, if they are
   distinct from the home paths:
   - `<project>/.claude/skills/econ-write`
   - `<project>/.agents/skills/econ-write`
   - `<project>/.codex/skills/econ-write`

   Before changing a project path, check whether it is tracked by that project's
   version control. Never remove or move a tracked path; this includes the
   package mirrors inside an `econ-writing-skill` source checkout. Leave tracked
   source material intact and identify it in the result instead of treating it
   as a legacy installation.

   Inspect path metadata without following a symbolic link, Windows junction,
   or other reparse point. Always move a link or junction itself to the backup
   location; never follow it, delete its target, or treat it as a verified
   duplicate. For an ordinary directory, compare the complete tree with the installed plugin's
   `skills/econ-write` tree. Remove it only when it is a byte-for-byte
   duplicate. If it contains local changes or extra files, move it to a unique
   backup under `~/.openeconai/backups/econ-write/YYYYMMDDTHHMMSSZ/`. Use a
   collision-proof label that identifies the original path. Never delete a
   parent `skills` directory or touch another skill.
8. Perform a final verification:
   - The native `econ-write@openeconai` plugin remains installed and enabled
     from `openeconai` with the same verified version and complete skill tree.
   - No unmanaged standalone `econ-write` path remains active; any modified copy
     has a recorded backup path. A version-controlled project source path may
     remain, but must be reported explicitly.
9. If a safe command fails, diagnose the cause, correct it, and retry. Do not
   switch to a standalone installation that would create a duplicate. Do not
   delete or move an existing standalone copy until the package-integrity check
   in step 5 has passed.
10. Finish with a concise result stating the client, installed plugin version,
   verification outcome, and any backup created. Do not give the user more
   installation commands. If the current session cannot load a newly installed
   plugin, leave the verified installation ready for the next session and say
   so without asking the user to repeat any step.

## Native plugin commands

The instructions above are the preferred workflow. The following commands are
for people who choose to manage the plugin directly.

### Claude Code

Inspect the current state:

```bash
claude plugin marketplace list
claude plugin list --json
```

Fresh installation:

```bash
claude plugin marketplace add OpenEconAI/plugins
claude plugin install econ-write@openeconai --scope user
```

Update:

```bash
claude plugin marketplace update openeconai
claude plugin update econ-write@openeconai --scope user
```

Verify:

```bash
claude plugin details econ-write@openeconai
claude plugin list --json
```

A new Claude Code session loads the installed version automatically. In an
existing interactive session, `/reload-plugins` can load pending changes.

### Codex

Inspect the current state:

```bash
codex plugin marketplace list
codex plugin list --json
```

Fresh installation:

```bash
codex plugin marketplace add OpenEconAI/plugins
codex plugin add econ-write@openeconai
```

Update:

```bash
codex plugin marketplace upgrade openeconai
codex plugin add econ-write@openeconai
```

Verify:

```bash
codex plugin list --marketplace openeconai --json
```

A new Codex session loads the installed version automatically.

### Remove the native plugin

Run only the command for the applicable client:

```bash
claude plugin uninstall econ-write@openeconai --scope user
codex plugin remove econ-write@openeconai
```

Keep the shared `openeconai` marketplace if another OpenEcon.ai plugin uses it.

## Migrate from a standalone skill manually

Older installation methods may have placed Econ Write in one or more of these
directories:

- `~/.claude/skills/econ-write`
- `~/.agents/skills/econ-write`
- `~/.codex/skills/econ-write`

Install and verify the native plugin first. Then compare each exact standalone
directory with the plugin's bundled `skills/econ-write` tree. Remove only a
byte-for-byte duplicate. Move a locally modified copy to
`~/.openeconai/backups/econ-write/<timestamp>/` with its source path identified.
Never remove a parent `skills` directory, which may contain unrelated skills.

## Standalone skill alternatives

Use these only when the native plugin marketplace is unavailable. They install
the skill files directly and do not register a plugin. Rerun the same method to
update, and never combine methods.

### Agent Skills installer

On any platform with Node.js and `npx`:

```bash
npx skills add hanlulong/econ-writing-skill
```

### Bash installer

On macOS or Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash
```

From a clone:

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cd econ-writing-skill
./scripts/install.sh
```

The Bash installer stages all five files before changing an existing copy. A
changed previous copy is preserved under
`~/.openeconai/backups/econ-write/<timestamp>/`. Current Codex installations
use `~/.agents/skills/econ-write`; an old `~/.codex/skills/econ-write` copy is
removed when identical or backed up when modified.

The installer accepts these options:

| Option | Result |
| --- | --- |
| `--global` | Install for all projects; this is the default. |
| `--local [path]` | Install in one project. |
| `--claude` | Install only for Claude Code. |
| `--codex` | Install only for Codex. |
| `--all` | Install for both clients; this is the default. |

For example:

```bash
./scripts/install.sh --local --claude /path/to/project
```

### Manual copy

The complete, canonical skill is the `skills/econ-write` directory in this
repository. Copy the whole directory rather than downloading only `SKILL.md`,
because the skill references its four companion files.

| Client | Global destination |
| --- | --- |
| Claude Code | `~/.claude/skills/econ-write` |
| Codex | `~/.agents/skills/econ-write` |

For a project-specific installation, use `.claude/skills/econ-write` or
`.agents/skills/econ-write` under the project root. On Windows, these paths are
relative to the user profile or project and can be copied with File Explorer
or PowerShell.

## Troubleshooting

- If the plugin is not found, refresh the `openeconai` marketplace and retry
  the native install or update.
- If Econ Write appears twice, keep the native `econ-write@openeconai` plugin
  and deactivate the standalone copy after preserving local changes.
- If the current session still shows an older installed version, open a new
  session. Claude Code can alternatively use `/reload-plugins`.
- If a standalone installation is incomplete, reinstall the entire
  `skills/econ-write` directory so all five files come from one release.
