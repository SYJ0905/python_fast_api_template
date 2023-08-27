import os
import sys

sys.path.insert(0, os.getcwd())

from src.main import app

# from src import create_app, db


application = app
# with application.app_context():
#     db.create_all()
