"""Add fields to DataSourceType model

Revision ID: 9c2f5b290b16
Revises: 
Create Date: 2023-03-20 14:19:47.665501

"""
import json

from alembic import op
import sqlalchemy as sa

from data_source_api.utils import get_class_by_data_source_name
from db_engine import Session
from schemas import DataSourceType

# revision identifiers, used by Alembic.
revision = '9c2f5b290b16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    try:
        op.add_column('data_source_type', sa.Column('display_name', sa.String(length=32), nullable=True))
        op.add_column('data_source_type', sa.Column('config_fields', sa.String(length=1024), nullable=True))
        with Session() as session:
            # update existing data sources
            data_source_types = session.query(DataSourceType).all()
            for data_source_type in data_source_types:
                data_source_class = get_class_by_data_source_name(data_source_type.name)
                config_fields = data_source_class.get_config_fields()

                data_source_type.config_fields = json.dumps([config_field.dict() for config_field in config_fields])
                data_source_type.display_name = data_source_class.get_display_name()

            session.commit()
    except:
        pass


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data_source_type', 'config_fields')
    op.drop_column('data_source_type', 'display_name')
    # ### end Alembic commands ###
