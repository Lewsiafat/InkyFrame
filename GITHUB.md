# Publishing InkyFrame to GitHub

Quick guide to publish your InkyFrame project to GitHub.

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `InkyFrame`
3. Description: `📸 Web server for uploading and displaying photos on Inky e-ink displays`
4. Choose: **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **Create repository**

## Step 2: Add Remote and Push

Run these commands in your project directory:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/InkyFrame.git

# Push to GitHub
git push -u origin master
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 3: Add Topics (Optional but Recommended)

On your GitHub repository page:
1. Click the ⚙️ gear icon next to "About"
2. Add topics:
   - `e-ink`
   - `raspberry-pi`
   - `fastapi`
   - `photo-gallery`
   - `inky-impression`
   - `python`
   - `web-server`

## Step 4: Add Repository Description

In the "About" section, add:
- **Description:** `📸 Web server for uploading and displaying photos on Inky e-ink displays`
- **Website:** (your deployment URL if you have one)

## Recommended: Add Badges to README

Add these badges at the top of your README.md:

```markdown
# InkyFrame

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 📸 A FastAPI web server for uploading, optimizing, and displaying photos on Pimoroni Inky Impression e-ink displays
```

## Optional: Add Screenshots

Add screenshots to make your repository more attractive:

1. Create a `screenshots` folder
2. Add images of:
   - Web interface
   - Photo gallery
   - Photo displayed on Inky
3. Reference in README:

```markdown
## Screenshots

### Web Interface
![Web Interface](screenshots/web-interface.png)

### Photo Gallery
![Gallery](screenshots/gallery.png)

### E-ink Display
![Display](screenshots/display.jpg)
```

## Your Repository is Ready! 🎉

Your InkyFrame project is now on GitHub and ready to share with the world!

**Repository URL:** `https://github.com/YOUR_USERNAME/InkyFrame`

## Next Steps

- ⭐ Star your own repository
- 📝 Add more documentation if needed
- 🐛 Set up GitHub Issues for bug tracking
- 🔄 Enable GitHub Actions for CI/CD (optional)
- 📢 Share your project on social media!
