# GitFam Quick Reference

## Installation

```bash
# macOS/Linux
./setup.sh

# Windows
.\setup.ps1

# Or manually
uv sync
```

## Essential Commands

**With uv (prefix with `uv run`):**
```bash
# Quick start wizard (recommended for first-time setup)
uv run gitfam quick-start

# Initialize new project
uv run gitfam init-project

# Create a family branch
uv run gitfam create-branch

# Add family member
uv run gitfam add-family-member
uv run gitfam add-family-member --branch smith-california

# Generate website
uv run gitfam generate-website
uv run gitfam generate-website --output ./web

# Generate metadata
uv run gitfam metadata                    # Show summary in terminal
uv run gitfam metadata --format json      # Save as JSON
uv run gitfam metadata --format yaml      # Save as YAML
uv run gitfam metadata --branch smith-california  # Specific branch only

# Help
uv run gitfam --help
```

**Or activate virtual environment first:**
```bash
source .venv/bin/activate     # Unix/Mac/Git Bash
# or
.venv\Scripts\activate        # Windows CMD

# Then use commands directly
gitfam quick-start
gitfam create-branch
gitfam metadata
# etc...
```

## File Structure Created

```
families/
└── [branch-name]/
    ├── README.md
    └── members/
        └── [firstname-lastname-year]/
            ├── profile.md          # Main profile
            ├── README.md           # Quick reference
            ├── interviews/
            │   └── videos/
            ├── photos/
            └── documents/
```

## Typical Workflow

1. **Setup**: `gitfam quick-start`
2. **Add members**: `gitfam add-family-member`
3. **Edit profiles**: Open `families/.../members/.../profile.md`
4. **Add media**: Copy files to `photos/` and `interviews/videos/`
5. **Generate site**: `gitfam generate-website`
6. **View**: Open `web/index.html`
7. **Commit**: `git add . && git commit -m "Added family members"`

## Preview Website Locally

```bash
# After generating website
python -m http.server 8000 --directory web

# Then open: http://localhost:8000
```

## Deploy to GitHub Pages

```bash
# Generate site
gitfam generate-website

# Copy to docs folder
cp -r web/* docs/

# Commit
git add docs/
git commit -m "Update website"
git push

# Enable GitHub Pages:
# Settings → Pages → Source: main branch, /docs folder
```

## Tips

- Use descriptive file names: `1950-school-photo.jpg`
- Date format: `YYYY-MM-DD`
- Video naming: `2024-11-05-childhood-part1.mp4`
- Commit often with clear messages
- Back up to multiple git remotes

## Web Viewer Features

- Modern gradient design
- Responsive (mobile-friendly)
- Shows stats, branches, members
- Displays interviews, photos, videos
- Family relationships
- Static HTML (no server needed)

## Customization

Templates are in:
- `templates/profile-template.md`
- `templates/interview-questions.md`
- `gitfam/web_templates/*.html`

## Getting Help

- CLI help: `gitfam --help`
- Full guide: `docs/CLI_GUIDE.md`
- Getting started: `docs/GETTING_STARTED.md`
- Video storage: `docs/VIDEO_STORAGE.md`
