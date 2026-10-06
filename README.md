# Concurrent File Sharing using TCP Sockets and SDN

## 1. Project Overview

This project implements a multi-user file-sharing application using TCP sockets and an SDN-controlled Mininet network.

The system consists of:
- A TCP file-sharing server
- Multiple TCP clients
- A Mininet-based network topology
- An Open vSwitch (OVS) switch
- An OS-Ken SDN controller
- OpenFlow 1.3 communication between the switch and controller

The server provides file listing and file download functionality to multiple clients concurrently.

---

## 2. Architecture

The implemented network contains three Mininet hosts connected to one Open vSwitch:


             OS-Ken SDN Controller
                    |
              OpenFlow 1.3
                    |
                   s1
              /     |     \
            h1      h2      h3
          Client   Server  Client
                    |
                 TCP :5000

---

## 3. Objectives

The main objectives of the D1 implementation are:

- Implement a TCP-based file-sharing application using low-level Python sockets.
- Support multiple clients communicating with a common file server.
- Deploy the application inside a Mininet-based network.
- Connect the Mininet Open vSwitch to an OS-Ken SDN controller using OpenFlow 1.3.
- Demonstrate end-to-end communication between the socket application and the SDN-controlled network.
- Verify host connectivity, TCP communication, file transfer, and SDN forwarding behavior.

---

## 4. Components and Host Roles

| Component | Role | Address / Port |
|---|---|---|
| h1 | TCP client | 10.0.0.1 |
| h2 | TCP file server | 10.0.0.2:5000 |
| h3 | TCP client | 10.0.0.3 |
| s1 | Open vSwitch | OpenFlow 1.3 |
| c0 | OS-Ken SDN controller | 127.0.0.1:6653 |

### h1 and h3 – Clients

The clients connect to the TCP file server and support:

- `LIST` – list available files
- `DOWNLOAD <filename>` – download a file
- `QUIT` – terminate the client session

### h2 – File Server

The server listens on TCP port `5000`.

It maintains a shared directory and handles client requests using a separate thread for each connected client.

### s1 – Open vSwitch

The Open vSwitch provides the data-plane connectivity between the Mininet hosts.

It communicates with the OS-Ken controller using OpenFlow 1.3.

### c0 – OS-Ken Controller

The OS-Ken controller implements a basic learning-switch function.

It receives Packet-In messages for unknown traffic, learns source MAC addresses, and installs forwarding flows in the switch when the destination is known.

---

## 5. Communication Flow

The normal file-sharing communication flow is:

Client h1 / h3
       |
       | TCP connection
       v
   OVS Switch s1
       |
       | TCP traffic
       v
TCP File Server h2
       |
       | File LIST / DOWNLOAD
       v
   shared_files/

---

## 6. Technologies Used

- Python 3
- TCP sockets
- Python `socket` module
- Python `threading` module
- Mininet 2.3.0
- Open vSwitch (OVS)
- OS-Ken 2.8.1
- OpenFlow 1.3
- Ubuntu 24.04
- Git
- GitHub

---

## 7. Project Structure

concurrent-file-sharing-sdn/
│
├── client.py
├── server.py
├── controller.py
├── topology.py
├── README.md
│
├── docs/
│   ├── D1_TEST_RESULTS.md
│   ├── sdn_architecture.drawio
│   └── sdn_architecture.png
│
├── shared_files/
│   ├── .gitkeep
│   └── test.txt
│
└── .gitignore

|           File                  |            Description                 |
|---------------------------------|----------------------------------------|
|         `client.py`             | TCP client application                 |
|         `server.py`             | Multi-client TCP file-sharing server   |
|        `controller.py`          | OS-Ken OpenFlow 1.3 SDN controller     |
|         `topology.py`           | Mininet topology definition            |
|          `README.md`            | Project documentation                  |
|   `docs/D1_TEST_RESULTS.md`     | D1 test cases and results              |
| `docs/sdn_architecture.drawio`  | Editable architecture diagram          |
|  `docs/sdn_architecture.png`    | Architecture diagram image             |
|       `shared_files/`           | Files available for download           |


---

## 8. Environment Setup

The D1 implementation was tested using:
Ubuntu 24.04
Mininet 2.3.0
OS-Ken 2.8.1
Open vSwitch
OpenFlow 1.3
Python 3


Checking Python: 
python3 --version

Check Mininet:
mn --version

Check OS-Ken:
osken-manager --version

---

## 9. Running the SDN Controller

