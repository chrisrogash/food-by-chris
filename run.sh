#!/bin/bash
set -e  # stop on first error

# Install Git + SSH client
apt-get update
apt-get install -y git openssh-client

# Configure Git
git config --global user.name "chrisrogash"
git config --global user.email "chris.rogash@hotmail.com"
git config --global core.sshCommand "ssh -i /root/.ssh/id_ed25519 -o StrictHostKeyChecking=no"
git config --global --add safe.directory /app
# CONNECT WITH GIT
cd /app

if [ ! -d ".git" ]; then
  git init
  git checkout -b main  # create main branch explicitly
fi

if ! git remote | grep -q "origin"; then
  git remote add origin git@github.com:chrisrogash/food-by-chris.git
fi

# make sure there’s at least one commit
if [ -z "$(git rev-parse --verify HEAD 2>/dev/null)" ]; then
  git add .
  git commit -m "Initial commit"
fi


# install admin portal requirements
pip install --no-cache-dir -r /app/admin/requirements.txt

# running the admin portal
python /app/admin/app.py

