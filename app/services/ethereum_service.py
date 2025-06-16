import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class EthereumService:
    def __init__(self):
        self.infura_url = os.getenv("INFURA_URL")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.wallet_address = os.getenv("WALLET_ADDRESS")
        self.web3 = Web3(Web3.HTTPProvider(self.infura_url))

        if not self.web3.isConnected():
            raise ConnectionError("❌ Failed to connect to Infura RPC")

        self.account = self.web3.eth.account.from_key(self.private_key)
        print(f"✅ Connected as: {self.account.address}")
