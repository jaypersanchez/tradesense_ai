import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class CompoundService:
    def __init__(self, web3):
        self.web3 = web3
        self.usdc_address = Web3.to_checksum_address(os.getenv("USDC_ADDRESS"))
        self.c_usdc_address = Web3.to_checksum_address(os.getenv("C_USDC_ADDRESS"))
        self.dai_address = Web3.to_checksum_address(os.getenv("DAI_ADDRESS"))
        self.c_dai_address = Web3.to_checksum_address(os.getenv("C_DAI_ADDRESS"))
        self.comptroller_address = Web3.to_checksum_address(os.getenv("COMPOUND_COMPTROLLER"))

        # ABI loading will go here
        print("✅ Compound contract addresses loaded.")