Open a terminal and move to the project directory:

```bash
cd ~/concurrent-file-sharing-sdn
```

Start the OS-Ken controller:

```bash
osken-manager controller.py
```

The controller should start successfully and wait for the Mininet Open vSwitch to connect.

A successful switch connection produces output similar to:

```text
Switch connected: 1
```

Keep this terminal running while the Mininet network is active.

---

## 10. Starting the Mininet Topology

Open a second terminal:

```bash
cd ~/concurrent-file-sharing-sdn
```

Start the topology:

```bash
sudo python3 topology.py
```

The topology creates:

```text
          OS-Ken Controller
                  |
             OpenFlow 1.3
                  |
                  s1
               /  |  \
              /   |   \
            h1    h2    h3
         Client Server Client
```

Inside the Mininet CLI, test host connectivity:

```text
mininet> pingall
```

Expected result:

```text
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 0% dropped (6/6 received)
```

---

## 11. Running the File Server

Inside the Mininet CLI, start the TCP server on h2:

```text
mininet> h2 python3 /home/arnab999/concurrent-file-sharing-sdn/server.py &
```

The server should display:

```text
File Sharing Server started
Listening on port 5000
```

Verify that the server is listening on TCP port 5000:

```text
mininet> h2 ss -ltn | grep 5000
```

Expected output:

```text
LISTEN 0 5 0.0.0.0:5000 0.0.0.0:*
```

---

## 12. Running the TCP Client

Start the first client on h1:

```text
mininet> h1 python3 /home/arnab999/concurrent-file-sharing-sdn/client.py
```

The client should receive:

```text
Welcome to the File Sharing Server
```

### List Available Files

Enter:

```text
LIST
```

Example output:

```text
.gitkeep
test.txt
```

### Download a File

Enter:

```text
DOWNLOAD test.txt
```

Expected output:

```text
File downloaded successfully
```

### Terminate the Client

Enter:

```text
QUIT
```

The client then returns to the Mininet CLI.

---

## 13. Testing a Second Client

A second client can be started on h3:

```text
mininet> h3 python3 /home/arnab999/concurrent-file-sharing-sdn/client.py
```

The h3 client can perform the same operations:

```text
LIST
DOWNLOAD test.txt
QUIT
```

This demonstrates communication between multiple Mininet client hosts and the same TCP file server.

The server implementation uses a separate thread for each accepted client connection, allowing multiple client sessions to be handled concurrently.

---

## 14. Supported Client Commands

| Command | Description |
|---|---|
| `LIST` | Lists files available on the server |
| `DOWNLOAD <filename>` | Downloads the specified file |
| `QUIT` | Terminates the client session |

---

## 15. TCP Socket Implementation

The application uses Python's low-level TCP socket API.

### Server

The server uses:

```python
socket.AF_INET
socket.SOCK_STREAM
```

The server:

1. Creates a TCP socket.
2. Binds to `0.0.0.0:5000`.
3. Listens for incoming connections.
4. Accepts client connections.
5. Creates a separate thread for each client.
6. Processes application commands.
7. Transfers files in chunks.
8. Closes the client connection when the session ends.

### Client

The client:

1. Creates a TCP socket.
2. Connects to the server at `10.0.0.2:5000`.
3. Sends application commands.
4. Receives server responses.
5. Downloads files in chunks.
6. Terminates using the `QUIT` command.

---

## 16. Testing and Results

The D1 implementation was tested in the Mininet environment.

### Test 1 – Host Connectivity

Command:

```text
mininet> pingall
```

Observed result:

```text
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 0% dropped (6/6 received)
```

**Status: PASS**

---

### Test 2 – TCP Server Startup

The server was started on h2:

```text
mininet> h2 python3 /home/arnab999/concurrent-file-sharing-sdn/server.py &
```

Port verification:

```text
mininet> h2 ss -ltn | grep 5000
```

Observed:

```text
File Sharing Server started
Listening on port 5000
LISTEN 0 5 0.0.0.0:5000 0.0.0.0:*
```

**Status: PASS**

---

### Test 3 – h1 File Listing and Download

The h1 client connected successfully.

The `LIST` command returned:

```text
.gitkeep
test.txt
```

The following command was executed:

```text
DOWNLOAD test.txt
```

Observed result:

```text
File downloaded successfully
```

The session was then terminated using:

```text
QUIT
```

**Status: PASS**

---

### Test 4 – h3 File Listing and Download

