"""
This API grants access to the database tables in this way:
    http://127.0.0.1:5000/table_name/column_name/keyword
"""

import sys
from flask import Flask
from sqlalchemy import create_engine, MetaData, select


database = sys.argv[1]
engine = create_engine(f'sqlite:///{database}')
meta = MetaData(engine)
meta.reflect()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    available = '\n'.join(table for table in engine.table_names())
    return __doc__ + f"\nDatabase tables:\n{available}"

@app.route('/<table>', methods=['GET'])
def get_columns(table):
    reflected_table = meta.tables[table]
    return '\n'.join(column for column in reflected_table.columns.keys())

@app.route('/<table>/<column>', methods=['GET'])
def get_unique_entries(table, column):
    reflected_table = meta.tables[table]
    reflected_column = reflected_table.columns[column]
    values_query = select([reflected_column]).distinct()
    values = values_query.execute().fetchall()
    return '\n'.join(value[0] for value in values)

@app.route('/<table>/<column>/<keyword>', methods=['GET'])
def get_filtered_entries(table, column, keyword):
    reflected_table = meta.tables[table]
    reflected_column = reflected_table.columns[column]
    search_query = select([reflected_table]).where(reflected_column.like(
        f"%{keyword}%"))
    result = search_query.execute().fetchall()
    return '\n'.join(', '.join(line) for line in result)


if __name__ == '__main__':
    app.run(debug=True)
