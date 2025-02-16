"""adding running time criteria

Revision ID: e82ac4f587a0
Revises: 60a7dfa217e7
Create Date: 2025-02-15 22:09:42.561899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e82ac4f587a0'
down_revision = '60a7dfa217e7'
branch_labels = None
depends_on = None


def running_time():
    return {
        'id': '001fe2d3-09a5-4bc0-b891-45d475a4b1bc',
        'name': 'Running Time',
        'desc': 'This criteria measure how efficient an algorithm is with increasing input size. Allows you to predict how the algorithm will perform under real-world conditions.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': 'fd25f834-ac02-4f3e-8ee1-a6accc9b7809',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            },
            {
                'id': 'd2c994de-5645-475c-b4db-9b71b2d6a6ce',
                'alg_id': '0192919b-2501-2fea-a93d-5d5541c4002b',  # factorial 
            }
        ]
    }

def upgrade():
    values = []
    values.append(running_time())
    cols_c = f"""criteria_id, name, description, created_at, updated_at, enabled"""
    cols_a = f"""algorithm_criteria_id, algorithm_id, criteria_id, created_at, updated_at, enabled"""
    for v in values:
        vals = f"""('{v['id']}','{v['name']}','{v['desc']}','{v['dt']}','{v['dt']}',{True})"""
        op.execute(f"""INSERT INTO service_algorithm_analysis.criteria({cols_c}) VALUES {vals}""")
        for vv in v['algorithms']:
            vals = f"""('{vv['id']}','{vv['alg_id']}','{v['id']}','{v['dt']}','{v['dt']}',{True})"""
            op.execute(f"""INSERT INTO service_algorithm_analysis.algorithm_criteria({cols_a}) VALUES {vals}""")


def downgrade():
    values = []
    values.append(running_time())
    a_ids = [v['id'] for v in values]
    a_ids = a_ids if len(a_ids) > 1 else a_ids*2
    a_ids = tuple(a_ids)
    op.execute(f"""DELETE FROM service_algorithm_analysis.algorithm_criteria WHERE criteria_id in {a_ids}""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.criteria WHERE criteria_id in {a_ids}""")
