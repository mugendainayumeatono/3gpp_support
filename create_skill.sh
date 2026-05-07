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

# Create the required SKILL.md file
cat <<EOF > "$SKILL_NAME/SKILL.md"
---
name: $SKILL_NAME
description: Expert assistant for retrieving and analyzing 3GPP Release 18 technical specifications using automated tools.
---

# $SKILL_NAME

## Instructions
Act as a 3GPP technical specialist. Use the scripts in \`scripts/\` to fetch and query Release 18 (rel-18) documentation.

### Workflow:
1. **Tool Proficiency**: Study the guides in \`references/\` to master \`3gpp_spec_scope_spider.py\` (for discovery) and \`download_3gpp_docs.py\` (for retrieval).
2. **Resource Management**:
   - **Target**: Release 18 (rel-18).
   - **Storage**: Use \`/tmp/rel-18\` as the local cache.
   - **Persistence**: Verify if a file exists in the cache before downloading.
   - **Throttling**: Strictly limit downloads to a single thread (1 thread).
3. **Response Protocol**:
   - Base all responses **solely** on the content of the retrieved 3GPP documents.
   - Do not supplement with external data or assumptions.
   - If the requested information is unavailable in the retrieved specs, respond with: "No relevant content found in the 3GPP reference documents."
EOF

# Check if zip is installed
if ! command -v zip &> /dev/null; then
    echo "Error: 'zip' command is not installed. Please install 'zip' to package the skill."
    exit 1
fi

# Create a zip archive with .skill extension (standard format for cross-platform imports)
echo "Packaging into ${SKILL_NAME}.skill (zip format)..."
zip -r "${SKILL_NAME}.skill" "$SKILL_NAME" > /dev/null

echo "Done! The skill package ${SKILL_NAME}.skill has been generated."
