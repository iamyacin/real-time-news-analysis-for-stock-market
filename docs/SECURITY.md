# Security and secret rotation

## What happened

The original repository contained hardcoded credentials:

- MongoDB Atlas connection string in `config.py` and collectors
- ten NewsAPI keys in `config.py`
- Twitter consumer/token secrets in `RealTimeScripts/StreamingTwitterAPI.py`

They were removed from the current working tree during the 2026 restoration.
The old values still exist in git history.

## Immediate actions

1. **Rotate** any key that may still be active:
   - MongoDB Atlas database user password
   - NewsAPI keys
   - Twitter/X app keys and tokens
2. Confirm no secrets are tracked:

   ```bash
   git grep -n -E 'mongodb\+srv://|api_key=|API[0-9]+ *= *["'\'']' -- . ':!*.ipynb'
   ```

3. Keep `.env` out of git:

   ```bash
   grep -n '^\.env$' .gitignore
   ```

## Local secrets

Use `.env`:

```bash
cp .env.example .env
```

The file is ignored. For shared/CI environments, use your platform's secret
store. SOPS is optional; see below.

## Purge the old values from git history

This is destructive and rewrites commit hashes. Do it only after a backup.

```bash
# 1. Back up the repository
git bundle create ../stock-news-backup-$(date +%F).bundle --all
git tag pre-secret-purge-$(date +%F)

# 2. Create a replacement file with one old secret per line
cat > /tmp/secrets.txt <<'EOF'
old-mongo-password==>***REMOVED***
old-newsapi-key==>***REMOVED***
old-twitter-secret==>***REMOVED***
EOF

# 3. Rewrite history
git filter-repo --replace-text /tmp/secrets.txt

# 4. Verify
git grep -n 'old-newsapi-key' $(git rev-list --all) || echo "clean"

# 5. Force-push only after confirming the backup and the rewritten history
git push --force-with-lease origin master
```

After the rewrite:

- All commit hashes change.
- `docs/PROVENANCE.md` references old merge commits; add a note about the
  rewrite and the backup location.
- Collaborators must re-clone.

## SOPS (optional)

If you want encrypted secrets in the repository:

```bash
sops --encrypt --age <your-age-public-key> .env > secrets.env.enc
sops --decrypt secrets.env.enc > .env
```

Add `secrets.env.enc` only if your team has the age key. Never commit the age
private key.

## Public repository checklist

- [ ] Keys rotated
- [ ] `.env` ignored
- [ ] No secrets in the current tree
- [ ] History purged or old keys confirmed dead
- [ ] `README.md` security note present
- [ ] `git status` clean before publishing
