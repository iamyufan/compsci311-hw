import socket
import argparse
import json
import statistics


def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(request.encode())
        response = b''
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

    return response.decode()


def parse_response(response):
    header, body = response.split('\r\n\r\n', 1)
    header_lines = header.split('\r\n')
    headers = {}
    for line in header_lines[1:]:
        key, value = line.split(': ')
        headers[key] = value
    content_length = int(headers['Content-Length'])
    return json.loads(body[:content_length])


def build_request(host, method, path, body=None):
    request = f"{method} {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    if body:
        request += f"Content-Length: {len(body)}\r\n"
        request += "Content-Type: application/json\r\n"
    request += "Connection: close\r\n"
    request += "\r\n"
    if body:
        request += body
    return request


def handle_post(action, host, port, id):
    if action == 'submit':
        path = f'/api/run/{id}'
        # print(f"POST path: {path}")
        request = build_request(host, 'POST', path)
        response = send_request(host, port, request)
        parsed_response = parse_response(response)
    return parsed_response


def handle_get(action, host, port, start, limit, runid=None):
    if action == 'queries':
        path = f"/api/queries?run={runid}&limit={limit}&start={start}"
    elif action == 'list':
        path = f"/api/list?limit={limit}&start={start}"
    # print(f"GET path: {path}")
    request = build_request(host, 'GET', path)
    response = send_request(host, port, request)
    parsed_response = parse_response(response)
    return parsed_response


def get_all_run_ids(host, port):
    run_ids = []
    limit = 30
    start = 1
    while True:
        response = handle_get('list', host, port, start=start, limit=limit)
        run_ids.extend(response['runIds'])
        if response['next'] is None:
            break
        start += limit
    return run_ids


def count_qeuries(host, port, runid):
    sum = 0
    limit = 30
    start = 1
    while True:
        response = handle_get('queries', host, port,
                              start=start, limit=limit, runid=runid)
        sum += len(response['queries'])
        if response['next'] is None:
            break
        start += limit
    return sum


def handle_statistics(host, port):
    run_ids = get_all_run_ids(host, port)
    print(f'run_ids: {run_ids}')

    queries_count = []
    for run_id in run_ids:
        count = count_qeuries(host, port, run_id)
        queries_count.append(count)

    mean = statistics.mean(queries_count)
    variance = statistics.variance(queries_count)

    response = {
        'mean': mean,
        'variance': variance
    }

    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host", default="http://127.0.0.1",
                        help="Hostname of the server")
    parser.add_argument("port", default="5000", type=int,
                        help="Port of the server")
    parser.add_argument("action", choices=[
                        "submit", "queries", "list", "statistics"], help="Action to perform")
    parser.add_argument("--id", help="ID for submit action")
    parser.add_argument("--start", type=int, default=1,
                        help="Start index for list action")
    parser.add_argument("--limit", type=int, default=10,
                        help="Limit for list action")
    parser.add_argument("--runid", help="RunID for viewing detail")

    args = parser.parse_args()

    if args.action == "submit":
        if not args.id:
            print("ID is required for submit action")
            return
        response = handle_post(args.action, args.host, args.port, args.id)
    elif args.action == "queries":
        if not args.runid:
            print("RunID is required for queries")
            return
        response = handle_get(args.action, args.host,
                              args.port, args.start, args.limit, args.runid)
    elif args.action == "list":
        response = handle_get(args.action, args.host,
                              args.port, args.start, args.limit)
    elif args.action == "statistics":
        response = handle_statistics(args.host, args.port)
    print(response)


if __name__ == "__main__":
    main()
