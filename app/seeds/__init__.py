from flask.cli import AppGroup
from .users import seed_users, undo_users
from .stocks import seed_stocks, undo_stocks
from .notes import seed_notes, undo_notes
from .pinned import seed_pinned, undo_pinned
from .watchlists import seed_watchlist, undo_watchlist
from .comments import seed_comments, undo_comments
from .articles import seed_articles, undo_articles
from .planner import seed_planner, undo_planner

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_stocks()
        undo_notes()
        undo_pinned()
        undo_watchlist()
        undo_comments()
        undo_articles()
        undo_planner()
    seed_users()
    seed_stocks()
    seed_notes()
    seed_pinned()
    seed_watchlist()
    seed_comments()
    seed_articles()
    seed_planner()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_users()
    undo_stocks()
    undo_notes()
    undo_pinned()
    undo_watchlist()
    undo_comments()
    undo_articles()
    undo_planner()
    # Add other undo functions here
