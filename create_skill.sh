#!/bin/bash

GENERATE_SKILL=1

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -s|--skip-gen) GENERATE_SKILL=0; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done

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

# Handle SKILL.md
if [ "$GENERATE_SKILL" -eq 1 ]; then
    echo "Generating new SKILL.md..."
    
    # Keep up to 2 historical versions
    if [ -f "doc/SKILL.md" ]; then
        if [ -f "doc/SKILL.md.1" ]; then
            mv -f "doc/SKILL.md.1" "doc/SKILL.md.2"
        fi
        cp "doc/SKILL.md" "doc/SKILL.md.1"
    fi

    ./generate_SKILL-md.sh
    if [ $? -ne 0 ]; then
        echo "Error: Failed to generate SKILL.md"
        exit 1
    fi
else
    echo "Using existing SKILL.md (skipping generation)..."
    if [ ! -f "doc/SKILL.md" ]; then
        echo "Error: doc/SKILL.md not found. Cannot skip generation if the file does not exist."
        exit 1
    fi
fi

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
