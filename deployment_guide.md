# Deployment Guide for Symbiome

## Prerequisites

1.  **Install Git**
    *   Download and install Git from [git-scm.com](https://git-scm.com/downloads).
    *   During installation, you can use all default settings.
    *   After installation, **restart VS Code** to make sure it recognizes the `git` command.

## Phase 1: Push to GitHub

1.  **Create a New Repository on GitHub**
    *   Go to [github.com/new](https://github.com/new).
    *   **Repository name**: `symbiome` (or any name you prefer).
    *   **Public/Private**: Choose whichever you prefer (Public is easier for Streamlit Cloud).
    *   **Initialize this repository with**: Leave all unchecked (no README, no .gitignore, no license).
    *   Click **Create repository**.

2.  **Push Your Code**
    *   Copy the commands under "…or push an existing repository from the command line". They will look like this:
        ```bash
        git remote add origin https://github.com/YOUR_USERNAME/symbiome.git
        git branch -M main
        git push -u origin main
        ```
    *   Paste and run these commands in your terminal here in VS Code.

## Phase 2: Deploy to Streamlit Cloud

1.  **Log in to Streamlit**
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Sign in with your GitHub account.

2.  **Deploy the App**
    *   Click **New app** (top right).
    *   **Repository**: Select `YOUR_USERNAME/symbiome`.
    *   **Branch**: `main`.
    *   **Main file path**: `app.py`.
    *   Click **Deploy!**.

## Troubleshooting
*   **Missing Dependencies**: If the app fails to start, check the logs on Streamlit Cloud. It usually means a package is missing from `requirements.txt`.
*   **Secrets**: If you use any API keys (like OpenAI), go to the App Settings in Streamlit Cloud -> Secrets and add them there.
