import os

# Getting current directory for script
dirCurrent = os.path.abspath(os.path.dirname(__file__))

# For hackathons, you dont really need production config
DEBUG = True

# Secret key for session management
SECRET_KEY = 'insertSecretKeyHere'

# connect to database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(dirCurrent, "database.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(dirCurrent, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False