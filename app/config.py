import os

"""
Configuration variables for Lakbay.

This should replace constants.py in Lakbay v1.0.

:Author:     Maded Batara III
:Version:    v1.0dev (2016-03-24)
"""

# SQLAlchemy-related variables for database locations.
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Folder containing GTFS files.
GTFS_FOLDER = "data/gtfs-sakay"