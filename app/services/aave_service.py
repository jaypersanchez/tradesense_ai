import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class AaveService:
    def __init__(self, web3):
        self.web3 = web3
        self.old_pool = Web3.to_checksum_address(os.getenv("OLD_AAVE_LENDING_POOL_ADDRESS"))
        self.current_pool = Web3.to_checksum_address(os.getenv("AAVE_LENDING_POOL_ADDRESS"))

        # ABI loading and function wrappers to come later
        print("✅ Aave lending pool addresses loaded.")
