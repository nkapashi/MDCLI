import requests
import json
import re

class node(object):
    headers = {'Content-type': 'application/json'}
    errorMessage = True
    
    @staticmethod
    def getjson(payload, url):
        try:
            jsonData = requests.request("POST", url, json=payload, headers=node.headers)
            return jsonData.json()
        except requests.exceptions.RequestException as e:
            print(e)
            return {'message':'error'}
        except ValueError: 
            return {'message':'error'}
    
class json_rpc_node(node):
    payload = {"jsonrpc":"2.0", "id":"0", "method":None, "params":None}
    
    def __init__(self, host, port):
        self.url = 'http://'+host+':'+port+'/json_rpc'
        
    def get_info(self):
        """General statistics about a monero node
        Args: None
        Returns:
            dict: Current network block height and varous node stats.
        """
        self.method = "get_info"
        self.payload = json_rpc_node.payload
        self.payload['method']=self.method
        self.respData = node.getjson(self.payload, self.url).get('result')
        try:
            self.resultDict = {'netHeight':self.respData['target_height'], \
                                 'nodeHeight':self.respData['height'], \
                                 'diff': self.respData['target_height'] - self.respData['height'], \
                                 'startTime': self.respData['start_time'], \
                                 'connectionsIn': self.respData['incoming_connections_count'],\
                                 'connecionsOut': self.respData['outgoing_connections_count'], \
                                 'connectionsRpc': self.respData['rpc_connections_count'], \
                                 'netHash': int(self.respData['difficulty'] / 120 / 1000000), \
                                 'status': ('OFFLINE' if self.respData['offline'] else 'ONLINE' ), \
                                 'tx_pool':self.respData['tx_pool_size'] }            
            return self.resultDict
        except (KeyError, TypeError):
            return node.errorMessage
            
    def connections(self):
        """Return inbound and outbound connections along with the block height of connected nodes.
        Args: None
        Returns:
            dict: For sucess, bool otherwise.
                key "outgoing" with value list of tuples having ip address[0] and block height[1].
                key "incoming" with value list of tuples having ip address[0] and block height[1].
        """
        self.method = "get_connections"
        self.payload = json_rpc_node.payload
        self.payload['method']=self.method
        self.respData = node.getjson(self.payload, self.url).get('result')
        self.ipv4OutList = []
        self.ipv4InList = []
        self.resultDict={}
        try:
            for ipv4 in self.respData['connections']:
                if ipv4['incoming'] == False:
                    self.ipv4OutList.append((ipv4['host'], ipv4['height']))
                else:
                    self.ipv4InList.append((ipv4['host'], ipv4['height']))
            self.resultDict['outgoing'] = self.ipv4OutList
            self.resultDict['incoming'] = self.ipv4InList
            return self.resultDict
        except (KeyError, TypeError):
            return node.errorMessage
               
    def blockSummary(self, height):
        """Returns various details about block in the chain.
        Args:
            height (int): The height of the block.
        Returns:
            dict: Dict for sucess. bool otherwise.
        """
        self.height = height
        self.method = "getblock"
        self.params = {"height":self.height}
        self.payload = json_rpc_node.payload
        self.payload['method']=self.method
        self.payload['params']=self.params
        self.respData = node.getjson(self.payload, self.url).get('result')
        try:
            self.resultDict = {'height':self.respData['block_header']['height'], \
                               'size':self.respData['block_header']['block_size'], \
                               'txCount':self.respData['block_header']['num_txes'], \
                               'timetamp':self.respData['block_header']['timestamp'], \
                               'nonce':self.respData['block_header']['nonce'], \
                               'block_hash':self.respData['block_header']['hash'], \
                               'block_reward':self.respData['block_header']['reward'], \
                               'tx_hashes': self.respData.get('tx_hashes', [])}
            return self.resultDict
        except (KeyError, TypeError):
            return node.errorMessage
        
class json_node(node):
    
        def __init__(self, host, port):
            self.url = 'http://'+host+':'+port+'/'
        
        def getTransaction(self, transaction):
            """Returns transaction details.
            Args:
                (str): Transaction Id.
            Returns:
                dict: Dict with transaction details for sucess. Otherwise bool.
            """
            self.payload = {"txs_hashes":[transaction], "decode_as_json": True}
            self.response = node.getjson(self.payload, self.url+'gettransactions')
            self.resultDict = {}
            self.inputsList = []
            self.outputsList = []
            try:
                self.tx_json = json.loads(self.response['txs_as_json'][0])
                self.resultDict['inPool'] = self.response['txs'][0]['in_pool']
                if self.response['txs'][0]['block_height'] == 18446744073709551615:
                    self.resultDict['blockHeight'] = 'Pending'
                else:
                    self.resultDict['blockHeight'] = self.response['txs'][0]['block_height']
                self.resultDict['tx_timestamp'] = self.response['txs'][0]['block_timestamp']
                self.resultDict['txFee'] = self.tx_json['rct_signatures']['txnFee']
                for item in self.tx_json['vin']:
                    self.inputsList.append((item['key']['amount'], item['key']['k_image']))
                self.resultDict['inputs'] = self.inputsList
                for item in self.tx_json['vout']:
                    self.outputsList.append((item['amount'], item['target']['key']))
                self.resultDict['outputs'] = self.outputsList
                return self.resultDict
            except (KeyError, TypeError):
                return node.errorMessage
                          

        def getTx_pool(self):
            """Returns transactions waiting in the transaction pool.
            Args:
            Returns:
                dict: Dict with transaction in the pool and their details.
            """
            self.respData = requests.request("POST", self.url+'get_transaction_pool', headers=node.headers).text
            self.respData = re.sub(r'tx_blob.*', "tx_blob\": false,", self.respData)
            self.respData = re.sub(r'tx_json.*', "tx_json\": false", self.respData)
            # using re to replace rx_blob and tx_json as their contents may have
            # characters that break json deserialization
            self.respData = json.loads(self.respData)
            self.respList = []
            self.resultDict = {}
            try:
                for tx in self.respData['transactions']:
                    tx_dict={}
                    tx_dict['txid'] = tx['id_hash']
                    tx_dict['timestamp'] = tx['receive_time']
                    tx_dict['tx_fee'] = tx['fee']
                    self.respList.append(tx_dict)
                    self.respList = sorted(self.respList, key=lambda k: k['timestamp'])
                    self.resultDict['txPool'] = self.respList
                return self.resultDict
            except (KeyError, TypeError):
                return node.errorMessage