The h3 client connected successfully.

The `LIST` command returned the available files.

The following command was executed:

```text
DOWNLOAD test.txt
```

Observed result:

```text
File downloaded successfully
```

The session was then terminated using:

```text
QUIT
```

**Status: PASS**

---

### Test 5 – Multiple Client Communication

Both h1 and h3 were successfully used as TCP clients communicating with the same h2 file server.

The tests verified that:

- Multiple Mininet hosts can connect to the TCP server.
- The server accepts connections from different clients.
- Clients can list files.
- Clients can download the same shared file.
- Client sessions can be terminated using `QUIT`.
- The server uses a separate thread for each accepted client connection.

**Status: PASS**

---

## 17. SDN Flow Verification

After generating traffic between the Mininet hosts, OpenFlow rules can be inspected using:

```text
mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1
```

The switch contains learned forwarding flows between the host interfaces.

Examples observed during testing included:

```text
s1-eth1 -> s1-eth2
s1-eth2 -> s1-eth1
s1-eth3 -> s1-eth1
s1-eth1 -> s1-eth3
s1-eth3 -> s1-eth2
s1-eth2 -> s1-eth3
```

A priority-0 table-miss flow was also present:

```text
priority=0 actions=CONTROLLER:65535
```

This demonstrates that the switch is connected to the OS-Ken controller and that forwarding rules are installed for observed traffic.

---

## 18. Socket–SDN Integration

The TCP file-sharing application runs on the Mininet hosts.

The application traffic travels through the Open vSwitch:

```text
TCP Client
    |
    v
Mininet Host
    |
    v
OVS Switch s1
    |
    v
Mininet Host
    |
    v
TCP Server
```

The SDN control path is separate from the application data path:

```text
                OS-Ken Controller
                       ^
                       |
                   Packet-In
                       |
                       |
                    Flow-Mod
                       |
                       v
                   OVS Switch
```

When traffic does not match an existing forwarding rule, the switch can send a Packet-In message to the controller.

The controller learns MAC addresses and installs forwarding rules using Flow-Mod messages.

Therefore, the D1 implementation demonstrates interaction between:

```text
TCP Socket Application
          +
       Mininet
          +
     Open vSwitch
          +
    OS-Ken Controller
          +
      OpenFlow 1.3
```

---

## 19. D1 Scope

The D1 implementation establishes a working baseline consisting of:

- TCP file-sharing communication
- Multi-client server architecture
- Mininet network deployment
- Open vSwitch switching
- OS-Ken SDN control
- OpenFlow 1.3 communication
- Basic controller-based MAC learning
- End-to-end testing
- OpenFlow flow verification

The D1 controller provides basic learning-switch functionality.

Advanced application-driven SDN behavior is outside the scope of the current D1 implementation.

---

## 20. Future Enhancements / D2

Potential extensions for the next development stage include:

- Dynamic SDN policies
- Application-aware network control
- Traffic monitoring
- Access control and filtering
- Failure and recovery handling
- Performance measurement
- Baseline comparison
- Additional file-sharing functionality
- More advanced SDN-controlled behavior

These enhancements can be developed without changing the basic D1 architecture.

---

## 21. Reproducibility

To reproduce the D1 demonstration:

1. Start the OS-Ken controller.
2. Start the Mininet topology.
3. Run `pingall`.
4. Start the TCP server on h2.
5. Start a client on h1 or h3.
6. Run `LIST`.
7. Run `DOWNLOAD test.txt`.
8. Run `QUIT`.
9. Inspect the OpenFlow flows on s1.

The complete source code, topology, architecture diagrams, and D1 test results are included in this repository.

---

## 22. Documentation

Additional project documentation is available in the `docs/` directory.

### D1 Test Results

```text
docs/D1_TEST_RESULTS.md
```

This document contains the detailed D1 test cases, commands, observed results, and pass/fail status.

### Architecture Diagram

Editable diagram:

```text
docs/sdn_architecture.drawio
```

PNG version:

```text
docs/sdn_architecture.png
```

---

## 23. Conclusion

The D1 implementation provides a working concurrent TCP file-sharing application deployed over an SDN-controlled Mininet network.

The demonstrated system successfully combines:

- Low-level TCP socket programming
- Threaded client handling
- Mininet
- Open vSwitch
- OS-Ken
- OpenFlow 1.3
- End-to-end file transfer
- Multiple client hosts
- SDN-based forwarding

The implementation provides a stable baseline for further development in D2.




















