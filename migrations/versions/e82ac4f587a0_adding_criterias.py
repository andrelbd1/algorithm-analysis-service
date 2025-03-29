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
            },
            {
                'id': '019533ba-7e43-2f2e-0c83-75ffb2b27398',
                'alg_id': '0195316b-d5ca-431a-8d95-f3f65e3ec1dd',  # fibonacci
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
            },
            {
                'id': '019533b4-fd15-5668-6225-c852d6caa971',
                'alg_id': '0195316b-d5ca-431a-8d95-f3f65e3ec1dd',  # fibonacci
            }
        ]
    }

def count_nodes():
    return {
        'id': '92771dd3-811d-43d3-ad9a-adc2a2c672db',
        'name': 'Count Nodes',
        'desc': 'Count the number of nodes in the graph.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': '499b32f9-e2fc-4eb8-860e-fafdb8145b7f',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            }
        ]
    }

def count_edges():
    return {
        'id': '9f59f0dd-2e0e-4c40-99ad-5f0ba5ac2e32',
        'name': 'Count Edges',
        'desc': 'Count the number of edges in the graph.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': 'afacccde-a1d6-4acd-a152-1428c47027fa',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            }
        ]
    }

def detect_cycle():
    return {
        'id': '3008715f-0d3f-445e-9d58-3bd57ccb681d',
        'name': 'Detect Cycle',
        'desc': 'Identify if there are any cycles within the graph structure.',
        'dt': "2024-10-18 21:08:00",
        'algorithms': [
            {
                'id': '209262a2-1662-4d30-9136-57320f117c9f',
                'alg_id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',  # dijkstra
            }
        ]
    }

def upgrade():
    values = []
    values.append(running_time())
    values.append(memory_consume())
    values.append(count_nodes())
    values.append(count_edges())
    values.append(detect_cycle())
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
    values.append(count_nodes())
    values.append(count_edges())
    values.append(detect_cycle())
    c_ids = [v['id'] for v in values]
    c_ids = tuple(c_ids)
    execution_id = f"""SELECT execution_id FROM service_algorithm_analysis.result WHERE criteria_id in {c_ids}"""
    op.execute(f"""DELETE FROM service_algorithm_analysis.result WHERE execution_id in ({execution_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.payload WHERE execution_id in ({execution_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.execution WHERE execution_id in ({execution_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.algorithm_criteria WHERE criteria_id in {c_ids}""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.criteria WHERE criteria_id in {c_ids}""")
