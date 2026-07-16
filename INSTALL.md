# Install or update Econ Write

This is the canonical installation contract for Econ Write. Standalone skill
installation is the default for Claude Code and Codex. Native plugins remain an
optional installation method.

When a user sends an agent here, the agent should complete the work itself and
return a concise result—not a list of commands for the user to run.

## Instructions for Codex and Claude Code agents

Follow every step below. The workflow must be safe for a first installation, an
update, an already-current installation, or an explicitly requested migration.

1. Detect whether the current task is running in Claude Code or Codex. Operate
   on only that client unless the user explicitly asks for both. Never inspect,
   remove, move, or back up the other client's installation paths.
2. Use the standalone method unless the user explicitly requests the native
   plugin. The user-level standalone destination is:
   - Claude Code: `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/econ-write`
   - Codex: `$HOME/.agents/skills/econ-write`

   For a project-local request, use `<project>/.claude/skills/econ-write` for
   Claude Code or `<project>/.agents/skills/econ-write` for Codex. Use user scope
   unless the user explicitly requests project-local installation.
3. Inspect the selected client's state before changing it:
   - Inspect the selected standalone destination without following symbolic
     links, Windows junctions, or other reparse points.
   - Inspect the selected client's other active standalone scope when it is
     distinct from the destination. For Codex, also inspect the legacy
     `.codex/skills/econ-write` path at the same user or project scope.
   - Check the selected client's native plugin state with structured output:
     - Claude Code: `claude plugin list --json`
     - Codex: `codex plugin list --json`
   - Do not query the other client's plugin manager.
4. Before changing a project path, check whether it is tracked by that
   project's version control. Never remove or move a tracked path. This includes
   the `.claude`, `.agents`, and `skills` mirrors in an
   `econ-writing-skill` source checkout. Report a tracked path instead of
   treating it as a legacy installation.
5. Install or update the standalone skill for the selected client:
   - From a source checkout, run the applicable command:
     - Claude Code: `./scripts/install.sh --global --claude`
     - Codex: `./scripts/install.sh --global --codex`
   - For a remote macOS or Linux installation, run the applicable command:
     - Claude Code: `curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --claude`
     - Codex: `curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --codex`
   - On Windows, use the Agent Skills installer described below or copy the
     complete `skills/econ-write` directory to the selected client destination.

   The Bash installer downloads one version-pinned source archive, validates the
   five required files, stages the complete replacement, and changes the active
   destination only after staging succeeds. An existing non-identical copy is
   normally preserved under `~/.openeconai/backups/econ-write/<timestamp>/`. If that
   central backup root is unavailable or unsafe, the installer uses a reported
   same-volume `.openeconai-inactive/econ-write/` path outside skill discovery.
   A link or junction is moved as an object; its target is never followed or
   modified.
6. Verify the selected standalone destination before deactivating any prior
   copy. It must be an ordinary directory containing these five non-empty files
   from the same source snapshot and no incomplete staging directory:
   - `SKILL.md`
   - `identification-strategies.md`
   - `latex-tips.md`
   - `review-checklist.md`
   - `specialized-tasks.md`
7. Enforce one active Econ Write copy for the selected client only:
   - For any other untracked standalone copy belonging to that client, remove it
     only when its complete tree is byte-for-byte identical to the verified
     destination. If it differs or contains extra files, move it to a unique
     reported backup path, normally under
     `~/.openeconai/backups/econ-write/<timestamp>/`, with the same-volume
     inactive location as the safe fallback. Move a link or junction itself and
     never follow its target. Never remove a parent `skills` directory or touch
     another skill.
   - If `econ-write@openeconai` is installed for the selected client, remove it
     only after step 6 passes:
     - Claude Code: remove only scopes actually reported by the JSON listing,
       using `claude plugin uninstall econ-write@openeconai --scope <scope> --keep-data`.
       Never run a scoped removal speculatively.
     - Codex: `codex plugin remove econ-write@openeconai --json`.
   - Do not remove a similarly named package from any other marketplace, and do
     not touch the other client even if it also has Econ Write installed.
8. Perform final verification for the selected client:
   - The selected standalone destination remains complete and byte-for-byte
     consistent with the staged source.
   - No untracked same-client duplicate or same-client native plugin remains
     active. A tracked project source path may remain but must be reported.
   - Every modified prior copy has a recorded backup path.
