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

    def execute(self, contract, query, nonce) -> None:
        """Execute the task."""
        #logger.info("Submarine Task: execute method called.")
        response = self.create_ocean_request(query)
        result = self.process_response(response)
        updateQuery = contract.functions.updateQuery(query["contract"], result)
        if not self.query_txn:
            self.query_txn = self.prepare_tx(updateQuery, nonce)
            #self.query_txn = None
        

    def teardown(self) -> None:
        """Teardown the task."""
        logger.info("Submarine Task: teardown method called.")

    def create_ocean_request(self, query) -> None:
        pass

    def process_response(self, response) -> None:
        return [4,5,6,7,8]

    def prepare_tx(self, updateQuery, nonce):
        
        query_txn = updateQuery.buildTransaction({
                    'gas': 300000,
                    'nonce': nonce
        })
        return query_txn

       
