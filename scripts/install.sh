#!/bin/bash
# Install Econ Writing Skill for Claude Code and/or Codex
#
# Usage:
#   ./scripts/install.sh --claude     Install globally for Claude Code
#   ./scripts/install.sh --codex      Install globally for Codex
#   ./scripts/install.sh --all        Install globally for both clients
#   ./scripts/install.sh --local --claude  Install to current project for Claude Code
#   ./scripts/install.sh --help       Show help
#
# One-line install (no git clone needed):
#   curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --claude

set -e

RELEASE_TAG="econ-write--v0.1.2"
REPO_ARCHIVE_URL="${ECON_WRITE_ARCHIVE_URL:-https://codeload.github.com/hanlulong/econ-writing-skill/tar.gz/refs/tags/$RELEASE_TAG}"
SKILL_FILES=("SKILL.md" "identification-strategies.md" "latex-tips.md" "review-checklist.md" "specialized-tasks.md")
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
BACKUP_ROOT="$HOME/.openeconai/backups/econ-write/$RUN_ID"
BACKUPS_CREATED=0
SOURCE_STAGE_ROOT=""
SOURCE_SKILL_DIR=""

# Parse arguments
MODE="global"
PLATFORM=""
TARGET=""
TARGET_SET=0

print_help() {
    echo "Econ Writing Skill Installer"
    echo ""
    echo "Usage: ./scripts/install.sh [options] [target-directory]"
    echo ""
    echo "Options:"
    echo "  --global     Install to global skill directories (default)"
    echo "  --local      Install to project directory only"
    echo "  --claude     Install for Claude Code only"
    echo "  --codex      Install for Codex only"
    echo "  --all        Install for both clients explicitly"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/install.sh --global --claude             # Claude Code only"
    echo "  ./scripts/install.sh --global --codex              # Codex only"
    echo "  ./scripts/install.sh --global --all                # Both clients"
    echo "  ./scripts/install.sh --local --claude .            # Current project"
    echo "  ./scripts/install.sh --local --codex /path/to/repo # Specific project"
    echo ""
    echo "One-line install (no git clone needed):"
    echo "  curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash -s -- --global --claude"
}

select_platform() {
    local selected="$1"

    if [ -n "$PLATFORM" ] && [ "$PLATFORM" != "$selected" ]; then
        echo "Error: Choose exactly one of --claude, --codex, or --all." >&2
        exit 2
    fi
    PLATFORM="$selected"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --global) MODE="global"; shift ;;
        --local)  MODE="local"; shift ;;
        --claude) select_platform "claude"; shift ;;
        --codex)  select_platform "codex"; shift ;;
        --all)    select_platform "all"; shift ;;
        --help)   print_help; exit 0 ;;
        -*)
            echo "Error: Unknown option: $1" >&2
            print_help >&2
            exit 2
            ;;
        *)
            if [ "$TARGET_SET" -eq 1 ]; then
                echo "Error: Only one target directory may be provided." >&2
                exit 2
            fi
            TARGET="$1"
            TARGET_SET=1
            shift
            ;;
    esac
done

if [ -z "$PLATFORM" ]; then
    echo "Error: Choose exactly one of --claude, --codex, or --all." >&2
    print_help >&2
    exit 2
fi

if [ "$MODE" != "local" ] && [ "$TARGET_SET" -eq 1 ]; then
    echo "Error: A target directory is valid only with --local." >&2
    exit 2
fi

