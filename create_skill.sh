#!/bin/bash

SKILL_NAME="3gpp_support"

echo "Building skill package for: $SKILL_NAME"

# Clean up previous build if exists
rm -rf "$SKILL_NAME"
rm -f "${SKILL_NAME}.skill"

# Create the main skill directory
mkdir -p "$SKILL_NAME/scripts"
mkdir -p "$SKILL_NAME/references"
mkdir -p "$SKILL_NAME/assets"

# Copy python scripts
cp 3gpp_spec_scope_spider.py "$SKILL_NAME/scripts/"
cp download_3gpp_docs.py "$SKILL_NAME/scripts/"

# Copy documentations
cp doc/3gpp_download_tool_guide.md "$SKILL_NAME/references/"
cp doc/3gpp_scope_spider_guide.md "$SKILL_NAME/references/"

# Copy the required SKILL.md file from doc folder
cp doc/SKILL.md "$SKILL_NAME/SKILL.md"

# Check if zip is installed
if ! command -v zip &> /dev/null; then
    echo "Error: 'zip' command is not installed. Please install 'zip' to package the skill."
    exit 1
fi

# Create a zip archive with .skill extension (standard format for cross-platform imports)
echo "Packaging into ${SKILL_NAME}.skill (zip format)..."
zip -r "${SKILL_NAME}.skill" "$SKILL_NAME" > /dev/null

echo "Done! The skill package ${SKILL_NAME}.skill has been generated."
