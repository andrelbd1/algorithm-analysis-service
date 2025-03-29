"""create tables

Revision ID: 886facf07954
Revises: 
Create Date: 2024-11-04 22:06:45.457783

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '886facf07954'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('algorithm',
    sa.Column('algorithm_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('source', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('algorithm_id'),
    schema='service_algorithm_analysis'
    )
    op.create_table('criteria',
    sa.Column('criteria_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('criteria_id'),
    schema='service_algorithm_analysis'
    )
    op.create_table('algorithm_criteria',
    sa.Column('algorithm_criteria_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('algorithm_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('criteria_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['algorithm_id'], ['service_algorithm_analysis.algorithm.algorithm_id'], ),
    sa.ForeignKeyConstraint(['criteria_id'], ['service_algorithm_analysis.criteria.criteria_id'], ),
    sa.PrimaryKeyConstraint('algorithm_criteria_id'),
    schema='service_algorithm_analysis'
    )
    op.create_index('idx_algorithm_criteria_algorithm', 'algorithm_criteria', ['algorithm_id'], unique=False, schema='service_algorithm_analysis')
    op.create_index('idx_criteria_algorithm_criteria', 'algorithm_criteria', ['criteria_id'], unique=False, schema='service_algorithm_analysis')
    op.create_table('input',
    sa.Column('input_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('algorithm_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('input_type', sa.String(length=10), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['algorithm_id'], ['service_algorithm_analysis.algorithm.algorithm_id'], ),
    sa.PrimaryKeyConstraint('input_id'),
    schema='service_algorithm_analysis'
    )
    op.create_index('idx_input_algorithm', 'input', ['algorithm_id'], unique=False, schema='service_algorithm_analysis')
    op.create_table('execution',
    sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('algorithm_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('alias', sa.String(length=100), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['algorithm_id'], ['service_algorithm_analysis.algorithm.algorithm_id'], ),
    sa.PrimaryKeyConstraint('execution_id'),
    schema='service_algorithm_analysis'
    )
    op.create_index('idx_execution_algorithm', 'execution', ['algorithm_id'], unique=False, schema='service_algorithm_analysis')
    op.create_table('payload',
    sa.Column('payload_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('input_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('input_value', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['input_id'], ['service_algorithm_analysis.input.input_id'], ),
    sa.ForeignKeyConstraint(['execution_id'], ['service_algorithm_analysis.execution.execution_id'], ),
    sa.PrimaryKeyConstraint('payload_id'),
    schema='service_algorithm_analysis'
    )
    op.create_index('idx_payload_input', 'payload', ['input_id'], unique=False, schema='service_algorithm_analysis')
    op.create_index('idx_payload_execution', 'payload', ['execution_id'], unique=False, schema='service_algorithm_analysis')
    op.create_table('result',
    sa.Column('result_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('execution_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('criteria_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('value', sa.String(length=50), nullable=True),
    sa.Column('unit', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['criteria_id'], ['service_algorithm_analysis.criteria.criteria_id'], ),
    sa.ForeignKeyConstraint(['execution_id'], ['service_algorithm_analysis.execution.execution_id'], ),
    sa.PrimaryKeyConstraint('result_id'),
    schema='service_algorithm_analysis'
    )
    op.create_index('idx_result_criteria', 'result', ['criteria_id'], unique=False, schema='service_algorithm_analysis')
    op.create_index('idx_result_execution', 'result', ['execution_id'], unique=False, schema='service_algorithm_analysis')    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_result_execution', table_name='result', schema='service_algorithm_analysis')
    op.drop_index('idx_result_criteria', table_name='result', schema='service_algorithm_analysis')
    op.drop_table('result', schema='service_algorithm_analysis')
    op.drop_index('idx_payload_execution', table_name='payload', schema='service_algorithm_analysis')
    op.drop_index('idx_payload_input', table_name='payload', schema='service_algorithm_analysis')
    op.drop_table('payload', schema='service_algorithm_analysis')
    op.drop_index('idx_execution_algorithm', table_name='execution', schema='service_algorithm_analysis')
    op.drop_table('execution', schema='service_algorithm_analysis')
    op.drop_index('idx_input_algorithm', table_name='input', schema='service_algorithm_analysis')
    op.drop_table('input', schema='service_algorithm_analysis')
    op.drop_index('idx_criteria_algorithm_criteria', table_name='algorithm_criteria', schema='service_algorithm_analysis')
    op.drop_index('idx_algorithm_criteria_algorithm', table_name='algorithm_criteria', schema='service_algorithm_analysis')
    op.drop_table('algorithm_criteria', schema='service_algorithm_analysis')
    op.drop_table('criteria', schema='service_algorithm_analysis')
    op.drop_table('algorithm', schema='service_algorithm_analysis')
    # ### end Alembic commands ###