if [ "$MODE" = "global" ] && { [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; } &&
   [ -n "${CLAUDE_CONFIG_DIR:-}" ] && [[ "$CLAUDE_CONFIG_DIR" != /* ]]; then
    echo "Error: CLAUDE_CONFIG_DIR must be an absolute path." >&2
    exit 2
fi

SCRIPT_DIR=""
REPO_ROOT=""
LOCAL_SKILL_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
    if [ -n "$SCRIPT_DIR" ]; then
        REPO_ROOT="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd || echo "")"
        LOCAL_SKILL_DIR="$REPO_ROOT/skills/econ-write"
    fi
fi

# Check if running from local repo or via curl | bash
is_local() {
    [ -n "$LOCAL_SKILL_DIR" ] && [ -d "$LOCAL_SKILL_DIR" ]
}

validate_source_dir() {
    local source_dir="$1"
    local file

    for file in "${SKILL_FILES[@]}"; do
        if [ ! -f "$source_dir/$file" ] || [ -L "$source_dir/$file" ] || [ ! -s "$source_dir/$file" ]; then
            echo "Error: Source is incomplete: skills/econ-write/$file" >&2
            return 1
        fi
    done
}

cleanup_source() {
    if [ -n "$SOURCE_STAGE_ROOT" ] && [ -d "$SOURCE_STAGE_ROOT" ]; then
        rm -rf "$SOURCE_STAGE_ROOT"
    fi
}

trap cleanup_source EXIT

prepare_source() {
    local archive
    local listing
    local extracted
    local skill_member
    local archive_root
    local file
    local member

    if is_local; then
        SOURCE_SKILL_DIR="$LOCAL_SKILL_DIR"
        validate_source_dir "$SOURCE_SKILL_DIR"
        return
    fi

    if ! command -v curl >/dev/null 2>&1; then
        echo "Error: curl is required for a remote installation." >&2
        return 1
    fi
    if ! command -v tar >/dev/null 2>&1; then
        echo "Error: tar is required for a remote installation." >&2
        return 1
    fi

    SOURCE_STAGE_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/econ-write-source.XXXXXX")"
    archive="$SOURCE_STAGE_ROOT/source.tar.gz"
    listing="$SOURCE_STAGE_ROOT/archive-members.txt"
    extracted="$SOURCE_STAGE_ROOT/skill"
    mkdir -p "$extracted"

    if ! curl -fsSL "$REPO_ARCHIVE_URL" -o "$archive"; then
        echo "Error: Failed to download the Econ Write source snapshot; existing installations were not changed." >&2
        return 1
    fi
    if ! tar -tzf "$archive" > "$listing"; then
        echo "Error: Failed to inspect the Econ Write source snapshot; existing installations were not changed." >&2
        return 1
    fi

    skill_member="$(grep -E '^[A-Za-z0-9._-]+/skills/econ-write/SKILL\.md$' "$listing" || true)"
    if [ -z "$skill_member" ] || [ "$(printf '%s\n' "$skill_member" | wc -l | tr -d ' ')" -ne 1 ]; then
        echo "Error: The source snapshot does not contain skills/econ-write; existing installations were not changed." >&2
        return 1
    fi
    archive_root="${skill_member%/skills/econ-write/SKILL.md}"
    case "$archive_root" in
        ""|.|..|-*|*/*)
            echo "Error: The source snapshot has an unsafe archive root; existing installations were not changed." >&2
            return 1
            ;;
    esac

    for file in "${SKILL_FILES[@]}"; do
        member="$archive_root/skills/econ-write/$file"
        if [ "$(grep -Fxc "$member" "$listing" || true)" -ne 1 ]; then
            echo "Error: The source snapshot has a missing or duplicate $file; existing installations were not changed." >&2
            return 1
        fi
    done

    if ! tar -xzf "$archive" -C "$extracted" --strip-components=3 -- \
        "$archive_root/skills/econ-write/SKILL.md" \
        "$archive_root/skills/econ-write/identification-strategies.md" \
        "$archive_root/skills/econ-write/latex-tips.md" \
        "$archive_root/skills/econ-write/review-checklist.md" \
        "$archive_root/skills/econ-write/specialized-tasks.md"; then
        echo "Error: Failed to extract the Econ Write source snapshot; existing installations were not changed." >&2
        return 1
    fi
    SOURCE_SKILL_DIR="$extracted"
    validate_source_dir "$SOURCE_SKILL_DIR"
}

backup_name() {
    printf '%s' "$1" | sed 's#[^A-Za-z0-9._-]#_#g' | awk '{ print substr($0, length($0) > 180 ? length($0) - 179 : 1) }'
}

paths_overlap() {
    python3 - "$1" "$2" <<'PY'
import os
import sys
from pathlib import Path

try:
    if os.path.samefile(sys.argv[1], sys.argv[2]):
        raise SystemExit(0)
except OSError:
    pass

def forms(raw):
    path = Path(raw).expanduser()
    return {
        os.path.normcase(os.path.normpath(str(path.absolute()))),
        os.path.normcase(os.path.normpath(str(path.resolve(strict=False)))),
    }

def overlaps(left, right):
    try:
        common = os.path.commonpath((left, right))
    except (OSError, ValueError):
        return False
    return common in {left, right}

raise SystemExit(
    0
    if any(overlaps(left, right) for left in forms(sys.argv[1]) for right in forms(sys.argv[2]))
    else 1
)
PY
}

skill_destination_is_safe() {
    python3 - "$1" "$HOME" <<'PY'
import os
import stat
import sys
from pathlib import Path

destination = Path(os.path.abspath(os.path.expanduser(sys.argv[1])))
home = Path(os.path.abspath(os.path.expanduser(sys.argv[2])))
try:
    boundary = Path(os.path.commonpath((str(home), str(destination.parent))))
except ValueError:
    boundary = Path(destination.anchor)
candidate = boundary
for part in destination.parent.relative_to(boundary).parts:
    candidate = candidate / part
    try:
        metadata = candidate.lstat()
    except OSError:
        continue
    attributes = getattr(metadata, "st_file_attributes", 0)
    if (
        stat.S_ISLNK(metadata.st_mode)
        or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
        or not stat.S_ISDIR(metadata.st_mode)
    ):
        print(candidate)
        raise SystemExit(1)
PY
}

legacy_parent_is_safe() {
    python3 - "$1" "$2" <<'PY'
import os
import stat
import sys
from pathlib import Path

legacy = Path(os.path.abspath(os.path.expanduser(sys.argv[1])))
boundary = Path(os.path.abspath(os.path.expanduser(sys.argv[2])))
try:
    legacy.parent.relative_to(boundary)
except ValueError:
    print(legacy.parent)
    raise SystemExit(1)
path = legacy.parent
while True:
    try:
        metadata = path.lstat()
    except OSError:
        pass
    else:
        attributes = getattr(metadata, "st_file_attributes", 0)
        if stat.S_ISLNK(metadata.st_mode) or attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            print(path)
            raise SystemExit(1)
    if path == boundary:
        break
    if boundary not in path.parents:
        print(path)
        raise SystemExit(1)
    path = path.parent
PY
}

preserve_copy() {
    local source_path="$1"
    local original_path="$2"
    local name
    local path_hash
    local original_parent
    local client_root
    local central_backup
    local local_backup

    name="$(backup_name "$original_path")"
    path_hash="$(python3 - "$original_path" <<'PY'
import hashlib
import sys

print(hashlib.sha256(sys.argv[1].encode("utf-8")).hexdigest()[:12])
PY
    )"
    name="$name-$path_hash"
    central_backup="$BACKUP_ROOT/$name"
    if skill_destination_is_safe "$central_backup"; then
        if mkdir -p "$BACKUP_ROOT" && mv "$source_path" "$central_backup"; then
            BACKUPS_CREATED=1
            echo "  Preserved previous copy: $central_backup"
            return 0
        fi
    fi

    original_parent="$(dirname "$original_path")"
    if [ "$(basename "$original_parent")" != "skills" ]; then
        return 1
    fi
    client_root="$(dirname "$original_parent")"
    local_backup="$client_root/.openeconai-inactive/econ-write/$RUN_ID/$name"
    if ! skill_destination_is_safe "$local_backup"; then
        return 1
    fi
    mkdir -p "$(dirname "$local_backup")" || return 1
    if mv "$source_path" "$local_backup"; then
        BACKUPS_CREATED=1
        echo "  Preserved previous copy on its original volume: $local_backup"
        return 0
    fi

    echo "  Warning: Could not move the previous copy to $BACKUP_ROOT/$name"
    echo "  Previous copy remains at: $source_path"
    return 1
}

