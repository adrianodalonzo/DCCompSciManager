from flask import current_app, g
import click
import os
from .db import Database

def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
def init_db():
    db = get_db()
    file_path = os.path.join(current_app.root_path, 'setup.sql')
    db.run_file(file_path)
    
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
    