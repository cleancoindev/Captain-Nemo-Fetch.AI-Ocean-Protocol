import logging
import os
from squid_py import Metadata, Ocean
import squid_py
import mantaray_utilities as manta_utils

# Setup logging
from mantaray_utilities.user import get_account_from_config
from mantaray_utilities.events import subscribe_event
manta_utils.logging.logger.setLevel('INFO')
import mantaray_utilities as manta_utils
from squid_py import Config
from squid_py.keeper import Keeper
from pathlib import Path
import datetime
import web3
import asyncio

# Get the configuration file path for this environment
OCEAN_CONFIG_PATH = Path(os.environ['OCEAN_CONFIG_PATH'])
assert OCEAN_CONFIG_PATH.exists(), "{} - path does not exist".format(OCEAN_CONFIG_PATH)

# The Market Place will be delegated to provide access to your assets, so we need the address
MARKET_PLACE_PROVIDER_ADDRESS = os.environ['MARKET_PLACE_PROVIDER_ADDRESS']

logging.critical("Configuration file selected: {}".format(OCEAN_CONFIG_PATH))
logging.critical("Deployment type: {}".format(manta_utils.config.get_deployment_type()))
logging.critical("Squid API version: {}".format(squid_py.__version__))
logging.info("MARKET_PLACE_PROVIDER_ADDRESS:{}".format(MARKET_PLACE_PROVIDER_ADDRESS))

# Instantiate Ocean with the default configuration file.
configuration = Config(OCEAN_CONFIG_PATH)
squid_py.ConfigProvider.set_config(configuration)
ocn = Ocean(configuration)

publisher_account = manta_utils.user.get_account_by_index(ocn,0)

Did_bitcoin = 'did:op:71fae96b1d9a4651ba0d3946603fb4c11deb724685f64780985ce32ea2dfe517'

print(ocn.assets.resolve(Did_bitcoin))

service_agreement_id = ocn.assets.order(Did_bitcoin, 0, publisher_account)
