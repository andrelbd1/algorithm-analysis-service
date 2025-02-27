"""insert dijkstra and factorial

Revision ID: 60a7dfa217e7
Revises: 886facf07954
Create Date: 2024-11-18 20:49:27.187083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60a7dfa217e7'
down_revision = '886facf07954'
branch_labels = None
depends_on = None

def dijkstra():
    return {
        'id': '0192919b-2501-91c1-d4bb-c71b4c0785d5',
        'name': 'Dijkstra',
        'desc': 'A popular search algorithm used to determine the shortest path between two nodes in a graph.',
        'source': 'https://github.com/andrelbd1/algorithms-practice/blob/master/solutions/dijkstra/dijkstra.py',
        'dt': "2024-10-18 21:08:00",
        'input':[
            {
                'id': '0192919b-2501-59d0-d088-50be8a4e5ae6',
                'name': 'number of nodes',
                'input_type': 'integer',
                'description': 'number of nodes to build a random graph'
            },
            {
                'id': '0192919b-2501-3c8d-b7ad-8c470d1bfba6',
                'name': 'number of edges',
                'input_type': 'integer',
                'description': 'number of edges to build a random graph'
            }
        ]
    }    

def factorial():
    return {
        'id': '0192919b-2501-2fea-a93d-5d5541c4002b',
        'name': 'Factorial',
        'desc': 'A mathematical function that multiplies a positive integer by all the positive integers that are less than or equal to it.',
        'source': 'https://github.com/andrelbd1/algorithms-practice/blob/master/solutions/factorial/code.py',
        'dt': "2024-10-18 21:08:00",
        'input':[
            {
                'id': '0192919b-2501-585f-1492-4f5d22c98267',
                'name': 'factorial number',
                'input_type': 'integer',
                'description': 'number to calculate factorial'
            }
        ]
    }

def fibonacci():
    return {
        'id': '0195316b-d5ca-431a-8d95-f3f65e3ec1dd',
        'name': 'Fibonacci sequence',
        'desc': 'The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, starting from 0 and 1.',
        'source': 'https://realpython.com/fibonacci-sequence-python/',
        'dt': "2024-10-18 21:08:00",
        'input':[
            {
                'id': '0195316d-80fc-40c2-b3ca-44a90d8c6851',
                'name': 'fibonacci number',
                'input_type': 'integer',
                'description': 'number to calculate fibonacci sequence'
            }
        ]
    }

def upgrade():
    values = []
    values.append(dijkstra())
    values.append(factorial())
    values.append(fibonacci())
    cols_a = f"""algorithm_id, name, description, source, created_at, updated_at, enabled"""
    cols_i = f"""input_id, algorithm_id, name, description, input_type, created_at, updated_at, enabled"""
    for v in values:
        vals = f"""('{v['id']}','{v['name']}','{v['desc']}','{v['source']}','{v['dt']}','{v['dt']}',{True})"""
        op.execute(f"""INSERT INTO service_algorithm_analysis.algorithm({cols_a}) VALUES {vals}""")
        for vv in v['input']:
            vals = f"""('{vv['id']}','{v['id']}','{vv['name']}','{vv['description']}','{vv['input_type']}','{v['dt']}','{v['dt']}',{True})"""
            op.execute(f"""INSERT INTO service_algorithm_analysis.input({cols_i}) VALUES {vals}""")


def downgrade():
    values = []
    values.append(dijkstra())
    values.append(factorial())
    values.append(fibonacci())
    a_ids = [v['id'] for v in values]
    a_ids = tuple(a_ids)
    report_id = f"""SELECT report_id FROM service_algorithm_analysis.report WHERE algorithm_id in {a_ids}"""
    op.execute(f"""DELETE FROM service_algorithm_analysis.result WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.payload WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.report WHERE report_id in ({report_id})""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.input WHERE algorithm_id in {a_ids}""")
    op.execute(f"""DELETE FROM service_algorithm_analysis.algorithm WHERE algorithm_id in {a_ids}""")
