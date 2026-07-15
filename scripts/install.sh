#!/bin/bash
# Install Econ Writing Skill for Claude Code and/or Codex
#
# Usage:
#   ./scripts/install.sh              Install globally (default, all platforms)
#   ./scripts/install.sh --local      Install to current project only
#   ./scripts/install.sh --claude     Install for Claude Code only
#   ./scripts/install.sh --codex      Install for Codex only
#   ./scripts/install.sh --help       Show help
#
# One-line install (no git clone needed):
#   curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main"
SKILL_FILES=("SKILL.md" "identification-strategies.md" "latex-tips.md" "review-checklist.md" "specialized-tasks.md")
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
BACKUP_ROOT="$HOME/.openeconai/backups/econ-write/$RUN_ID"
BACKUPS_CREATED=0

# Parse arguments
MODE="global"
PLATFORM="all"
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
    echo "  --all        Install for all supported platforms (default)"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./scripts/install.sh                          # Global install, all platforms"
    echo "  ./scripts/install.sh --local .                 # Install to current project"
    echo "  ./scripts/install.sh --local /path/to/project  # Install to specific project"
    echo "  ./scripts/install.sh --global --claude         # Global install, Claude Code only"
    echo ""
    echo "One-line install (no git clone needed):"
    echo "  curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/scripts/install.sh | bash"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --global) MODE="global"; shift ;;
        --local)  MODE="local"; shift ;;
        --claude) PLATFORM="claude"; shift ;;
        --codex)  PLATFORM="codex"; shift ;;
        --all)    PLATFORM="all"; shift ;;
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

if [ "$MODE" != "local" ] && [ "$TARGET_SET" -eq 1 ]; then
    echo "Error: A target directory is valid only with --local." >&2
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

validate_local_source() {
    local file

    if ! is_local; then
        return 0
    fi

    for file in "${SKILL_FILES[@]}"; do
        if [ ! -s "$LOCAL_SKILL_DIR/$file" ]; then
            echo "Error: Local source is incomplete: skills/econ-write/$file" >&2
            return 1
        fi
    done
}

backup_name() {
    printf '%s' "$1" | sed 's#[^A-Za-z0-9._-]#_#g'
}

preserve_copy() {
    local source_path="$1"
    local original_path="$2"
    local name

    name="$(backup_name "$original_path")"
    mkdir -p "$BACKUP_ROOT"
    if mv "$source_path" "$BACKUP_ROOT/$name"; then
        BACKUPS_CREATED=1
        echo "  Preserved previous copy: $BACKUP_ROOT/$name"
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

    parent_dir="$(dirname "$dest_dir")"
    mkdir -p "$parent_dir"
    stage_root="$(mktemp -d "$parent_dir/.econ-write-install.XXXXXX")"
    stage_dir="$stage_root/econ-write"
    previous_dir="$stage_root/previous"
    mkdir -p "$stage_dir"

    for file in "${SKILL_FILES[@]}"; do
        if is_local; then
            if ! cp "$LOCAL_SKILL_DIR/$file" "$stage_dir/$file"; then
                echo "  Error: Failed to stage $file"
                rm -rf "$stage_root"
                return 1
            fi
        else
            if ! curl -fsSL "$REPO_URL/skills/econ-write/$file" -o "$stage_dir/$file" 2>/dev/null; then
                echo "  Error: Failed to download $file; the existing installation was not changed."
                rm -rf "$stage_root"
                return 1
            fi
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
            mv "$previous_dir" "$dest_dir" || true
        fi
        rm -rf "$stage_root"
        return 1
    fi

    if [ -e "$previous_dir" ] || [ -L "$previous_dir" ]; then
        if ! preserve_copy "$previous_dir" "$dest_dir"; then
            echo "  Error: The update could not preserve the previous installation; restoring it."
            rm -rf "$dest_dir"
            mv "$previous_dir" "$dest_dir" || true
            rm -rf "$stage_root"
            return 1
        fi
    fi
    rm -rf "$stage_root"
    echo "  Installed for $label: $dest_dir/"
}

deactivate_legacy_codex_copy() {
    local current_dir="$HOME/.agents/skills/econ-write"
    local legacy_dir="$HOME/.codex/skills/econ-write"

    if [ ! -e "$legacy_dir" ] && [ ! -L "$legacy_dir" ]; then
        return 0
    fi

    if [ ! -L "$legacy_dir" ] && [ -d "$legacy_dir" ] && diff -qr "$legacy_dir" "$current_dir" >/dev/null 2>&1; then
        rm -rf "$legacy_dir"
        echo "  Removed duplicate legacy Codex copy: $legacy_dir/"
        return 0
    fi

    if ! preserve_copy "$legacy_dir" "$legacy_dir"; then
        echo "  Error: Could not deactivate the modified legacy Codex copy."
        return 1
    fi
}

validate_local_source

echo ""
echo "  Econ Writing Skill Installer"
echo "  =============================="
echo ""

if [ "$MODE" = "global" ]; then
    echo "  Mode: Global (available in all projects)"
    echo ""

    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
        install_skill "$HOME/.claude/skills/econ-write" "Claude Code (global)"
    fi
    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
        install_skill "$HOME/.agents/skills/econ-write" "Codex (global)"
        deactivate_legacy_codex_copy
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
    fi

    echo ""
    echo "  Done! The skill is installed in: $TARGET"
fi

if [ "$BACKUPS_CREATED" -eq 1 ]; then
    echo "  Backups: $BACKUP_ROOT/"
fi

echo ""
echo "  Usage:"
echo "    /econ-write write introduction for my paper on minimum wage"
echo "    /econ-write rewrite this abstract for clarity"
echo "    /econ-write draft conclusion for my RCT paper on cash transfers"
echo "    /econ-write review my results section for style violations"
echo ""
