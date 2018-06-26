# MDCLI

Command line client tool for bitmonerod RPC calls. With mdcli you can:

- Get statistics about your monero node such as sync status, inbound and outbound connections, and network stats such as network hash rate and tx pool size. 

- Use your monerod node as block explorer - query transactions and block details.

  

  **Examples:**

  Show node statistics such as uptime, current block height, block to sync, total number of inbound and outbound connections. 

  ```
  >mdcli.exe --node-address 172.17.0.7:18081 --cmd stats
  
  NODE STATS           | ONLINE
  ---------------------------------
  UPTIME               | 0d, 0h, 2m
  Node Block Height    | 1587762
  Blocks to catch-up   | 13204
  Outbound Connections | 8
  Inbound Connections  | 0
  ```

  Show details about inbound and outbound connections. The ip address of incoming and outgoing nodes and their block height.

  ```
  >mdcli.exe --node-address 172.17.0.7:18081 --cmd connections
  
  # | INBOUND HOST | HEIGHT
  --------------------------
  1 | 172.12.X.X   | 1601064
  
  # | OUTBOUND HOST  | HEIGHT
  ----------------------------
  1 | 87.9X.1XX.XXX  | 1601064
  2 | 8X.1XX.2XX.XXX | 1601064
  3 | 104.46.113.48  | 1601064
  4 | X6.9.XX.X3     | 1470452
  5 | X7.XX.X9.X     | 1601064
  6 | 1XX.XX0.XXX.X2 | 1601064
  7 | XXX.164.X1.XX  | 1601064
  8 | XX.X1.1XX.XX   | 1601064
  ```

  Network hash rate and size of the transaction pool.

  ```
  >mdcli.exe --node-address 172.17.0.7:18081 --cmd netstat 
  
  Network Hash | 405 Mh\s
  -----------------------
  TX POOL SIZE | 4
  ```

  Print the transactions in tx pool, their time and fee

  ```
  >mdcli.exe --node-address 172.17.0.7:18081 --cmd txpool
  
  # | tx_id                                                            | time            | fee
  --------------------------------------------------------------------------------------------------
  1 | XXX5c74f22ec7XXXXXXXXXXXXXXXXX2946a3b53c6ae646dc8d9ef6bfed29b55c | 22-Jun-18 21:46 | 0.0024
  ```

  Help for the options is available too.

  ```
  usage: mdcli.exe [-h] [--node-address NODE_ADDRESS] --cmd
                   {stats,blocks,netstat,connections,txpool,tx,get_block}
                   [{stats,blocks,netstat,connections,txpool,tx,get_block} ...]
                   [--value VALUE]
  
  optional arguments:
    -h, --help            show this help message and exit
    --node-address NODE_ADDRESS
                          Default localhost. Specify the node address and port
                          number. Example: 172.17.0.2:18081.
    --cmd {stats,blocks,netstat,connections,txpool,tx,get_block} [{stats,blocks,netstat,connections,txpool,tx,get_block} ...]
                          Sepcify command to execute. Multiple command are
                          supported. Example --cmd stats connetions
    --value VALUE         Sepcify block height or transaction id
  ```

  

## Getting Started

To run the code simply download all files in this repository and run  *python mdcli --cmd* 

### Prerequisites

You need **Python 3.6.3 or newer.**  Older versions will not work due to the use of f-strings. Prebuild binaries are also available. Still the better option is to run directly the python code or build to executable with cx_Freeze.

### Compiling

Compile your own executable with cx_Freeze:

```
python setup.py build
```
### Binary releases

Binary releases are available for Windows and Linux. The binary is known to run on Windows 10 and on Ubuntu 17.x and 18.x. It requires **glibc 2.25 or higher**. You may need to install **libexpat.so.1** in case you are running a very minimal installation.

```
apt-get install libexpat1
```

## Versioning

More to follow...

