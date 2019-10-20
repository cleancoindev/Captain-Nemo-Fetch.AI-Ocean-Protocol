# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the implementation of an Autonomous Economic Agent."""
import logging, os
from pathlib import Path
from typing import Optional, cast

from agent import Agent
from aea.context.base import AgentContext
#from aea.crypto.wallet import Wallet
from aea.decision_maker.base import DecisionMaker
from aea.mail.base import Envelope, MailBox
from aea.registries.base import Resources
from aea.skills.error.handlers import ErrorHandler



import logging
from web3.auto import Web3
import time
import requests
import json



logger = logging.getLogger(__name__)


class Nemo(Agent):
    """This class implements an autonomous economic agent."""

    def __init__(self, name: str,
                 #wallet: Wallet,
                 timeout: float = 1.0,
                 debug: bool = False) -> None:
        """
        Instantiate the agent.

        :param name: the name of the agent
        :param wallet: the crypto wallet of the agent.
        :param timeout: the time in (fractions of) seconds to time out an agent between act and react
        :param debug: if True, run the agent in debug mode.

        :return: None
        """
        super().__init__(name=name, timeout=timeout, debug=debug)
        self._directory = ""
        self._resources = None  # type: Optional[Resources]
        
   
    @property
    def resources(self) -> Resources:
        """Get resources."""
        assert self._resources is not None, "No resources initialized. Call setup."
        return self._resources

    def start(self) -> None:
        """
        Start the agent.

        :return: None
        """
        
        self.setup()

        self.liveness._is_stopped = False
        self._run_main_loop()

    def setup(self) -> None:
        """
        Set up the agent.

        :return: None
        """
        self._resources = Resources.from_resource_dir(self._directory, None)
        assert self._resources is not None, "No resources initialized. Error in setup."
        self._resources.setup()

        self.w3 = Web3(Web3.HTTPProvider("https://nile.dev-ocean.com")) #"http://localhost:7545"))

        with open('keystore/UTC--2019-10-19T15-13-02.082157851Z--719b682d53f15899376709fb372c98aa5a116799') as keyfile:
            encrypted_key = keyfile.read()
            self.private_key = self.w3.eth.account.decrypt(encrypted_key, 'submarine')

        master_contract_address = '0x7d5158372BC13D1bA316b44B9002821BE46652F5'
        
        master_contract_address = Web3.toChecksumAddress(master_contract_address)
        self.account =  self.w3.eth.account.privateKeyToAccount(self.private_key)
        self.w3.eth.defaultAccount = self.account.address
        self.eventBehaviour = self.resources.behaviour_registry.fetch_all()[0]
        self.resultTask = self.resources.task_registry.fetch_all()[0]
        #my_address = '0x719b682d53f15899376709fb372c98aa5a116799'

        with open("abi.json") as f:
            abi = json.load(f)

        self.contract = self.w3.eth.contract(address=master_contract_address, abi=abi)
        self.address = master_contract_address 
        

        print("master contract", self.contract)

    def act(self) -> None:
        """
        Perform actions.

        :return: None
        """
        self.eventBehaviour.act(self.contract, self.w3.eth.defaultAccount)
   
    def react(self) -> None:
        """
        React to incoming events (envelopes).

        :return: None
        """
        pass


    def update(self) -> None:
        """Update the current state of the agent.

        :return None
        """
        nonce = self.w3.eth.getTransactionCount(self.account.address)  
        query = self.eventBehaviour.active_query
        if query:
            self.resultTask.execute(self.contract, query, nonce)
            self.eventBehaviour.active_query = None
        
        if self.resultTask.query_txn:
            print("sending transaction", self.resultTask.query_txn)
            signed_txn = self.w3.eth.account.signTransaction(self.resultTask.query_txn, private_key=self.private_key)
            self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            self.resultTask.query_txn = None
            
            time.sleep(3)
       
    def teardown(self) -> None:
        """
        Tear down the agent.

        :return: None
        """
        if self._resources is not None:
            self._resources.teardown()



if __name__ == '__main__':

    agent_name = "Submarine"
    private_key_pem_path = "default_private_key.pem"
    #wallet = Wallet({'default': private_key_pem_path})
    #public_key = wallet.public_keys['default']

    
   

    agent = Nemo(
        agent_name)
    agent.start()