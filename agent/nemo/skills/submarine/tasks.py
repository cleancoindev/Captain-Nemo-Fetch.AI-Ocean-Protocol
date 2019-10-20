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

"""This module contains the tasks for the 'Submarine' skill."""
import logging
import time

from aea.skills.base import Task

logger = logging.getLogger("aea.echo_skill")
from numpy import genfromtxt
from sklearn.linear_model import LogisticRegression

import os
import time

from squid_py import (
    Ocean,
    ConfigProvider,
    Config
)





class SubmarineTask(Task):
    """Submarine task."""

    def __init__(self, **kwargs):
        """Initialize the task."""
        super().__init__(**kwargs)
        logger.info("SubmarineTask.__init__: arguments: {}".format(kwargs))

    def setup(self) -> None:
        """Set up the task."""
        logger.info("Submarine Task: setup method called.")
        self.query_txn = None
        self.model = LogisticRegression()

    def execute(self, contract, query, nonce) -> None:
        """Execute the task."""
        #logger.info("Submarine Task: execute method called.")
        if not self.query_txn:
            response = self.create_ocean_request(query)
            result = self.process_response(query, response)
            updateQuery = contract.functions.updateQuery(query["contract"], result)
        
            self.query_txn = self.prepare_tx(updateQuery, nonce)
            #self.query_txn = None
        

    def teardown(self) -> None:
        """Teardown the task."""
        logger.info("Submarine Task: teardown method called.")

    def create_ocean_request(self, query) -> None:
        ConfigProvider.set_config(Config('../../ocean/config.ini'))
        # Make a new instance of Ocean
        ocean = Ocean() # or Ocean(Config('config.ini'))
        config = ocean.config
        # make account instance, assuming the ethereum account and password are set 
        # in the config file `config.ini`
        account = ocean.accounts.list()[0]
        filename = '../../ocean/bitcoin_2017.csv'
        did = query['did']
        my_data = genfromtxt(filename, delimiter=',')
        #print('data at', filename, my_data)
        return my_data

        

        

        #did = 'did:op:71fae96b1d9a4651ba0d3946603fb4c11deb724685f64780985ce32ea2dfe517'
        service_agreement_id = ocean.assets.order(did, 0, account)

        # after a short wait (seconds to minutes) the asset data files should be available in the `downloads.path` defined in config
        # wait a bit to let things happen

        print(service_agreement_id)
        time.sleep(20)

        # Asset files are saved in a folder named after the asset id
        dataset_dir = os.path.join(ocean.config.downloads_path, f'datafile.{asset_ddo.asset_id}.0')
        if os.path.exists(dataset_dir):
            print('asset files downloaded: {}'.format(os.listdir(dataset_dir)))




    def process_response(self, query, response) -> None:
        X = [response[i][:-1] for i in range(350)]
        y = [response[i][-1] for i in range(350)]

        self.model.fit(X, y)
        y_test = self.model.predict_proba([response[i][:-1] for i in range(301,363)])[:,1]
        mse = ((y_test-[response[i][-1] for i in range(301,363)])**2).mean()
        print(y_test.tolist()[:5], [mse]*5)

        if query["command"] == 'mean':
            return [int(100000*mse) for x in range(5)]
        return [int(100000*x) for x in y_test.tolist()[:5]]

    def prepare_tx(self, updateQuery, nonce):
        
        query_txn = updateQuery.buildTransaction({
                    'gas': 300000,
                    'nonce': nonce
        })
        return query_txn

       
