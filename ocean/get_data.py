import os
import time

from squid_py import (
    Ocean,
    ConfigProvider,
    Config
)

ConfigProvider.set_config(Config('config.ini'))
# Make a new instance of Ocean
ocean = Ocean() # or Ocean(Config('config.ini'))
config = ocean.config
# make account instance, assuming the ethereum account and password are set 
# in the config file `config.ini`
account = ocean.accounts.list()[0]

print('account', account)

did = 'did:op:71fae96b1d9a4651ba0d3946603fb4c11deb724685f64780985ce32ea2dfe517'
service_agreement_id = ocean.assets.order(did, 0, account)

# after a short wait (seconds to minutes) the asset data files should be available in the `downloads.path` defined in config
# wait a bit to let things happen

print(service_agreement_id)
time.sleep(20)

# Asset files are saved in a folder named after the asset id
dataset_dir = os.path.join(ocean.config.downloads_path, f'datafile.{asset_ddo.asset_id}.0')
if os.path.exists(dataset_dir):
    print('asset files downloaded: {}'.format(os.listdir(dataset_dir)))


