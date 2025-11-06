# GitFam Tools

This directory contains legacy bash helper scripts for creating family branches and members.

## ⚠️ Recommendation

**We recommend using the interactive CLI tool instead** (located in `gitfam/`):

```bash
uv run gitfam create-branch
uv run gitfam add-family-member
```

The CLI provides:
- ✅ Interactive prompts with validation
- ✅ Cross-platform support (Windows, Mac, Linux)
- ✅ Automatic file template generation
- ✅ Better error handling
- ✅ Recursive member addition workflow

See [`../docs/CLI_GUIDE.md`](../docs/CLI_GUIDE.md) for full documentation.

---

## Legacy Bash Scripts

These scripts are kept for users who prefer shell scripting or have specific automation needs:

### `create-family-branch.sh`
```bash
./tools/create-family-branch.sh "surname-location" "Description"
```

### `create-member.sh`
```bash
./tools/create-member.sh "First Last" BIRTHYEAR "family-branch"
```

**Note:** These scripts work only on Unix-like systems (Linux, macOS, Git Bash on Windows).
