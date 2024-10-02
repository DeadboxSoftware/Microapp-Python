"""Alter username column on User model

Revision ID: 3b4d6d0904aa
Revises: 0b86df9d2294
Create Date: 2024-10-01 00:28:23.968640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b4d6d0904aa'
down_revision: Union[str, None] = '0b86df9d2294'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('discord_id', sa.String(), nullable=True))
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('user_email_key', 'user', type_='unique')
    op.drop_constraint('user_username_key', 'user', type_='unique')
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.create_unique_constraint('user_username_key', 'user', ['username'])
    op.create_unique_constraint('user_email_key', 'user', ['email'])
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'username',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('user', 'discord_id')
    # ### end Alembic commands ###
