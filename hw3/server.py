from flask import Flask, jsonify, request, render_template
import uuid
from runNetMaze import get_query_list
import json
from datetime import datetime

app = Flask(__name__)

# In-memory storage for run information
runs = {}


@app.route('/api/run/<string:id>', methods=['POST'])
def run_netmaze(id):
    run_id = str(uuid.uuid4())
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')

    runs[run_id] = {
        'id': id,
        'queries': [],
        'count': None,
        'submit_time': timestamp
    }

    query_list = get_query_list(input_id=id)

    runs[run_id]['queries'] = query_list
    runs[run_id]['count'] = len(query_list)

    with open('runs.json', 'w') as f:
        json.dump(runs, f)

    response = {
        'runId': run_id
    }

    return jsonify(response)


@app.route('/api/queries', methods=['GET'])
def get_query():
    run_id = request.args.get('run', None)
    limit = int(request.args.get('limit', 30))
    start = int(request.args.get('start', 1))

    # Error handling
    if run_id not in runs:
        return '', 204
    if (limit > 30):
        return "HTTP Error 400"

    # Get query list of the given runid
    queries = runs[run_id]['queries']
    paginated_queries = queries[start - 1:start - 1 + limit]

    # Generate the response
    response = {
        'runId': run_id,
        'limit': limit,
        'start': start,
        'queries': paginated_queries,
        'prev': None if start == 1 else f'/api/queries?run={run_id}&limit={limit}&start={start - limit}',
        'next': None if start + limit > len(queries) else f'/api/queries?run={run_id}&limit={limit}&start={start + limit}'
    }

    return jsonify(response)


@app.route('/api/list', methods=['GET'])
def get_run_list():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 1))

    # Error handling
    if limit > 30:
        return '', 400

    # Get the list of runids
    run_ids = list(runs.keys())
    paginated_run_ids = run_ids[start - 1:start - 1 + limit]

    # Generate the response
    response = {
        'limit': limit,
        'start': start,
        'runIds': paginated_run_ids,
        'prev': None if start == 1 else f'/api/list?limit={limit}&start={start - limit}',
        'next': None if start + limit > len(run_ids) else f'/api/list?limit={limit}&start={start + limit}'
    }

    return jsonify(response)


@app.route('/')
def index():
    with open('runs.json', 'r') as f:
        runs = json.load(f).values()

    return render_template('index.html', runs=runs)


if __name__ == '__main__':
    app.run()
