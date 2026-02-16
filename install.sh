#!/bin/bash
# Install Econ Writing Skill for Claude Code or Codex
# Usage: ./install.sh [target-project-directory]

set -e

TARGET="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing Econ Writing Skill..."
echo "Target directory: $TARGET"

# Install for Claude Code
mkdir -p "$TARGET/.claude/skills/econ-write"
cp "$SCRIPT_DIR/.claude/skills/econ-write/SKILL.md" "$TARGET/.claude/skills/econ-write/SKILL.md"
echo "  Installed for Claude Code: .claude/skills/econ-write/SKILL.md"

# Install for Codex
mkdir -p "$TARGET/.agents/skills/econ-write"
cp "$SCRIPT_DIR/.agents/skills/econ-write/SKILL.md" "$TARGET/.agents/skills/econ-write/SKILL.md"
echo "  Installed for Codex: .agents/skills/econ-write/SKILL.md"

echo ""
echo "Done! The econ-write skill is now available."
echo ""
echo "Usage in Claude Code:"
echo "  /econ-write write introduction for my paper on minimum wage"
echo "  /econ-write rewrite this abstract for clarity"
echo ""
echo "Usage in Codex:"
echo "  /econ-write draft a conclusion for my RDD paper"
