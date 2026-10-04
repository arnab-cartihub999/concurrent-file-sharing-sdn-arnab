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

```text
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
