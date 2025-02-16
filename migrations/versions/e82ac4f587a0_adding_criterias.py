"""adding criterias

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
        'desc': 'Measures the time taken by the algorithm to complete its execution from start to finish for a given input.',
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

def memory_consume():
    return {
        'id': 'f6465865-d1a3-496c-82b7-5d7d67adf927',
        'name': 'Memory Consume',
        'desc': 'Measures the total amount of memory used by the algorithm during its execution, including both static and dynamic allocations.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': '09f3b4a8-14cb-4b41-8e97-d400eea77285',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            },
            {
                'id': '89474b4c-6569-49dc-a68d-7fde8f718187',
                'alg_id': '0192919b-2501-2fea-a93d-5d5541c4002b',  # factorial
            }
        ]
    }

def setup_time():
    return {
        'id': '92771dd3-811d-43d3-ad9a-adc2a2c672db',
        'name': 'Setup Time',
        'desc': 'Measures the time taken to initialize any data structures or prerequisites before running the algorithm.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': '1e740c1b-1ea6-4c0f-bcba-fb939890bc60',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            }
        ]
    }

def upgrade():
    values = []
    values.append(running_time())
    values.append(memory_consume())
    values.append(setup_time())
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
    values.append(memory_consume())
    values.append(setup_time())
    c_ids = [v['id'] for v in values]
    c_ids = tuple(c_ids)
    report_id = f"""SELECT report_id FROM service_algorithm_analysis.result WHERE criteria_id in {c_ids}"""
    op.execute(f"""DELETE FROM service_algorithm_analysis.result WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.payload WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.report WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.algorithm_criteria WHERE criteria_id in {c_ids}""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.criteria WHERE criteria_id in {c_ids}""")
