#!/usr/bin/env bash
# Science Vibe Coding — Universal Installer
# Detects your AI coding tool and installs the rules file.
#
# Usage:
#   curl -sL https://raw.githubusercontent.com/Liu-MingH/Scientific-research-SKILL/main/install.sh | bash
#   or: bash install.sh [target_directory]

set -e

REPO_URL="https://raw.githubusercontent.com/Liu-MingH/Scientific-research-SKILL/main/SKILL.md"
TARGET_DIR="${1:-.}"

echo "Science Vibe Coding — Installer"
echo "================================"
echo ""

# Download the source file
TMPFILE=$(mktemp)
curl -sL "$REPO_URL" -o "$TMPFILE" 2>/dev/null || wget -qO "$TMPFILE" "$REPO_URL" 2>/dev/null

if [ ! -s "$TMPFILE" ]; then
    echo "Error: Failed to download SKILL.md"
    exit 1
fi

# Detect and install
INSTALLED=0

# Claude Code
if [ -d "$TARGET_DIR/.claude" ] || command -v claude &>/dev/null; then
    cp "$TMPFILE" "$TARGET_DIR/CLAUDE.md"
    echo "✅ Installed as CLAUDE.md (Claude Code)"
    INSTALLED=1
fi

# Cursor
if [ -d "$TARGET_DIR/.cursor" ] || [ -f "$TARGET_DIR/.cursorrules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.cursorrules"
    echo "✅ Installed as .cursorrules (Cursor)"
    INSTALLED=1
fi

# Windsurf / Codeium
if [ -d "$TARGET_DIR/.codeium" ] || [ -f "$TARGET_DIR/.windsurfrules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.windsurfrules"
    echo "✅ Installed as .windsurfrules (Windsurf)"
    INSTALLED=1
fi

# Copilot
if [ -d "$TARGET_DIR/.github" ] || command -v gh &>/dev/null; then
    mkdir -p "$TARGET_DIR/.github"
    cp "$TMPFILE" "$TARGET_DIR/.github/copilot-instructions.md"
    echo "✅ Installed as .github/copilot-instructions.md (Copilot)"
    INSTALLED=1
fi

# Cline
if [ -f "$TARGET_DIR/.clinerules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.clinerules"
    echo "✅ Installed as .clinerules (Cline)"
    INSTALLED=1
fi

# Fallback: no tool detected
if [ "$INSTALLED" -eq 0 ]; then
    cp "$TMPFILE" "$TARGET_DIR/CLAUDE.md"
    echo "✅ Installed as CLAUDE.md (default)"
    echo ""
    echo "No AI tool detected. Installed as CLAUDE.md."
    echo "To use with other tools, copy manually:"
    echo "  cp CLAUDE.md .cursorrules        # Cursor"
    echo "  cp CLAUDE.md .windsurfrules      # Windsurf"
    echo "  cp CLAUDE.md .clinerules         # Cline"
fi

rm -f "$TMPFILE"

echo ""
echo "Done! Open your project in your AI coding tool to activate."