install_skill() {
    local dest_dir="$1"
    local label="$2"
    local parent_dir
    local stage_root
    local stage_dir
    local previous_dir

    if ! skill_destination_is_safe "$dest_dir"; then
        echo "  Error: Refusing an unsafe $label destination ancestor: $dest_dir" >&2
        return 1
    fi

    parent_dir="$(dirname "$dest_dir")"
    mkdir -p "$parent_dir"
    stage_root="$(mktemp -d "$parent_dir/.econ-write-install.XXXXXX")"
    stage_dir="$stage_root/econ-write"
    previous_dir="$stage_root/previous"
    mkdir -p "$stage_dir"

    for file in "${SKILL_FILES[@]}"; do
        if ! cp "$SOURCE_SKILL_DIR/$file" "$stage_dir/$file"; then
            echo "  Error: Failed to stage $file"
            rm -rf "$stage_root"
            return 1
        fi

        if [ ! -s "$stage_dir/$file" ]; then
            echo "  Error: $file is empty; the existing installation was not changed."
            rm -rf "$stage_root"
            return 1
        fi
    done

    if [ ! -L "$dest_dir" ] && [ -d "$dest_dir" ] && diff -qr "$dest_dir" "$stage_dir" >/dev/null 2>&1; then
        rm -rf "$stage_root"
        echo "  Already current for $label: $dest_dir/"
        return 0
    fi

    if [ -e "$dest_dir" ] || [ -L "$dest_dir" ]; then
        if ! mv "$dest_dir" "$previous_dir"; then
            echo "  Error: Could not stage the previous installation at $dest_dir"
            rm -rf "$stage_root"
            return 1
        fi
    fi

    if ! mv "$stage_dir" "$dest_dir"; then
        echo "  Error: Could not activate the staged installation at $dest_dir"
        if [ -e "$previous_dir" ] || [ -L "$previous_dir" ]; then
            if ! mv "$previous_dir" "$dest_dir"; then
                echo "  Error: Could not restore the previous installation. It remains available at: $previous_dir" >&2
                return 1
            fi
        fi
        rm -rf "$stage_root"
        return 1
    fi

    if [ -e "$previous_dir" ] || [ -L "$previous_dir" ]; then
        if ! preserve_copy "$previous_dir" "$dest_dir"; then
            echo "  Error: The update could not preserve the previous installation; restoring it."
            if ! rm -rf "$dest_dir" || ! mv "$previous_dir" "$dest_dir"; then
                echo "  Error: Automatic restoration failed. The previous installation remains available at: $previous_dir" >&2
                return 1
            fi
            rm -rf "$stage_root"
            return 1
        fi
    fi
    rm -rf "$stage_root"
    echo "  Installed for $label: $dest_dir/"
}

