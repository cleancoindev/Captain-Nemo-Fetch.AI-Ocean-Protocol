from web3.auto import Web3
import time
import requests
import json



def create_ocean_request(query):
    pass

def process_response(response):
    pass

def prepare_tx(fun):
    nonce = w3.eth.getTransactionCount(account.address)  
    query_txn = fun.buildTransaction({
                'gas': 300000,
                'gasPrice': w3.toWei('1', 'gwei'),
                'nonce': nonce,
    })
    return w3.eth.account.sign_transaction(query_txn, private_key=private_key)

    

def main_loop():
    length = 0
    print('starting agent main loop on address', w3.eth.defaultAccount)
    while True:
        event_filter = contract.events.QueryCreated.createFilter(fromBlock=0)
        


        if length < len(event_filter.get_all_entries()):
            event_args = event_filter.get_all_entries()[-1]["args"]
            command = event_args["command"]
            agentAddress = event_args["agentAddress"]
            oceanDid = event_args["oceanDid"]
            queryContract = event_args["queryContract"]
            print('data', command, agentAddress, oceanDid)
            if agentAddress == w3.eth.defaultAccount:
                time.sleep(2)
                continue
                response = create_ocean_request({"command" : command, "did" : oceanDid})
                result = process_response(response)
                updateQuery = contract.functions.updateQuery(queryContract, result)
            
                signed_txn = prepare_tx(updateQuery)
                w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            
            length += 1# len(event_filter.get_all_entries())#maybe dont need this

        time.sleep(2)




if __name__ == '__main__':

    w3 = Web3(Web3.HTTPProvider("http://localhost:7545"))

    with open('../keystore/UTC--2019-10-19T15-13-02.082157851Z--719b682d53f15899376709fb372c98aa5a116799') as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, 'submarine')

    contract_address = '0x1d803F88DAdDb8aF40124018dD98B0F10f0A248f'
    
    contractAddress = Web3.toChecksumAddress(contract_address)
    account =  w3.eth.account.privateKeyToAccount(private_key)
    w3.eth.defaultAccount = account.address

    #my_address = '0x719b682d53f15899376709fb372c98aa5a116799'

    with open("abi.json") as f:
        abi = json.load(f)

    contract = w3.eth.contract(address=contractAddress, abi=abi)
    contract.address = contractAddress 
    
    main_loop()
