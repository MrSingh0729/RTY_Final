from app import app
from init_db import init_db
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize database with model and project goal data')
    parser.add_argument('--force', action='store_true', help='Force reinitialization by deleting existing data')
    
    args = parser.parse_args()
    
    with app.app_context():
        init_db(force=args.force)