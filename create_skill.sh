#!/bin/bash

# Check if a skill name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <skill-name>"
  exit 1
fi

SKILL_NAME=$1

# Create the main skill directory
mkdir -p "$SKILL_NAME"

# Create the required SKILL.md file with basic frontmatter
cat <<EOF > "$SKILL_NAME/SKILL.md"
---
name: $SKILL_NAME
description: Enter a single-line description of the skill here.
---

# $SKILL_NAME

## Overview
Describe the skill here.

## Instructions
Write instructions for using the skill here.
EOF

# Create optional resource directories based on Gemini CLI Skill standards
mkdir -p "$SKILL_NAME/scripts"
mkdir -p "$SKILL_NAME/references"
mkdir -p "$SKILL_NAME/assets"

echo "Created skill directory structure for: $SKILL_NAME"
echo ""
echo "Structure created:"
echo "$SKILL_NAME/"
echo "├── SKILL.md"
echo "├── scripts/      - For executable code (Node.js/Python/Bash/etc.)"
echo "├── references/   - For documentation intended to be loaded into context"
echo "└── assets/       - For files used in output (templates, icons, fonts, etc.)"
