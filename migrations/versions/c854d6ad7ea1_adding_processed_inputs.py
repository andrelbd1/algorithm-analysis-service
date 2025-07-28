"""adding processed inputs

Revision ID: c854d6ad7ea1
Revises: e82ac4f587a0
Create Date: 2025-05-27 19:36:34.550640

"""
from alembic import op
import pathlib
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c854d6ad7ea1'
down_revision = 'e82ac4f587a0'
branch_labels = None
depends_on = None


def upgrade():
    sql_path = pathlib.Path(__file__).parent.parent
    lst_files = ['load_execution_data.sql',
                 'load_payload_data.sql',
                 'load_result_data.sql']
    for f in lst_files:
        f = f"{sql_path}/{f}"
        with open(f, 'r') as file:
            sql_commands = file.read()
        op.execute(sql_commands)


def downgrade():    
    op.execute('DELETE FROM service_algorithm_analysis.payload;')
    op.execute('DELETE FROM service_algorithm_analysis."result";')
    op.execute('DELETE FROM service_algorithm_analysis.execution;')
