#!/bin/bash
# Install Econ Writing Skill for Claude Code and/or Codex
#
# Usage:
#   ./install.sh              Install globally (default, all platforms)
#   ./install.sh --local      Install to current project only
#   ./install.sh --claude     Install for Claude Code only
#   ./install.sh --codex      Install for Codex only
#   ./install.sh --help       Show help
#
# One-line install (no git clone needed):
#   curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main"
SKILL_FILES=("SKILL.md" "identification-strategies.md")

# Parse arguments
MODE="global"
PLATFORM="all"
TARGET=""

print_help() {
    echo "Econ Writing Skill Installer"
    echo ""
    echo "Usage: ./install.sh [options] [target-directory]"
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
    echo "  ./install.sh                          # Global install, all platforms"
    echo "  ./install.sh --local .                 # Install to current project"
    echo "  ./install.sh --local /path/to/project  # Install to specific project"
    echo "  ./install.sh --global --claude         # Global install, Claude Code only"
    echo ""
    echo "One-line install (no git clone needed):"
    echo "  curl -fsSL https://raw.githubusercontent.com/hanlulong/econ-writing-skill/main/install.sh | bash"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --global) MODE="global"; shift ;;
        --local)  MODE="local"; shift ;;
        --claude) PLATFORM="claude"; shift ;;
        --codex)  PLATFORM="codex"; shift ;;
        --all)    PLATFORM="all"; shift ;;
        --help)   print_help; exit 0 ;;
        *)        TARGET="$1"; shift ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"

# Check if running from local repo or via curl | bash
is_local() {
    [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/.claude/skills/econ-write/SKILL.md" ]
}

install_skill() {
    local dest_dir="$1"
    local label="$2"
    local source_dir="$3"

    mkdir -p "$dest_dir"

    for file in "${SKILL_FILES[@]}"; do
        if is_local && [ -f "$source_dir/$file" ]; then
            cp "$source_dir/$file" "$dest_dir/$file"
        else
            # Download from GitHub
            if curl -fsSL "$REPO_URL/.claude/skills/econ-write/$file" -o "$dest_dir/$file" 2>/dev/null; then
                true
            else
                [ "$file" = "SKILL.md" ] && echo "  Error: Failed to download $file" && return 1
            fi
        fi
    done

    echo "  Installed for $label: $dest_dir/"
}

echo ""
echo "  Econ Writing Skill Installer"
echo "  =============================="
echo ""

if [ "$MODE" = "global" ]; then
    echo "  Mode: Global (available in all projects)"
    echo ""

    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
        install_skill "$HOME/.claude/skills/econ-write" "Claude Code (global)" "$SCRIPT_DIR/.claude/skills/econ-write"
    fi
    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
        install_skill "$HOME/.codex/skills/econ-write" "Codex (global)" "$SCRIPT_DIR/.claude/skills/econ-write"
    fi

    echo ""
    echo "  Done! The skill is now available across all your projects."

elif [ "$MODE" = "local" ]; then
    TARGET="${TARGET:-.}"
    echo "  Mode: Local (project: $TARGET)"
    echo ""

    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "claude" ]; then
        install_skill "$TARGET/.claude/skills/econ-write" "Claude Code (local)" "$SCRIPT_DIR/.claude/skills/econ-write"
    fi
    if [ "$PLATFORM" = "all" ] || [ "$PLATFORM" = "codex" ]; then
        install_skill "$TARGET/.agents/skills/econ-write" "Codex (local)" "$SCRIPT_DIR/.claude/skills/econ-write"
    fi

    echo ""
    echo "  Done! The skill is installed in: $TARGET"
fi

echo ""
echo "  Usage:"
echo "    /econ-write write introduction for my paper on minimum wage"
echo "    /econ-write rewrite this abstract for clarity"
echo "    /econ-write draft conclusion for my RCT paper on cash transfers"
echo "    /econ-write review my results section for style violations"
echo ""
