# GitHub Submission Guide

## Quick Setup Steps

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Pesapal Junior Developer Challenge 2026 submission"
```

### 2. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `pesapal-jdev26-chris` (or your preferred name)
3. Description: "Pesapal Junior Developer Challenge 2026 - In-memory RDBMS with SQL interface"
4. **Set to PUBLIC** (required for submission)
5. **DO NOT** initialize with README (you already have one)
6. Click "Create repository"

### 3. Push to GitHub
```bash
# Replace <your-username> with your GitHub username
git remote add origin https://github.com/<your-username>/pesapal-jdev26-chris.git
git branch -M main
git push -u origin main
```

### 4. Update README
After pushing, update your README.md:
- Replace `[GitHub Link - Add your URL here after pushing]` with your actual repo URL
- Add your email in the Contact section
- Add your GitHub profile URL

Then commit and push:
```bash
git add README.md
git commit -m "Update README with repo URL and contact info"
git push
```

### 5. Verify Repository
Check your GitHub repo has:
- ✅ All files visible
- ✅ README displays properly
- ✅ Repository is PUBLIC
- ✅ No sensitive information (credentials, API keys, etc.)

### 6. Submit Application
1. Click "Apply Now" on the Pesapal job posting
2. Paste your GitHub repository URL: `https://github.com/<your-username>/pesapal-jdev26-chris`
3. Upload your CV
4. Submit before **23:59:59 EAT on 17th January 2026**

## Recommended Repository Settings

### About Section (on GitHub)
- **Description**: "In-memory RDBMS with SQL-like interface and web UI (Pesapal Challenge 2026)"
- **Topics**: `python`, `database`, `sql`, `flask`, `rdbms`, `pesapal-challenge`
- **Website**: Leave blank or add `http://localhost:5000` with note "Run locally"

### README Badges (Optional)
Add these at the top of README for professional look:
```markdown
![Python](https://img.shields.io/badge/python-3.13-blue)
![Flask](https://img.shields.io/badge/flask-3.0.0-green)
![Tests](https://img.shields.io/badge/tests-20%20passing-success)
```

## Troubleshooting

### If git is not installed:
Download from: https://git-scm.com/downloads

### If you have authentication issues:
1. Create a Personal Access Token on GitHub (Settings → Developer settings → Personal access tokens)
2. Use token as password when pushing

### If repo already exists:
```bash
git remote set-url origin https://github.com/<your-username>/pesapal-jdev26-chris.git
```

## Final Checklist Before Submission

- [ ] Repository is PUBLIC
- [ ] All code is pushed to GitHub
- [ ] README has your actual repo URL
- [ ] Contact information added in README
- [ ] Ran `python verify_submission.py` - all checks passed
- [ ] Tested REPL works: `python repl.py`
- [ ] Tested web app works: `python -m web_app.app`
- [ ] All tests pass: `python -m unittest tests.test_database`
- [ ] No sensitive information in code
- [ ] CV is ready to upload
- [ ] Submitted before deadline: Jan 17, 2026 23:59:59 EAT

Good luck! 🚀
