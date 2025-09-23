# Wiki Workflow Documentation

## Overview

The Tide project uses a Git submodule for wiki documentation located at `docs/wiki/`. This submodule points to the separate [tide.wiki repository](https://github.com/FreeSideNomad/tide.wiki) which contains all project documentation including domain models, design decisions, and business requirements.

## Repository Structure

- **Main Repository**: `https://github.com/FreeSideNomad/tide` (branch: `main`)
- **Wiki Repository**: `https://github.com/FreeSideNomad/tide.wiki` (branch: `master`)
- **Local Wiki Path**: `docs/wiki/` (submodule)

## Initial Setup

If you're setting up the repository for the first time:

```bash
# Clone the main repository
git clone https://github.com/FreeSideNomad/tide.git
cd tide

# Initialize and update the wiki submodule
git submodule init
git submodule update
```

## Getting Latest Wiki Changes from Remote

### Option 1: Update Submodule to Latest Remote Commit
```bash
# From main repository root
git submodule update --remote docs/wiki
```

### Option 2: Pull Latest Changes in Wiki Directory
```bash
# Navigate to wiki directory
cd docs/wiki

# Pull latest changes from remote
git pull origin master

# Return to main repo
cd ../..

# Update main repo's submodule reference (if needed)
git add docs/wiki
git commit -m "docs: sync wiki submodule to latest remote changes"
git push origin main
```

### Option 3: One-Command Update (Recommended)
```bash
# Update submodule and sync main repo reference
git submodule update --remote docs/wiki && git add docs/wiki && git commit -m "docs: sync wiki to latest remote" && git push origin main
```

## Making Changes to Wiki Documentation

### Step 1: Navigate to Wiki and Make Changes
```bash
cd docs/wiki

# Edit wiki files
vim domain-model.md
# or
code canadian-mental-health-ai-regulatory-framework.md
```

### Step 2: Commit Changes to Wiki Repository
```bash
# Still in docs/wiki directory
git add .
git commit -m "docs: describe your changes here

- Detail 1
- Detail 2"

# Push to wiki repository
git push origin master
```

### Step 3: Update Main Repository Submodule Reference
```bash
# Return to main repository root
cd ../..

# Add the updated submodule reference
git add docs/wiki

# Commit the submodule update
git commit -m "docs: update wiki submodule with [brief description]

Updated wiki documentation:
- [Describe changes]
- [Related GitHub issues if any]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Push to main repository
git push origin main
```

## Complete Workflow Examples

### Example 1: Adding New Documentation
```bash
# Create new documentation file
cd docs/wiki
echo "# New Feature Documentation" > new-feature.md

# Commit to wiki
git add new-feature.md
git commit -m "docs: add new feature documentation"
git push origin master

# Update main repo
cd ../..
git add docs/wiki
git commit -m "docs: update wiki submodule with new feature documentation"
git push origin main
```

### Example 2: Updating Existing Documentation
```bash
# Edit existing file
cd docs/wiki
vim domain-model.md

# Commit changes
git add domain-model.md
git commit -m "docs: update domain model with new requirements

- Add user profile creation business rules
- Update authentication service operations"
git push origin master

# Update main repo
cd ../..
git add docs/wiki
git commit -m "docs: update wiki submodule with domain model changes"
git push origin main
```

### Example 3: Syncing Multiple Team Members' Changes
```bash
# Get latest from both repositories
git pull origin main                    # Update main repo
git submodule update --remote docs/wiki # Update wiki to latest remote

# If there were wiki updates, commit the reference
git add docs/wiki
git commit -m "docs: sync wiki submodule to latest remote changes"
git push origin main
```

## Troubleshooting

### Problem: "fatal: Pathspec 'docs/wiki/file.md' is in submodule 'docs/wiki'"
**Solution**: You're trying to commit wiki files from the main repository. Navigate to `docs/wiki` first:
```bash
cd docs/wiki
git add file.md
git commit -m "your message"
```

### Problem: Wiki directory is empty or missing
**Solution**: Initialize and update the submodule:
```bash
git submodule init
git submodule update
```

### Problem: Changes not appearing after submodule update
**Solution**: The main repository needs to be updated to reference the new wiki commit:
```bash
git add docs/wiki
git commit -m "docs: update wiki submodule reference"
git push origin main
```

### Problem: Merge conflicts in submodule
**Solution**: Resolve conflicts in the wiki directory, then update main repo:
```bash
cd docs/wiki
# Resolve conflicts in files
git add .
git commit -m "docs: resolve merge conflicts"
git push origin master

cd ../..
git add docs/wiki
git commit -m "docs: update wiki submodule after conflict resolution"
git push origin main
```

## Best Practices

### 1. Always Work in Wiki Directory for Wiki Changes
- Never try to commit wiki files from the main repository
- Always `cd docs/wiki` before making wiki commits

### 2. Use Descriptive Commit Messages
```bash
# Good
git commit -m "docs: update domain model with user authentication requirements"

# Bad
git commit -m "update docs"
```

### 3. Keep Main Repo and Wiki in Sync
- After pushing wiki changes, always update the main repository
- Use consistent commit messages between wiki and main repo

### 4. Pull Before Push
```bash
# In wiki directory
git pull origin master
# Make changes
git push origin master

# In main repo
git pull origin main
# Update submodule reference
git push origin main
```

### 5. Use Branch Strategy for Major Changes
For significant documentation changes, consider using branches:
```bash
cd docs/wiki
git checkout -b feature/new-epic-documentation
# Make changes
git push origin feature/new-epic-documentation
# Create PR in wiki repository
```

## Quick Reference Commands

| Task | Command |
|------|---------|
| Get latest wiki changes | `git submodule update --remote docs/wiki` |
| Commit wiki changes | `cd docs/wiki && git add . && git commit -m "message" && git push origin master` |
| Update main repo reference | `git add docs/wiki && git commit -m "docs: update wiki submodule" && git push origin main` |
| Full wiki update workflow | `cd docs/wiki && git add . && git commit -m "message" && git push origin master && cd ../.. && git add docs/wiki && git commit -m "docs: update wiki" && git push origin main` |
| Check submodule status | `git submodule status` |
| Reset submodule to tracking branch | `git submodule update --remote --merge docs/wiki` |

## Integration with Development Workflow

The wiki workflow integrates with the standard development process:

1. **Planning Phase**: Update wiki documentation with requirements
2. **Development Phase**: Reference wiki documentation for implementation
3. **Review Phase**: Ensure wiki documentation reflects implemented features
4. **Documentation Phase**: Update wiki with lessons learned and architecture changes

All GitHub Issues should reference relevant wiki documentation to maintain traceability from business requirements to implementation.