9. If a safe command fails, diagnose the cause, correct it, and retry. Never
   remove a prior copy before the replacement passes verification. If cleanup
   fails after successful installation, leave the verified replacement intact
   and report the remaining same-client duplicate precisely.
10. Finish with a concise result stating the client, standalone destination,
    verification outcome, same-client migration outcome, and any backup created.
    Do not give the user more installation commands. A newly installed skill may
    require a new client session before it appears.

## Alternative direct standalone installation

The agent workflow above is preferred because it handles same-client migration
and verification. The commands below install the standalone files directly.

### Agent Skills installer

On any platform with Node.js and `npx`:

```bash
npx skills add hanlulong/econ-writing-skill
```

Select only the client you intend to configure. Rerun the same method to update.

### Bash installer

On macOS or Linux, select exactly one client:

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --claude
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --codex
```

Use `--all` only when you intentionally want both clients:

```bash
curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --all
```

From a clone:

```bash
git clone https://github.com/hanlulong/econ-writing-skill.git
cd econ-writing-skill
./scripts/install.sh --global --claude
```

The installer accepts these options:

| Option | Result |
| --- | --- |
| `--global` | Install for all projects; this is the default scope. |
| `--local [path]` | Install in one project. |
| `--claude` | Install only for Claude Code. |
| `--codex` | Install only for Codex. |
| `--all` | Explicitly install for both clients. |

Exactly one of `--claude`, `--codex`, or `--all` is required. The global Claude
destination honors an absolute `CLAUDE_CONFIG_DIR`. Codex standalone skills
remain under `$HOME/.agents/skills` and are not relocated by `CODEX_HOME`.

### Manual copy

Copy the complete canonical `skills/econ-write` directory rather than only
`SKILL.md`, because the skill references four companion files.

| Client | User-level destination |
| --- | --- |
| Claude Code | `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/econ-write` |
| Codex | `$HOME/.agents/skills/econ-write` |

For project-local installation, use `.claude/skills/econ-write` or
`.agents/skills/econ-write` under the project root.

## Native plugin installation (optional)

Choose this method explicitly when you prefer plugin-manager updates. Do not
keep a standalone copy active for the same client. Install and verify the plugin
before deactivating only that client's standalone copy.

### Claude Code native plugin

Fresh installation:

```bash
claude plugin marketplace add OpenEconAI/plugins
claude plugin install econ-write@openeconai --scope user
```

Update and verify:

```bash
claude plugin marketplace update openeconai
claude plugin update econ-write@openeconai --scope user
claude plugin details econ-write@openeconai
claude plugin list --json
```

Explicit plugin invocation: `/econ-write:econ-write`.

Remove:

```bash
claude plugin uninstall econ-write@openeconai --scope user
```

### Codex native plugin

Fresh installation:

```bash
codex plugin marketplace add OpenEconAI/plugins
codex plugin add econ-write@openeconai --json
```

Update and verify:

```bash
codex plugin marketplace upgrade openeconai
codex plugin add econ-write@openeconai --json
codex plugin list --marketplace openeconai --json
```

Explicit plugin invocation: `$econ-write:econ-write`.

Remove:

```bash
codex plugin remove econ-write@openeconai --json
```

Natural-language requests can activate either installation method
automatically because both package the same `econ-write` skill description.

## Switching installation methods

Migrate only the selected client. Never clean the other client's paths as a
side effect.

### Native plugin to standalone

Install and verify the standalone destination first. Then remove only the
selected client's reported `econ-write@openeconai` plugin records. Recheck both
states and confirm that only the standalone copy remains active.

### Standalone to native plugin

Install and verify `econ-write@openeconai` first. Then compare the selected
client's standalone tree with the plugin's bundled `skills/econ-write` tree.
Remove a byte-for-byte duplicate; back up a modified copy under
`~/.openeconai/backups/econ-write/<timestamp>/`. Recheck both states and confirm
that only the native plugin remains active.

## Troubleshooting

- If a standalone installation is incomplete, rerun the selected client's
  installation so all five files come from one source snapshot.
- If Econ Write appears twice, identify which method was selected, verify it,
  and deactivate only the same client's other copy. Preserve local changes.
- If a native plugin is not found, refresh the `openeconai` marketplace and
  retry the optional native installation.
- If the current session still shows an older copy, open a new session. Claude
  Code can alternatively use `/reload-plugins` for native-plugin updates.
- If the marketplace name `openeconai` points somewhere other than
  `OpenEconAI/plugins`, do not load code from it or replace it automatically.
  Stop safely and report the source conflict.
