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

"""This module contains the behaviours for the 'echo' skill."""

import logging, time
from aea.skills.base import Behaviour

logger = logging.getLogger("aea.echo_skill")


class SubmarineBehaviour(Behaviour):
    """Submarine behaviour."""

    def __init__(self, **kwargs):
        """Initialize the echo behaviour."""
        super().__init__(**kwargs)
        logger.info("SubmarineBehaviour.__init__: arguments: {}".format(kwargs))

    def setup(self) -> None:
        """Set up the behaviour."""
        #logger.info("Submarine Behaviour: setup method called.")
        self.orders_book = {}
        self.events_number = 0
        self.active_query = None

    def act(self, contract, address) -> None:
        """Act according to the behaviour."""
        #logger.info("Submarine Behaviour: act method called.")
        event_filter = contract.events.QueryCreated.createFilter(fromBlock=0)
        
        if self.events_number < len(event_filter.get_all_entries()):
            for e in event_filter.get_all_entries():
                event_args = e["args"]
                command = event_args["command"]
                agentAddress = event_args["agentAddress"]
                oceanDid = event_args["oceanDid"]
                queryContract = event_args["queryContract"]
                print('data', self.orders_book)
                if agentAddress == address:
                    if queryContract in self.orders_book:
                        self.orders_book[queryContract].append({"command" : command, "did" : oceanDid})
                    else:
                        self.orders_book[queryContract] = [{"command" : command, "did" : oceanDid}]
                    self.active_query = {"contract" : queryContract, "command" : command, "did" : oceanDid}
            self.events_number += 1# len(event_filter.get_all_entries())#maybe dont need this

        time.sleep(1)

    def teardown(self) -> None:
        """Teardown the behaviour."""
        logger.info("Submarine Behaviour: teardown method called.")
