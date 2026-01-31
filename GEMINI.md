# InkyFrame Project Documentation (GEMINI Summary)

This file serves as a central index and summary of the project documentation for the **InkyFrame** project.

## 📖 Project Overview

**InkyFrame** is a web-based application designed to control the **Inky Impression 7.3"** e-ink display. It provides a user-friendly interface for uploading photos, managing a gallery, and displaying images on the e-ink screen. The system automatically handles image optimization (resizing, dithering, color palettes) to ensure photos look great on the 7-color e-paper display.

**Core Tech Stack:**
*   **Backend:** FastAPI (Python)
*   **Frontend:** HTML/CSS/Vanilla JS
*   **Hardware:** Raspberry Pi + Inky Impression 7.3" (Spectra 6)

## 📂 Documentation Index

All detailed documentation is located in the `docs/` directory.

| File | Description |
|------|-------------|
| [📄 Project Specification](docs/project_spec.md) | **Start Here.** Detailed project requirements, architecture, API endpoints, and feature specifications. |
| [🚀 Deployment Guide](docs/DEPLOYMENT.md) | Instructions for deploying the application to a Raspberry Pi, including directory structure and service setup. |
| [📜 Deployment Scripts](docs/DEPLOY_SCRIPTS.md) | Guide to using the automated deployment scripts (`deploy_simple.bat`, `deploy.sh`) for Windows/Linux/Mac. |
| [🛠 Server Installation](docs/SERVER_INSTALL.md) | Manual steps for setting up the server environment on the Raspberry Pi (installing `uv`, dependencies, systemd). |
| [🖊 Inky Library Setup](docs/INSTALL_INKY.md) | Specific instructions for installing the pimoroni `inky` library on the server (from local source or PyPI). |
| [☁️ Weather Feature](docs/WEATHER_TESTING.md) | Guide for the Weather Display feature (Current status: Backend API ready, UI in progress). Includes API setup and testing steps. |
| [🐙 GitHub Guide](docs/GITHUB.md) | Instructions for publishing the project to GitHub, including repository setup and optional steps. |

## ⚡ Quick Reference

### Development
```bash
# Run local development server
uv run uvicorn src.main:app --reload
```

### Deployment (Quick)
**Windows:**
```cmd
scripts/deploy/deploy_simple.bat
```

**Linux/Mac:**
```bash
./scripts/deploy/deploy_simple.sh
```

### Server Management (on Raspberry Pi)
```bash
# Start server
./start.sh

# Check status
./status.sh
```
