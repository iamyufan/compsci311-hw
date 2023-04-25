# WebMaze

CompSci 311 (SP23), Duke Kunshan University

[Yufan Zhang](http://yufanbruce.com) (NetID: yz605)

---

WebMaze is a client-server pair implemented using remote procedure calls (RPCs) through a REST interface. The project consists of a Web server and a client to allow execution of your NetMaze client and report statistics.

## Getting Started

### Prerequisites

- Python 3.6 or later

- Flask (install using pip install flask)

### Start the server

To start the server, run the following command:

```bash
python3 server.py
```

This will output the following in your terminal:

![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-30-19-image.png)

The server will start on `http://localhost:5000` by default. You can change the host and port by modifying the `app.run()` statement in `server.py`.

### Running the Client

The client program is a command-line tool that issues REST requests toward the server. Here's how to use it:

```bash
python3 client.py <host_address> <port> <action> [<args>]
```

- `host_address`: The address of the REST API server.
- `port`: The port of the REST API server.
- `action`: The command to execute. Valid commands are:
  - `submit [--id <id>]`: Run a NetMaze client with the given ID.
  - `queries [--runid <runid>] [--limit <limit>] [--start <start>]`: Retrieve the queries of running of the given RunID. The `--limit` and `--start` options are optional and specify the maximum number of runs to return and the starting index of the queries to return, respectively.
  - `list [--limit <limit>] [--start <start>]`: List completed runs. The `--limit` and `--start` options are optional and specify the maximum number of runs to return and the starting index of the runs to return, respectively.
  - `statistics`: Compute the mean and variance of the number of queries across all completed NetMaze runs on the server.

## Example Usage

Here are some examples of how to use the client:

1. Run a NetMaze client with ID `yz605_1`:![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-40-17-image.png)

2. Retrive the queries with RunID `457ab73a-650d-4923-80fe-044ed9f47c91`![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-40-49-image.png)

3. List completed runs with a limit of 10 and starting index of 1:![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-41-44-image.png)

4. Compute the mean and varience of the number of queries across all completed runs:![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-43-07-image.png)

## Web Interface

By opening a web browser and navigate to `http://localhost:5000/`, you can also view a web interface to better manage the runs.

![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-45-11-image.png)

- The home page will display a table with information about each completed run, including its ID, the submission time, and the number of queries of this run.

## Access historical information in file

All completed runs will be stored in the `runs.json` file in the root directory. You can open and view the details of each run.

![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-48-06-image.png)

![](/Users/yufanzhang/Library/Application%20Support/marktext/images/2023-04-25-22-48-20-image.png)

## Contacts

yufan.zhang@duke.edu
[github.com/iamyufan](https://github.com/iamyufanhttps://github.com/iamyufan)
