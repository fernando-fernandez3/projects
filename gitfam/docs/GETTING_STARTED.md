# Getting Started with GitFam

Welcome! This guide will help you set up GitFam for your family.

## Prerequisites

Before you begin, you'll need:
- Git installed on your computer ([Download Git](https://git-scm.com/))
- Git LFS installed ([Download Git LFS](https://git-lfs.github.com/))
- A GitHub/GitLab account (for backup and collaboration)
- Basic familiarity with files and folders

## Quick Start

### 1. Fork or Clone This Repository

**Option A: Fork on GitHub (Recommended)**
1. Click "Fork" at the top of this repository
2. This creates your own copy you can customize
3. Clone your fork to your computer:
```bash
git clone https://github.com/YOUR-USERNAME/gitfam.git
cd gitfam
```

**Option B: Download and Start Fresh**
1. Download this repository as a ZIP
2. Extract it to a folder on your computer
3. Initialize git:
```bash
cd gitfam
git init
git add .
git commit -m "Initial GitFam setup"
```

### 2. Install Git LFS

Git LFS is essential for handling video files:

```bash
# Install Git LFS (if not already installed)
# macOS: brew install git-lfs
# Windows: Download from https://git-lfs.github.com/
# Linux: apt-get install git-lfs

# Initialize Git LFS in your repository
git lfs install
```

Verify it's working:
```bash
git lfs track
# Should show the video extensions from .gitattributes
```

### 3. Install the GitFam CLI Tool (Optional but Recommended)

GitFam includes an interactive CLI tool that makes creating branches and members much easier:

```bash
# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

Now you can use the interactive commands:
```bash
# Quick start - sets up everything
uv run gitfam quick-start

# Or use individual commands:
uv run gitfam create-branch
uv run gitfam add-family-member
uv run gitfam generate-website
```

See [`CLI_GUIDE.md`](CLI_GUIDE.md) for full CLI documentation.

### 4. Create Your First Family Branch

**Option A: Using the CLI (Recommended)**
```bash
uv run gitfam create-branch
```

This will interactively prompt you for:
- Branch name (e.g., `fernandez-california`)
- Description
- Founding members
- Key locations

**Option B: Manual Creation**

```bash
# Navigate to families directory
cd families
Now edit `profile.md` with their information.

### 6. Add Interviews and Media

```bash
cd families/fernandez-california/members/john-fernandez-1945/interviews

# Create interview notes
cp ../../../../../templates/interview-questions.md interview-2024-11-05.md
# Edit the file with notes and metadata

# Add video files (they'll use Git LFS automatically)
cp ~/Desktop/interview-part1.mp4 videos/
cp ~/Desktop/interview-part2.mp4 videos/
```

### 7. Generate the Website (Optional)

To preview your family tree as a beautiful static website:

```bash
# From the gitfam root directory
uv run gitfam generate-website

# Open dist/index.html in your browser
```

### 8. Commit Your Changes

```bash
# From the gitfam root directory
git add .
git commit -m "Added John Fernandez profile and first interview"
git push origin main
```

### 9. Set Up Redundant Backups

**GitHub (Primary Remote)**
```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-FAMILY-REPO.git
git push -u origin main
```

**Additional Backup (Optional but Recommended)**
```bash
# Add a second remote (GitLab, Bitbucket, or your own server)
git remote add backup https://gitlab.com/YOUR-USERNAME/YOUR-FAMILY-REPO.git
git push backup main
```

**Local Backups**
- Clone the repository to an external hard drive
- Set up automatic sync to NAS or cloud storage
- Keep a USB backup stored separately

## Next Steps

### Use the CLI for Ongoing Work

Once set up, the CLI makes adding content easy:

```bash
# Add more family members
uv run gitfam add-family-member

# Generate metadata and statistics
uv run gitfam metadata

# Rebuild the website after changes
uv run gitfam generate-website
```

### Conduct More Interviews
1. Read `/templates/interview-questions.md`
2. Set up two phones on tripods
3. Record the interview
4. Follow the guide for what to ask

### Invite Family to Collaborate

**For Technical Family Members:**
1. Give them access to the repository
2. They can clone and push changes
3. Use branches and pull requests for organization

**For Non-Technical Family Members:**
1. They can email you content
2. You can add it on their behalf
3. Consider setting up a simple web form (future enhancement)

## Best Practices

### File Naming
- Use lowercase
- Use hyphens instead of spaces
- Include dates in format YYYY-MM-DD
- Be consistent

### Directory Structure
Keep this structure for each person:
```
firstname-lastname-birthyear/
├── profile.md
├── interviews/
│   ├── interview-2024-11-05.md
│   ├── interview-2024-12-15.md
│   └── videos/
│       ├── 2024-11-05-part1.mp4
│       └── 2024-11-05-part2.mp4
├── photos/
│   ├── childhood/
│   ├── wedding/
│   └── family/
└── documents/
    ├── birth-certificate.pdf
    └── letters/
```

### Commit Messages
Be descriptive:
- ✅ "Added Maria's childhood photos from 1960s"
- ✅ "Interview with grandfather about WWII service"
- ❌ "Update"
- ❌ "Changes"

### Privacy Considerations
- Keep sensitive information in a private repository
- Consider separate repos for living vs. deceased family members
- Some family members may not want to be included - respect that
- Ask permission before sharing others' stories

## Troubleshooting

### Large Files Won't Push
**Problem:** Git refuses to push large video files

**Solution:** 
```bash
# Make sure Git LFS is tracking the files
git lfs track "*.mp4"
git add .gitattributes
git commit -m "Configure LFS for video files"

# Migrate existing large files to LFS
git lfs migrate import --include="*.mp4"
```

### Out of GitHub LFS Storage
**Problem:** GitHub LFS has limited free storage (1GB)

**Solutions:**
1. Upgrade GitHub LFS storage
2. Use a different remote that allows more (GitLab gives 10GB free)
3. Store videos on a personal server and just keep references in git
4. Use a cloud storage service (Google Drive, Dropbox) with links in the repo

### Family Member Can't Access
**Problem:** Non-technical family member wants to contribute

**Solutions:**
1. Give them access to Google Drive folder, you sync to git
2. Set up a private website with upload form
3. Have them email content to you
4. Schedule times to help them add content

## Advanced Setup

### Multiple Remotes Script
Create `tools/sync-all-remotes.sh`:
```bash
#!/bin/bash
# Sync to all backup locations

git push origin main
git push backup main
git push gitlab main

echo "Synced to all remotes"
```

### Automation
- Set up GitHub Actions to create backups
- Auto-generate family tree visualization
- Email notifications when content is added

---

## Need Help?

- Check `/docs` for more guides
- Open an issue in the repository
- The GitFam community is here to help

**Remember:** The hardest part is starting. Once you capture that first interview, you'll have preserved something irreplaceable. Start today.
