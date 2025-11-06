#!/bin/bash
# GitFam Helper Script: Create New Family Branch
# Usage: ./create-family-branch.sh "surname-location" "Description"

# Check if required arguments are provided
if [ $# -lt 1 ]; then
    echo "Usage: ./create-family-branch.sh \"family-branch-name\" \"Optional Description\""
    echo "Example: ./create-family-branch.sh \"smith-california\" \"Smith family California branch\""
    exit 1
fi

BRANCH_NAME="$1"
DESCRIPTION="${2:-$BRANCH_NAME family branch}"

# Convert to lowercase
BRANCH_NAME=$(echo "$BRANCH_NAME" | tr '[:upper:]' '[:lower:]')

BRANCH_PATH="families/${BRANCH_NAME}"

# Check if branch already exists
if [ -d "$BRANCH_PATH" ]; then
    echo "Error: Family branch already exists at $BRANCH_PATH"
    exit 1
fi

# Create directory structure
echo "Creating family branch: $BRANCH_PATH"
mkdir -p "$BRANCH_PATH/members"

# Create README
cat > "$BRANCH_PATH/README.md" << EOF
# $DESCRIPTION

## Overview

[Add a brief description of this family branch - geographical location, time period covered, key ancestors]

## Family Tree

\`\`\`
[Create a simple text-based family tree here]

Example:
├── Grandparent Name (b. 1920)
│   ├── Parent Name (b. 1945)
│   │   ├── Child Name (b. 1970)
│   │   └── Child Name (b. 1972)
│   └── Parent Name (b. 1948)
\`\`\`

## Key Locations

- [City, State/Country] (Years)
- [City, State/Country] (Years)

## Notable Events

- **[Year]**: [Description of important family event]
- **[Year]**: [Description of important family event]

## Family Members

### Living Members
- [Name](members/firstname-lastname-year/) - [Relationship]
- [Name](members/firstname-lastname-year/) - [Relationship]

### Previous Generations
- [Name](members/firstname-lastname-year/) - [Relationship] (d. Year)
- [Name](members/firstname-lastname-year/) - [Relationship] (d. Year)

## Interview Progress

- [ ] [Person Name] - Initial interview
- [ ] [Person Name] - Follow-up interview
- [ ] [Person Name] - Not yet scheduled

## Resources & Documents

- Family Bible records
- Immigration documents
- Property records
- Letters and correspondence
- Other genealogical records

## Notes

[Any additional information about this family branch]
EOF

echo "✓ Created family branch at: $BRANCH_PATH"
echo "✓ Created README.md"
echo ""
echo "Success! Family branch created."
echo ""
echo "Next steps:"
echo "1. Edit $BRANCH_PATH/README.md with family information"
echo "2. Add family members with: ./tools/create-member.sh \"Name\" YEAR \"$BRANCH_NAME\""
echo ""
echo "When ready, commit with:"
echo "  git add ."
echo "  git commit -m \"Created $BRANCH_NAME family branch\""
echo "  git push"
