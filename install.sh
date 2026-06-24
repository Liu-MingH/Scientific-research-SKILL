#!/usr/bin/env bash
# Science Vibe Coding — Universal Installer
# Detects your AI coding tool and installs the rules file.
#
# Usage:
#   curl -sLk https://raw.githubusercontent.com/Liu-MingH/Scientific-research-SKILL/main/install.sh | bash
#   or: bash install.sh [target_directory]

set -e

REPO_URL="https://raw.githubusercontent.com/Liu-MingH/Scientific-research-SKILL/main/SKILL.md"
TARGET_DIR="${1:-.}"

echo "Science Vibe Coding — Installer"
echo "================================"

# Download the source file
TMPFILE=$(mktemp)
if command -v curl &>/dev/null; then
    curl -sLk "$REPO_URL" -o "$TMPFILE"
elif command -v wget &>/dev/null; then
    wget -qO "$TMPFILE" "$REPO_URL"
else
    echo "Error: Neither curl nor wget found. Install one and retry."
    exit 1
fi

if [ ! -s "$TMPFILE" ]; then
    echo "Error: Failed to download SKILL.md from GitHub."
    echo "Try manually: https://github.com/Liu-MingH/Scientific-research-SKILL"
    exit 1
fi

echo "Downloaded SKILL.md ($(wc -c < "$TMPFILE") bytes)"
echo ""

# Detect and install — project-local indicators take priority over global commands
INSTALLED=0

if [ -d "$TARGET_DIR/.cursor" ] || [ -f "$TARGET_DIR/.cursorrules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.cursorrules"
    echo "✅ Installed as .cursorrules (Cursor)"
    INSTALLED=1

elif [ -d "$TARGET_DIR/.claude" ]; then
    cp "$TMPFILE" "$TARGET_DIR/CLAUDE.md"
    echo "✅ Installed as CLAUDE.md (Claude Code)"
    INSTALLED=1

elif [ -d "$TARGET_DIR/.codeium" ] || [ -f "$TARGET_DIR/.windsurfrules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.windsurfrules"
    echo "✅ Installed as .windsurfrules (Windsurf)"
    INSTALLED=1

elif [ -f "$TARGET_DIR/.clinerules" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.clinerules"
    echo "✅ Installed as .clinerules (Cline)"
    INSTALLED=1

elif [ -d "$TARGET_DIR/.github" ]; then
    cp "$TMPFILE" "$TARGET_DIR/.github/copilot-instructions.md"
    echo "✅ Installed as .github/copilot-instructions.md (Copilot)"
    INSTALLED=1
fi

# Fallback: no project-local indicator found, try global commands
if [ "$INSTALLED" -eq 0 ]; then
    if command -v claude &>/dev/null; then
        cp "$TMPFILE" "$TARGET_DIR/CLAUDE.md"
        echo "✅ Installed as CLAUDE.md (Claude Code)"
        INSTALLED=1
    elif command -v gh &>/dev/null; then
        mkdir -p "$TARGET_DIR/.github"
        cp "$TMPFILE" "$TARGET_DIR/.github/copilot-instructions.md"
        echo "✅ Installed as .github/copilot-instructions.md (Copilot)"
        INSTALLED=1
    fi
fi

# Fallback
if [ "$INSTALLED" -eq 0 ]; then
    cp "$TMPFILE" "$TARGET_DIR/CLAUDE.md"
    echo "✅ Installed as CLAUDE.md (default)"
    echo ""
    echo "No AI tool auto-detected. Installed as CLAUDE.md."
    echo "To use with other tools:"
    echo "  cp CLAUDE.md .cursorrules        # Cursor"
    echo "  cp CLAUDE.md .windsurfrules      # Windsurf"
    echo "  cp CLAUDE.md .clinerules         # Cline"
fi

rm -f "$TMPFILE"

echo ""
echo "Done! Open your project in your AI coding tool to activate."
