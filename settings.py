import os

# Project directory
PROJECT_DIR = os.getcwd()

# Database directory
DATABASES_DIR = os.path.join(PROJECT_DIR, 'databases')

# Sessions directory
SESSIONS_DIR = os.path.join(PROJECT_DIR, 'sessions')

# Apps directory
APPS_DIR = os.path.join(PROJECT_DIR, 'app')

# Applications

APPS = [
    'admin',
    'client',
    'node',
]

# Database name

DATABASE_NAME = 'youhere_dev'