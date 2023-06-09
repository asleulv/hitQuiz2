"""empty message

Revision ID: 956853b54a2d
Revises: 5693a41970f2
Create Date: 2023-05-15 23:48:23.584543

"""
from alembic import op
from quiz import db
from quiz.questions.models import Hit
import sqlalchemy as sa
import json

# revision identifiers, used by Alembic.
revision = '956853b54a2d'
down_revision = '4b8d0ecfe74b' 
branch_labels = None
depends_on = None


def upgrade():
    with open('./data/hits.json') as fh:
        data = json.load(fh)
    op.bulk_insert(Hit.__table__, data)


def downgrade():
    try:
        Hit.query.delete()
        db.session.commit()
    except: 
        db.session.rollback()
    pass
