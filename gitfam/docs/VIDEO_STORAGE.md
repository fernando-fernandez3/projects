# Video Storage Guide for GitFam

Video files are the heart of GitFam, but they're also the biggest technical challenge. This guide explains your storage options.

## The Challenge

**Interview videos are large:**
- 1 hour of 1080p video: ~4-10 GB (depending on quality)
- 1 hour of 4K video: ~20-45 GB
- A typical family with 10 interviews: 100+ GB

**Git challenges with large files:**
- Regular Git struggles with files over 100MB
- Repositories can become bloated and slow
- Cloning/pushing becomes time-consuming

## Solution Options

### Option 1: Git LFS (Recommended for Most)

**What it is:** Git Large File Storage - stores large files separately from your git history

**Pros:**
- ✅ Files stay in your repository structure
- ✅ Transparent to users (mostly)
- ✅ Works with GitHub, GitLab, Bitbucket
- ✅ Maintains file versioning

**Cons:**
- ❌ Limited free storage (1GB on GitHub, 10GB on GitLab)
- ❌ Bandwidth limits on free tiers
- ❌ Can get expensive with many/large videos

**Setup:**
```bash
# Install Git LFS
git lfs install

# It's already configured in .gitattributes
# Just add your video files normally
git add interviews/videos/interview-part1.mp4
git commit -m "Added interview video"
git push
```

**Cost:**
- GitHub: 1GB storage free, then $5/month per 50GB
- GitLab: 10GB storage free, then $60/year per 10GB
- Bitbucket: 1GB free, then $5/month per 100GB

**Best for:** Families with <20 hours of interviews, willing to pay a small monthly fee

---

### Option 2: Cloud Storage + References

**What it is:** Store videos in cloud service, keep links/metadata in Git

**Pros:**
- ✅ Virtually unlimited storage (cheapest option)
- ✅ Keep Git repository lean and fast
- ✅ Easy sharing with family
- ✅ Automatic backups (if using Dropbox/Google Drive/etc.)

**Cons:**
- ❌ Files not in Git = no version history for videos
- ❌ Requires manual organization
- ❌ Links can break if service changes

**Setup:**

1. **Create cloud storage structure:**
```
GoogleDrive/GitFam/
├── fernandez-family/
│   └── john-fernandez-1945/
│       └── interviews/
│           ├── 2024-11-05-part1.mp4
│           └── 2024-11-05-part2.mp4
```

2. **In your Git repo, store references:**
```markdown
<!-- In members/john-fernandez-1945/interviews/interview-2024-11-05.md -->

## Video Files

**Location:** Google Drive - `GitFam/fernandez-family/john-fernandez-1945/interviews/`

- `2024-11-05-part1.mp4` (Duration: 1:23:45, Size: 8.2 GB)
  - Link: https://drive.google.com/file/d/YOUR-FILE-ID/view
- `2024-11-05-part2.mp4` (Duration: 0:45:12, Size: 4.1 GB)
  - Link: https://drive.google.com/file/d/YOUR-FILE-ID/view

**Backup Locations:**
- Dropbox: `/GitFam-Backup/...`
- External HD: `/Volumes/FamilyBackup/GitFam/...`
```

**Services & Costs:**
- Google Drive: 15GB free, $2/month for 100GB, $10/month for 2TB
- Dropbox: 2GB free, $12/month for 2TB
- Microsoft OneDrive: 5GB free, $2/month for 100GB
- iCloud: 5GB free, $1/month for 50GB, $3/month for 200GB

**Best for:** Large video collections (>50 hours), budget-conscious families

---

### Option 3: Self-Hosted Storage

**What it is:** Store videos on your own server/NAS, keep references in Git

**Pros:**
- ✅ Complete control
- ✅ One-time cost (no monthly fees)
- ✅ Unlimited storage (buy more drives)
- ✅ True ownership

