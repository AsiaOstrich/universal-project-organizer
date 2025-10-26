#!/bin/bash
#
# List all available Claude Skills
#
# This script shows:
# 1. Personal Skills (global, in ~/.claude/skills/)
# 2. Project Skills (in .claude/skills/)
# 3. Marketplace Skills (available in marketplaces)
#

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           Claude Skills Installation Summary                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Personal Skills (Global)
echo "📦 Personal Skills (Global - ~/.claude/skills/)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d ~/.claude/skills ] && [ "$(ls -A ~/.claude/skills 2>/dev/null)" ]; then
    for skill in ~/.claude/skills/*/; do
        if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            if [ -f "$skill/SKILL.md" ]; then
                # Extract description from YAML frontmatter
                desc=$(sed -n '/^description:/,/^---/p' "$skill/SKILL.md" | grep "^description:" | sed 's/^description: *//')
                echo "  ✓ $skill_name"
                [ -n "$desc" ] && echo "    └─ $desc"
            else
                echo "  ⚠ $skill_name (missing SKILL.md)"
            fi
        fi
    done
else
    echo "  (none installed)"
fi
echo ""

# Project Skills (Local)
echo "🏗️  Project Skills (Local - .claude/skills/)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d .claude/skills ] && [ "$(ls -A .claude/skills 2>/dev/null)" ]; then
    for skill in .claude/skills/*/; do
        if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            if [ -f "$skill/SKILL.md" ]; then
                desc=$(sed -n '/^description:/,/^---/p' "$skill/SKILL.md" | grep "^description:" | sed 's/^description: *//')
                echo "  ✓ $skill_name"
                [ -n "$desc" ] && echo "    └─ $desc"
            else
                echo "  ⚠ $skill_name (missing SKILL.md)"
            fi
        fi
    done
else
    echo "  (none installed)"
fi
echo ""

# Marketplace Skills
echo "🛒 Available in Marketplaces"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d ~/.claude/plugins/marketplaces ]; then
    for marketplace in ~/.claude/plugins/marketplaces/*/; do
        if [ -d "$marketplace" ]; then
            marketplace_name=$(basename "$marketplace")
            echo "  📚 Marketplace: $marketplace_name"

            # Find all SKILL.md files
            skill_count=0
            while IFS= read -r skill_file; do
                skill_dir=$(dirname "$skill_file")
                skill_name=$(basename "$skill_dir")

                # Skip if it's directly in marketplace root
                if [ "$skill_dir" != "$marketplace" ]; then
                    desc=$(sed -n '/^description:/,/^---/p' "$skill_file" | grep "^description:" | sed 's/^description: *//' | head -c 80)
                    echo "     • $skill_name"
                    [ -n "$desc" ] && echo "       └─ $desc..."
                    ((skill_count++))
                fi
            done < <(find "$marketplace" -name "SKILL.md" -type f)

            echo "     (Total: $skill_count skills available)"
            echo ""
        fi
    done
else
    echo "  (no marketplaces configured)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 Tips:"
echo "  • Ask Claude: 'What skills are available?'"
echo "  • Install personal skill: Copy skill folder to ~/.claude/skills/"
echo "  • Add project skill: Copy skill folder to .claude/skills/"
echo "  • Manage marketplaces: claude plugin marketplace --help"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"