#!/bin/bash
# GitFam Helper Script: Create New Family Member
# Usage: ./create-member.sh "John Doe" 1945 "Smith-California"

# Check if required arguments are provided
if [ $# -lt 3 ]; then
    echo "Usage: ./create-member.sh \"First Last\" BIRTHYEAR \"family-branch\""
    echo "Example: ./create-member.sh \"John Smith\" 1945 \"smith-california\""
    exit 1
fi

FULL_NAME="$1"
BIRTH_YEAR="$2"
FAMILY_BRANCH="$3"

# Convert name to lowercase and replace spaces with hyphens
MEMBER_DIR=$(echo "$FULL_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
MEMBER_DIR="${MEMBER_DIR}-${BIRTH_YEAR}"

# Full path
MEMBER_PATH="families/${FAMILY_BRANCH}/members/${MEMBER_DIR}"

# Check if family branch exists
if [ ! -d "families/${FAMILY_BRANCH}" ]; then
    echo "Error: Family branch 'families/${FAMILY_BRANCH}' does not exist."
    echo "Create it first with: mkdir -p families/${FAMILY_BRANCH}/members"
    exit 1
fi

# Check if member already exists
if [ -d "$MEMBER_PATH" ]; then
    echo "Error: Member directory already exists at $MEMBER_PATH"
    exit 1
fi

# Create directory structure
echo "Creating member directory: $MEMBER_PATH"
mkdir -p "$MEMBER_PATH"
mkdir -p "$MEMBER_PATH/interviews/videos"
mkdir -p "$MEMBER_PATH/photos"
mkdir -p "$MEMBER_PATH/documents"

# Copy profile template
if [ -f "templates/profile-template.md" ]; then
    cp "templates/profile-template.md" "$MEMBER_PATH/profile.md"
    
    # Replace placeholder with actual name
    sed -i.bak "s/\[Full Name\]/$FULL_NAME/g" "$MEMBER_PATH/profile.md"
    rm "$MEMBER_PATH/profile.md.bak"
    
    echo "✓ Created profile.md from template"
else
    echo "Warning: Template not found at templates/profile-template.md"
    echo "# $FULL_NAME" > "$MEMBER_PATH/profile.md"
fi

# Create a README for this member
cat > "$MEMBER_PATH/README.md" << EOF
# $FULL_NAME (b. $BIRTH_YEAR)

## Quick Links
- [Full Profile](profile.md)
- [Interviews](interviews/)
- [Photos](photos/)
- [Documents](documents/)

## Interview Status
- [ ] Initial interview scheduled
- [ ] Childhood & early life
- [ ] Career & work
- [ ] Family stories
- [ ] Wisdom & advice

## To-Do
- [ ] Scan childhood photos
- [ ] Record video interview
- [ ] Get copies of important documents
- [ ] Follow up questions from first interview
EOF

echo "✓ Created directory structure"
echo "✓ Created README.md"
echo ""
echo "Success! Member profile created at: $MEMBER_PATH"
echo ""
echo "Next steps:"
echo "1. Edit $MEMBER_PATH/profile.md with their information"
echo "2. Add photos to $MEMBER_PATH/photos/"
echo "3. Schedule and record interview"
echo "4. Add interview videos to $MEMBER_PATH/interviews/videos/"
echo ""
echo "When ready, commit with:"
echo "  git add ."
echo "  git commit -m \"Added profile for $FULL_NAME\""
echo "  git push"
