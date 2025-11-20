"""Database extension instance."""
from flask_sqlalchemy import SQLAlchemy

# Instantiate the SQLAlchemy extension here to avoid circular imports.
db = SQLAlchemy()