deactivate_legacy_codex_copy() {
    local current_dir="$1"
    local legacy_dir="$2"
    local boundary="$3"

    if [ -L "$current_dir" ] || [ ! -d "$current_dir" ] ||
       ! diff -qr "$current_dir" "$SOURCE_SKILL_DIR" >/dev/null 2>&1; then
        echo "  Error: The current Codex skill could not be verified before legacy cleanup: $current_dir" >&2
        return 1
    fi

    if [ ! -e "$legacy_dir" ] && [ ! -L "$legacy_dir" ]; then
        return 0
    fi

    if paths_overlap "$current_dir" "$legacy_dir"; then
        echo "  Skipped aliased legacy Codex path that resolves to the current skill: $legacy_dir"
        return 0
    fi
    if ! legacy_parent_is_safe "$legacy_dir" "$boundary"; then
        echo "  Error: Refusing legacy migration through a linked or junction ancestor: $legacy_dir" >&2
        return 1
    fi

    if [ ! -L "$legacy_dir" ] && [ -d "$legacy_dir" ] && diff -qr "$legacy_dir" "$current_dir" >/dev/null 2>&1; then
        rm -rf "$legacy_dir"
        echo "  Removed duplicate legacy Codex copy: $legacy_dir/"
    elif ! preserve_copy "$legacy_dir" "$legacy_dir"; then
        echo "  Error: Could not deactivate the modified legacy Codex copy."
        return 1
    fi

    if [ -L "$current_dir" ] || [ ! -d "$current_dir" ] ||
       ! diff -qr "$current_dir" "$SOURCE_SKILL_DIR" >/dev/null 2>&1; then
        echo "  Error: The current Codex skill changed during legacy cleanup: $current_dir" >&2
        return 1
    fi
}

prepare_source

echo ""
echo "  Econ Writing Skill Installer"
echo "  =============================="
echo ""

if [ "$MODE" = "global" ]; then
    echo "  Mode: Global (available in all projects)"
    echo ""

    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
        install_skill "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/econ-write" "Claude Code (global)"
    fi
    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
        install_skill "$HOME/.agents/skills/econ-write" "Codex (global)"
        deactivate_legacy_codex_copy \
            "$HOME/.agents/skills/econ-write" \
            "$HOME/.codex/skills/econ-write" \
            "$HOME"
    fi

    echo ""
    echo "  Done! The skill is now available across all your projects."

elif [ "$MODE" = "local" ]; then
    TARGET="${TARGET:-.}"
    echo "  Mode: Local (project: $TARGET)"
    echo ""

    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
        install_skill "$TARGET/.claude/skills/econ-write" "Claude Code (local)"
    fi
    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
        install_skill "$TARGET/.agents/skills/econ-write" "Codex (local)"
        deactivate_legacy_codex_copy \
            "$TARGET/.agents/skills/econ-write" \
            "$TARGET/.codex/skills/econ-write" \
            "$TARGET"
    fi

    echo ""
    echo "  Done! The skill is installed in: $TARGET"
fi

if [ "$BACKUPS_CREATED" -eq 1 ]; then
    echo "  Previous copies were preserved at the paths reported above."
fi

echo ""
echo "  Usage:"
if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
    echo "    Claude Code: /econ-write rewrite this economics paper introduction"
fi
if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
    echo '    Codex: $econ-write rewrite this economics paper introduction'
fi
echo ""
