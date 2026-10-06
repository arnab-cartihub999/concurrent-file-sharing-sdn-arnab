# D1 Test Results

## 1. Test Environment

- OS: Ubuntu 24.04
- Mininet: 2.3.0
- SDN Controller: OS-Ken 2.8.1
- Switch: Open vSwitch
- OpenFlow Version: OpenFlow 1.3
- Transport Protocol: TCP
- Server Port: 5000

## 2. Mininet Topology

The D1 implementation uses a Mininet topology consisting of:

- h1: TCP file-sharing client – 10.0.0.1
- h2: TCP file-sharing server – 10.0.0.2
- h3: TCP file-sharing client – 10.0.0.3
- s1: Open vSwitch
- c0: OS-Ken SDN controller

The hosts are connected to the OpenFlow 1.3 switch, which is controlled by the OS-Ken controller.

## 3. Test Cases

### Test Case 1 – Host Connectivity

**Command:**

```text
pingall
