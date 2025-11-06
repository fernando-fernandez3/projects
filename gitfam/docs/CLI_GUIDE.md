# GitFam CLI Guide

The GitFam CLI provides interactive commands to easily build and manage your family history project.

## Installation

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install GitFam with all dependencies
cd gitfam
uv sync
```

**Note:** With `uv`, use `uv run` prefix for commands:
```bash
uv run gitfam quick-start
uv run gitfam create-branch
```

Or activate the virtual environment first:
```bash
source .venv/bin/activate        # Unix/Mac
# or
source .venv/Scripts/activate    # Git Bash
# or
.venv\Scripts\activate           # Windows CMD

# Then use commands directly
gitfam quick-start
```

### Using pip (alternative)

```bash
cd gitfam
pip install -e .

# Commands work directly after pip install
gitfam quick-start
```

## Commands

### Quick Start (Recommended for First Time)

```bash
gitfam quick-start
```

This interactive wizard will:
- Initialize your GitFam project (if needed)
- Create your first family branch
- Add your first family member
- Guide you through the setup process

### Initialize a New Project

```bash
gitfam init-project
```

Creates the basic GitFam directory structure:
- `families/` - Family branches
- `templates/` - Profile and interview templates
- `tools/` - Helper scripts
- `docs/` - Documentation
- `.gitattributes` - Git LFS configuration
- `.gitignore` - Git ignore rules

### Create a Family Branch

```bash
gitfam create-branch
```

Interactive prompts will ask for:
- Branch name (e.g., "smith-california")
- Description

This creates:
```
families/
└── [branch-name]/
    ├── README.md
    └── members/
```

### Add a Family Member

```bash
gitfam add-family-member

# Or specify the branch
gitfam add-family-member --branch smith-california
```

Interactive prompts will collect:
- Full name
- Birth year
- Birth date (optional)
- Birth place
- Current residence
- Family relationships

This creates:
```
families/[branch]/members/[name-year]/
├── profile.md
├── README.md
├── interviews/
│   └── videos/
├── photos/
└── documents/
```

### Generate Website

```bash
gitfam generate-website

# Or specify output directory
gitfam generate-website --output ./web
```

Generates a beautiful static website from your family tree that can be:
- Opened locally in a browser
- Hosted on GitHub Pages
- Hosted on any static site hosting service

## Workflow Example

### Starting a New Family History Project

```bash
# 1. Initialize project
cd my-family-history
uv run gitfam init-project

# 2. Run quick start wizard
uv run gitfam quick-start
# Follow the prompts to create your first branch and member

# 3. Add more family members
uv run gitfam add-family-member
# Repeat for each family member

# 4. Edit profiles with details
# Open families/[branch]/members/[person]/profile.md in your editor

# 5. Add photos and documents
# Copy files to the appropriate directories

# 6. Record interviews
# Use templates/interview-questions.md as a guide

# 7. Generate website to preview
uv run gitfam generate-website
# Open web/index.html in your browser

# 8. Commit to git
git add .
git commit -m "Added family members"
git push
```

### Adding to an Existing Project

```bash
# Add a new branch
uv run gitfam create-branch

# Add members to the new branch
uv run gitfam add-family-member

# Regenerate website
uv run gitfam generate-website

# Commit changes
git add .
git commit -m "Added new family branch"
```

## Tips & Tricks

### Batch Adding Members

For adding multiple members quickly:

```bash
# Add first member
uv run gitfam add-family-member --branch smith-california

# The command remembers the last branch, making it faster to add multiple members
# Just keep running the command
uv run gitfam add-family-member  # Uses last branch
uv run gitfam add-family-member  # Uses last branch
```

### Editing Profiles

The CLI creates basic profiles, but you'll want to edit them with rich details:

1. Find the profile: `families/[branch]/members/[person]/profile.md`
2. Open in your favorite editor
3. Fill in the sections using the template structure
4. Save and commit

### Organizing Photos

Best practices for photo organization:

```
members/john-smith-1945/photos/
├── childhood/
│   ├── 1950-school-photo.jpg
│   └── 1955-family-picnic.jpg
├── military/
│   └── 1965-navy-portrait.jpg
└── family/
    ├── 1970-wedding.jpg
    └── 2000-grandchildren.jpg
```

### Video Management

For interview videos, use descriptive names:

```
members/john-smith-1945/interviews/videos/
├── 2024-11-05-childhood-part1.mp4
├── 2024-11-05-childhood-part2.mp4
├── 2024-12-10-career-stories.mp4
└── 2025-01-15-advice-wisdom.mp4
```

## Web Viewer

### Viewing the Website Locally

After generating:

```bash
# Simple Python server
python -m http.server 8000 --directory web

# Then open: http://localhost:8000
```

Or just open `web/index.html` directly in your browser.

### Hosting on GitHub Pages

```bash
# Generate site
gitfam generate-website

# Copy to docs folder (GitHub Pages can serve from /docs)
cp -r web/* docs/

# Commit and push
git add docs/
git commit -m "Update website"
git push

# Enable GitHub Pages in repo settings:
# Settings → Pages → Source: Deploy from branch → Branch: main, /docs
```

### Styling and Customization

The generated website uses embedded CSS for simplicity. To customize:

1. Generate the site
2. Edit `web/index.html` and update the `<style>` section
3. Or create a custom `gitfam/web_templates/` with your own templates

## Troubleshooting

### Command Not Found

```bash
# Make sure GitFam is installed
uv sync

# Use uv run prefix
uv run gitfam --help

# Or activate the virtual environment
source .venv/bin/activate  # Then use 'gitfam' directly
```

### Import Errors

```bash
# Install dependencies
uv sync
```

### Permission Errors

```bash
# On Unix/Mac, make scripts executable
chmod +x tools/*.sh
```

## Advanced Usage

### Scripting with GitFam

You can use GitFam commands in scripts:

```bash
#!/bin/bash
# bulk-add-members.sh

# Read from CSV and add members
while IFS=, read -r name year place; do
    # You'd need to write to stdin for interactive prompts
    # Or create non-interactive versions of commands
    echo "Would add: $name ($year) from $place"
done < members.csv
```

### Custom Templates

Place custom templates in `templates/` and reference them in your workflow.

### Automation

Consider setting up:
- GitHub Actions to auto-generate website on commit
- Backup scripts to multiple remotes
- Notification systems when content is added

---

## Getting Help

```bash
# General help
uv run gitfam --help

# Command-specific help
uv run gitfam init-project --help
uv run gitfam add-family-member --help
uv run gitfam generate-website --help
```

Or visit the documentation in `/docs`.
