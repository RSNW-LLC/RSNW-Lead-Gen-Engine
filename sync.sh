#!/bin/bash

echo "[*] Syncing RSNW Lead Engine to GitHub..."

# 1. Add all new files
git add .

# 2. Save changes with a timestamp
git commit -m "Auto-sync: $(date)"

# 3. Push to GitHub using the RSNW key automatically
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsnw -o StrictHostKeyChecking=no" git push origin main

echo "[✓] Sync Complete! Your code is live."
