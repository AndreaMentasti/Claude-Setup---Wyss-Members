#!/bin/bash
# Block accidental edits to protected files and directories
# Customize PROTECTED_PATTERNS and PROTECTED_DIRS below for your project
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
FILE=""

# Extract file path based on tool type
if [ "$TOOL" = "Edit" ] || [ "$TOOL" = "Write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
fi

# No file path = not a file operation, allow
if [ -z "$FILE" ]; then
  exit 0
fi

# ============================================================
# CUSTOMIZE: Add patterns for files you want to protect
# Uses basename matching — add full paths for more precision
# ============================================================
PROTECTED_PATTERNS=(
  "settings.json"
)

# ============================================================
# CUSTOMIZE: Add directory path fragments to protect entire folders
# Any file whose path contains one of these strings is blocked
# ============================================================
PROTECTED_DIRS=(
  "/rawdata/"
  "\\rawdata\\"
  "/Dropbox/populism_and_narratives/data/rawdata/"
  "\\Dropbox\\populism_and_narratives\\data\\rawdata\\"
)

# Check basename patterns
BASENAME=$(basename "$FILE")
for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$BASENAME" == "$PATTERN" ]]; then
    echo "🔒 Protected file: $BASENAME — raw data must never be overwritten." >&2
    echo "   Edit .claude/hooks/protect-files.sh to change protection." >&2
    exit 2
  fi
done

# Check directory patterns
for DIR in "${PROTECTED_DIRS[@]}"; do
  if [[ "$FILE" == *"$DIR"* ]]; then
    echo "🔒 Protected directory: $FILE is inside rawdata/ — never overwrite raw data." >&2
    echo "   Edit .claude/hooks/protect-files.sh to change protection." >&2
    exit 2
  fi
done

exit 0
