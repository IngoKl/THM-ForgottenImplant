del .git
git init --initial-branch=main
git add .
git commit -m "Initial Commit (Redacted)"
git remote add origin git@github.com:IngoKl/THM-ForgottenImplant
git push --force --set-upstream origin main
git gc --aggressive --prune=all 