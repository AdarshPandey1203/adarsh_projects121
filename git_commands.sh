# This script will clear your GitHub repository and push the current project files.
# PLEASE BE CAREFUL: This will permanently delete the history of your repository.

# Initialize a new git repository
git init

# Add a remote to your GitHub repository
git remote add origin https://github.com/AdarshPandey1203/adarsh_projects121

# Create a new empty branch
git checkout --orphan temp_branch

# Add all files and commit
git add .
git commit -m "Initial commit"

# Delete the main branch
git branch -D main

# Rename the temp branch to main
git branch -m main

# Force push the new main branch to your remote repository
git push -f origin main
