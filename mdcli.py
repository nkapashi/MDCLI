from monerdnode import node, utils
from os import linesep
import argparse

devider = 1000000000000

def getStats():
    jsonRpc = mynode.get_info()
    utils.assertToExit(jsonRpc)
    statsRows = []
    statsRows.append(("NODE STATS", jsonRpc['status']))
    statsRows.append(("UPTIME", str(utils.calcUptime(jsonRpc['startTime'])[0])))
    statsRows.append(("Node Block Height", str(jsonRpc['nodeHeight'])))
    statsRows.append(("Blocks to catch-up", str(jsonRpc['diff']) if jsonRpc['diff'] > 0 \
                      else 'NA' if jsonRpc['status'] == 'OFFLINE' else '*SYNCED*'))
    statsRows.append(("Outbound Connections", str(jsonRpc['connecionsOut'])))
    statsRows.append(("Inbound Connections", str(jsonRpc['connectionsIn'])))
    utils.print_table(statsRows)
    print(linesep)
    
def getlastBlocks(numOfBlocks=6):
    jsonRpc = mynode.get_info()
    utils.assertToExit(jsonRpc)
    lastBlocksRows = []
    lastBlocksRows.append(('BLOCK HEIGHT','TX COUNT', 'SIZE(bytes)', 'TIME'))
    for tx in reversed(range(jsonRpc['nodeHeight'] - numOfBlocks, jsonRpc['nodeHeight'] -1)):
        blockData = mynode.blockSummary(tx)
        try:
            lastBlocksRows.append((str(blockData['height']), str(blockData['txCount']),  
                                   str(blockData['size'] // 1024), utils.fromUnixTime(blockData['timetamp'])))
        except KeyError:
            lastBlocksRows.append(('--', '--', '--', '--'))
    utils.print_table(lastBlocksRows)
    print(linesep)
    
def getNetStats():
    jsonRpc = mynode.get_info()
    utils.assertToExit(jsonRpc)
    netRows = []
    netRows.append(("Network Hash",str(jsonRpc['netHash']) + ' Mh\s'))
    netRows.append(("TX POOL SIZE",str(jsonRpc['tx_pool'])))
    utils.print_table(netRows)
    print(linesep)
    
def getConnections():
    jsonRpc = mynode.connections()
    utils.assertToExit(jsonRpc)
    outgoingHostsRow = []
    incomingHostsRow = []
    outgoingHostsRow.append(("#", "OUTBOUND HOST", "HEIGHT"))
    incomingHostsRow.append(("#", "INBOUND HOST", "HEIGHT"))
    try:
        if len(jsonRpc['outgoing']) > 0:
            for i,host in enumerate(jsonRpc['outgoing']):
                outgoingHostsRow.append((str(i + 1), host[0], str(host[1])))
        else:
            outgoingHostsRow.append(("--", "NO CONNECTIONS", "--"))
    except KeyError:
        outgoingHostsRow.append(("--", "NO CONNECTIONS", "--"))
    try:
        if len(jsonRpc['incoming']) > 0:
            for i,host in enumerate(jsonRpc['incoming']):
                incomingHostsRow.append((str(i + 1), host[0], str(host[1])))
        else:
            incomingHostsRow.append(("--", "NO CONNECTIONS", "--"))
    except KeyError:
        incomingHostsRow.append(("--", "NO CONNECTIONS", "--"))
    utils.print_table(incomingHostsRow)
    print(linesep)
    utils.print_table(outgoingHostsRow)
    print(linesep)

def getTxPool():
    txPoolData = myJsonNode.getTx_pool()
    utils.assertToExit(txPoolData)
    txPoolRows = []
    txPoolRows.append(("#","tx_id", "time", "fee"))
    for i, item in enumerate(reversed(txPoolData['txPool'])):
        txPoolRows.append((str(i + 1),
                       item['txid'], utils.fromUnixTime(item['timestamp']), str(item['tx_fee'] / devider)))
    utils.print_table(txPoolRows)
    print(linesep)

def getTX():
    if args.value == None:
        tx = input("Enter tx id: " ).strip()
    else:
        tx = args.value
    txDetails = myJsonNode.getTransaction(tx)
    utils.assertToExit(txDetails)
    txHashRowsDetal = []
    txInputs = []
    txOutputs = []
    txHashRowsDetal.append(('txTime', 'txBlockHeight', 'txInPool', 'txFee'))
    txInputs.append(('Amount', 'Key Image'))
    txOutputs.append(('Amount', 'Public Key'))
    txHashRowsDetal.append((utils.fromUnixTime(txDetails['tx_timestamp']), str(txDetails['blockHeight']), str(txDetails['inPool']), str(txDetails['txFee'] / devider)))
    for tx_input in txDetails['inputs']:
        txInputs.append((str(tx_input[0]), str(tx_input[1])))
    for tx_output in txDetails['outputs']:
        txOutputs.append((str(tx_output[0]), str(tx_output[1])))
    utils.print_table(txHashRowsDetal)
    print(linesep)
    utils.print_table(txInputs)
    print(linesep)
    utils.print_table(txOutputs)
    print(linesep)
    
def getBlock():
    if args.value == None:
        blockH = input("Enter block height: " ).strip()
    else:
        blockH = args.value
    jsonRpc = mynode.blockSummary(blockH)
    utils.assertToExit(jsonRpc)
    blockHDetails = []
    blockHDetails.append(("BLOCK #", str(jsonRpc['height'])))
    blockHDetails.append(("Hash", jsonRpc['block_hash']))
    blockHDetails.append(("Timestamp", utils.fromUnixTime(jsonRpc['timetamp'])))
    blockHDetails.append(("Block Reward", str(round(jsonRpc['block_reward'] / devider, 3))))
    blockHDetails.append(("Block Size (kbytes)", str(int(jsonRpc['size'] / 1024))))
    blockHDetails.append(('Transactions #', str(jsonRpc['txCount'])))
    blockTXs=[]
    blockTXs.append(("#", "tx_id"))
    if len(jsonRpc['tx_hashes']) > 0:
        for n,tx in enumerate(jsonRpc['tx_hashes']):
            blockTXs.append((str(n + 1), tx))
    else:
         blockTXs.append(("--", "--"))        
    utils.print_table(blockHDetails)
    print(linesep)
    utils.print_table(blockTXs)
    print(linesep)
                          
    
functions = {'stats' : getStats , 'blocks': getlastBlocks, 'netstat' : getNetStats, 
              'connections' : getConnections, 'txpool' : getTxPool, 'tx' : getTX, 'get_block' : getBlock}
parser = argparse.ArgumentParser()
parser.add_argument('--node-address', default="127.0.0.1:18081", help=' Default localhost. Specify the node address \
                    and port number. Example: 172.17.0.2:18081.')
parser.add_argument('--cmd', nargs='+', required=True, choices=functions.keys(), help='Sepcify command to execute. \
                Multiple command are supported. Example --cmd stats connetions')
parser.add_argument('--value', help='Sepcify block height or transaction id', default=None)
args = parser.parse_args()
mynode=node.json_rpc_node(args.node_address.split(':')[0], args.node_address.split(':')[1])
myJsonNode=node.json_node(args.node_address.split(':')[0], args.node_address.split(':')[1])
print(linesep)
for cmd in args.cmd:
    func = functions[cmd]
    func()