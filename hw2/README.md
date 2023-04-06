# NetMaze - Level 2

CompSci 311 (SP23), Duke Kunshan University

[Yufan Zhang](http://yufanbruce.com) (NetID: yz605)

---

This is an asyncio-based Python program that establishes connections with a remote server at a given host and port. The program connects to the server using two types of connections - primary and secondary. Additionally, the program also acts as a server and listens for incoming connections from the server. The program runs on Python 3.7 or higher and uses asyncio for asynchronous I/O operations.

## Requirements

- Python 3.7 or higher
- asyncio

## Installation

Install the required dependencies using pip:

```
pip install asyncio
```

## Usage

1. Run the program from the command line:

    ```
    python3 main.py
    ```

2. The program receives status messages from the server and prints them to the console.

## Output

The output after running the program should be something like the below.

```bash
vcm@vcm-32999:~/cs311$ python3 main.py 
Connected to server on primary connection
Connected to server on secondary connection to port 51337
Connected to server on secondary connection to port 51344
Connected to server on secondary connection to port 51327
Connected to server on secondary connection to port 51349
Connected to server on secondary connection to port 51333
Connected to server on secondary connection to port 51318
Connected to server on secondary connection to port 51347
Connected to server on secondary connection to port 51311
Connected to server on secondary connection to port 51308
Connected to server on secondary connection to port 51329
Connected to server on secondary connection to port 51345
Connected to server on secondary connection to port 51338
Connected to server on secondary connection to port 51320
Connected to server on secondary connection to port 51302
Connected to server on secondary connection to port 51321
Connected to server on secondary connection to port 51338 (visited)
> Listening on port 51426: server established
> Listening on port 51426: received message query 51329
Connected to server on secondary connection to port 51329 (visited)
> Listening on port 51426: received message query 51318
Connected to server on secondary connection to port 51318 (visited)
> Listening on port 51420: server established
> Listening on port 51420: received message query 51350
Connected to server on secondary connection to port 51350
Connected to server on secondary connection to port 51336
Connected to server on secondary connection to port 51327 (visited)
> Listening on port 51450: server established
> Listening on port 51420: received message query 51347
Connected to server on secondary connection to port 51347 (visited)
Connected to server on secondary connection to port 51335
Connected to server on secondary connection to port 51325
Connected to server on secondary connection to port 51317
Connected to server on secondary connection to port 51346
Connected to server on secondary connection to port 51328
> Listening on port 51450: received message query 51312
Connected to server on secondary connection to port 51312
Connected to server on secondary connection to port 51318 (visited)
> Listening on port 51421: server established
Connected to server on secondary connection to port 51322
Connected to server on secondary connection to port 51319
Connected to server on secondary connection to port 51326
Connected to server on secondary connection to port 51307
Connected to server on secondary connection to port 51313
Connected to server on secondary connection to port 51327 (visited)
> Listening on port 51450: received message query 51340
Connected to server on secondary connection to port 51340
Connected to server on secondary connection to port 51346 (visited)
> Listening on port 51421: received message query 51309
Connected to server on secondary connection to port 51309
Connected to server on secondary connection to port 51310
Connected to server on secondary connection to port 51313 (visited)
Connected to server on secondary connection to port 51334
Connected to server on secondary connection to port 51322 (visited)
Connected to server on secondary connection to port 51306
Connected to server on secondary connection to port 51349 (visited)
Connected to server on secondary connection to port 51311 (visited)
Connected to server on secondary connection to port 51307 (visited)
> Listening on port 51410: server established
Connected to server on secondary connection to port 51310 (visited)
Connected to server on secondary connection to port 51345 (visited)
> Listening on port 51421: received message query 51320
Connected to server on secondary connection to port 51320 (visited)
Connected to server on secondary connection to port 51335 (visited)
Connected to server on secondary connection to port 51303
Connected to server on secondary connection to port 51326 (visited)
Connected to server on secondary connection to port 51320 (visited)
> Listening on port 51410: received message query 51306
Connected to server on secondary connection to port 51306 (visited)
Connected to server on secondary connection to port 51316
Connected to server on secondary connection to port 51335 (visited)
Connected to server on secondary connection to port 51319 (visited)
Connected to server on secondary connection to port 51328 (visited)
Connected to server on secondary connection to port 51310 (visited)
Connected to server on secondary connection to port 51309 (visited)
Connected to server on secondary connection to port 51329 (visited)
Connected to server on secondary connection to port 51344 (visited)
Connected to server on secondary connection to port 51332
> Listening on port 51410: received message query 51303
Connected to server on secondary connection to port 51303 (visited)
Connected to server on secondary connection to port 51326 (visited)
Connected to server on secondary connection to port 51337 (visited)
Connected to server on secondary connection to port 51321 (visited)
Connected to server on secondary connection to port 51338 (visited)
Connected to server on secondary connection to port 51327 (visited)
Connected to server on secondary connection to port 51314
Connected to server on secondary connection to port 51327 (visited)
Connected to server on secondary connection to port 51311 (visited)
Connected to server on secondary connection to port 51325 (visited)
Connected to server on secondary connection to port 51316 (visited)
Connected to server on secondary connection to port 51307 (visited)
Connected to server on secondary connection to port 51333 (visited)
Connected to server on secondary connection to port 51327 (visited)
Connected to server on secondary connection to port 51346 (visited)
Connected to server on secondary connection to port 51320 (visited)
Connected to server on secondary connection to port 51329 (visited)
Connected to server on secondary connection to port 51315
Connected to server on secondary connection to port 51314 (visited)
Connected to server on secondary connection to port 51314 (visited)
Connected to server on secondary connection to port 51319 (visited)
Connected to server on secondary connection to port 51309 (visited)
Connected to server on secondary connection to port 51340 (visited)
Connected to server on secondary connection to port 51323
Connected to server on secondary connection to port 51330
Connected to server on secondary connection to port 51306 (visited)
Connected to server on secondary connection to port 51309 (visited)
Connected to server on secondary connection to port 51303 (visited)
Received status message: status success
The connected ports are: [51337, 51344, 51327, 51349, 51333, 51318, 51347, 51311, 51308, 51329, 51345, 51338, 51320, 51302, 51321, 51350, 51336, 51335, 51325, 51317, 51346, 51328, 51312, 51322, 51319, 51326, 51307, 51313, 51340, 51309, 51310, 51334, 51306, 51303, 51316, 51332, 51314, 51315, 51323, 51330]
The listening ports are: [51426, 51420, 51450, 51421, 51410]
```


## Contacts

[yufan.zhang@duke.edu](mailto:yufan.zhang@duke.edu)

[github.com/iamyufan](https://www.github.com/iamyufan)