**Cons:**
- ❌ Requires technical knowledge
- ❌ You're responsible for backups
- ❌ Initial hardware cost
- ❌ Need reliable internet for family access

**Setup Options:**

**A. Network Attached Storage (NAS)**
- Synology, QNAP, or DIY NAS
- Cost: $300-$1000 for device + drives
- Set up file sharing (SMB/NFS)
- Family accesses via local network or VPN

**B. Personal Cloud Server**
- Nextcloud on a home server or VPS
- Cost: $5-20/month for VPS, or self-host
- Full Dropbox-like interface
- Share links with family

**C. Git LFS Server**
- Self-host Git LFS server
- Most technical option
- Free except server costs

**Best for:** Tech-savvy families, large collections, long-term planning

---

### Option 4: Hybrid Approach (Recommended for Large Projects)

**Combine multiple methods for redundancy:**

1. **Active Storage:** Cloud service for current/recent interviews
2. **Archive Storage:** Move old interviews to cheaper cold storage
3. **Git:** Metadata, transcripts, small clips always in repo
4. **Local Backup:** External HDD stored at different location

**Example workflow:**
```
1. Record interview → Store on Google Drive (working copy)
2. Add metadata/notes to Git
3. After 1 year → Move to AWS Glacier (archive)
4. Update links in Git with archive location
5. Keep backup on external HD at relative's house
```

**Best for:** Multi-generational projects, maximum redundancy

---

## Our Recommendations

### Small Family (<10 people, ~20 hours video)
**Use:** Git LFS + GitHub/GitLab
- Simple setup
- Everything in one place
- Worth the small monthly cost

### Medium Family (10-30 people, 20-100 hours)
**Use:** Cloud Storage + Git References
- Google Drive or Dropbox for videos
- Git for all metadata/documents
- Most cost-effective

### Large/Multi-generational (50+ people, 100+ hours)
**Use:** Hybrid Approach
- Recent interviews on Google Drive
- Archive on AWS Glacier or self-hosted NAS
- Multiple backup locations
- Git for organization

### Tech-Savvy Family
**Use:** Self-Hosted NAS + Git LFS
- Synology NAS for storage
- Git for version control
- Complete ownership

---

## Backup Strategy (Critical!)

**No matter which storage option you choose, follow the 3-2-1 rule:**

- **3** copies of every file
- **2** different storage media types
- **1** copy off-site

**Example:**
1. Primary: Google Drive (cloud)
2. Secondary: External hard drive at home (local)
3. Tertiary: External hard drive at relative's house (off-site)

**Automated backup script:**
```bash
#!/bin/bash
# sync-backups.sh

# Sync from Google Drive to external HD
rclone sync GoogleDrive:GitFam /Volumes/Backup/GitFam

# Sync to off-site location (when connected)
if [ -d "/Volumes/OffsiteBackup" ]; then
    rsync -av /Volumes/Backup/GitFam /Volumes/OffsiteBackup/
fi

echo "Backups complete: $(date)"
```

---

## Migration Path

**Start simple, scale as needed:**

1. **Week 1:** Use Git LFS, start recording interviews
2. **Month 3:** If approaching storage limits, migrate to cloud storage
3. **Year 1:** Set up archive strategy for old interviews
4. **Year 2+:** Consider NAS if collection is large

You can always move videos later. The metadata in Git makes this easy.

---

## Decision Flowchart

```
Are you technical? 
├─ Yes → Consider self-hosted NAS
└─ No → Continue

Do you have <20 hours of video?
├─ Yes → Use Git LFS (simplest)
└─ No → Continue

Is $10-20/month acceptable?
├─ Yes → Use Git LFS with paid storage
└─ No → Use cloud storage + references

Want maximum redundancy?
└─ Yes → Use hybrid approach
```

---

## Questions?

See `/docs/GETTING_STARTED.md` for implementation details or open an issue in the repository.

**Remember:** The best storage solution is the one you'll actually use consistently. Start simple, then optimize.
