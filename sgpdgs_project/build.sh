#!/bin/bash

# Build script for Vercel
echo "Building Django project..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd sgpdgs_project
python manage.py collectstatic --noinput --clear

echo "Build completed!"
