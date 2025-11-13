# 🔒 Security Notice

## ⚠️ Important: .env File Was Previously Tracked

**Date:** November 13, 2025

### Issue
The `cafe-fausse-backend/.env` file containing sensitive credentials was previously tracked in git history.

### Actions Taken
1. ✅ Created comprehensive `.gitignore` files for root, backend, and frontend
2. ✅ Removed `.env` from git tracking using `git rm --cached`
3. ✅ `.env` file still exists locally for development use
4. ✅ All future commits will ignore `.env` files

### 🚨 CRITICAL: If This Repo is Public

If this repository has ever been pushed to GitHub or any public platform, **you MUST**:

1. **Rotate ALL credentials immediately:**
   - Database password
   - JWT secret
   - Admin password
   - Email password (Gmail App Password)
   - Any API keys

2. **Consider these options:**
   - Make the repository private
   - OR use `git filter-branch` or `BFG Repo-Cleaner` to remove `.env` from history
   - OR create a new repository with clean history

### Git History Cleanup (If Needed)

To completely remove `.env` from git history:

```bash
# Option 1: Using BFG Repo-Cleaner (recommended)
# Download from: https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Option 2: Using git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch cafe-fausse-backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push to update remote (WARNING: This rewrites history)
git push origin --force --all
git push origin --force --tags
```

### Best Practices Going Forward

1. **Never commit secrets:**
   - Use `.env.example` with dummy values
   - Keep actual `.env` only on local machines

2. **Use environment variables in production:**
   - Railway, Vercel, etc. provide secure environment variable management
   - Never hardcode credentials in source code

3. **Regular security audits:**
   - Check `git ls-files | grep .env` regularly
   - Use pre-commit hooks to prevent accidental commits

4. **Credential rotation:**
   - Rotate credentials periodically
   - Immediately rotate if exposure is suspected

### Current Status

✅ `.gitignore` files are in place  
✅ `.env` is no longer tracked (as of this commit)  
⚠️ Historical commits may still contain `.env` - see cleanup instructions above  
✅ `.env.example` files are safe to commit (contain no real credentials)

### Questions?

Refer to:
- `DEPLOYMENT.md` for production security checklist
- `.env.example` files for required variables
- This document for credential rotation procedures
