import hashlib
import time
import json
from datetime import datetime

# --- Configuration ---
# You can customize these values
COIN_NAME = "EcoCoin"
MINER_ADDRESS = "your_github_username_miner" # Replace with your GitHub username or a unique identifier
BLOCK_REWARD = 10 # Number of EcoCoins per mined block
INITIAL_DIFFICULTY_PREFIX = "00" # Hash must start with this many zeros (e.g., "00", "000", "0000")

# --- Block Structure ---
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, current_hash=None, miner_address=MINER_ADDRESS):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner_address = miner_address
        # current_hash will be calculated during mining. If not provided, it's a candidate block.
        self.current_hash = current_hash if current_hash else self.calculate_hash() 

    def calculate_hash(self):
        """
        Calculates the SHA-256 hash of the block's header.
        This is the core of the Proof-of-Work.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "miner_address": self.miner_address
        }, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.current_hash[:10]}..., PrevHash: {self.previous_hash[:10]}..., Nonce: {self.nonce}, Miner: {self.miner_address}, Data: {self.data})"

# --- Blockchain Structure ---
class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_data = [] # Data waiting to be included in the next block (like transactions)
        self.balances = {MINER_ADDRESS: 0} # Simple ledger for rewards
        self.difficulty_prefix = INITIAL_DIFFICULTY_PREFIX
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the very first block in the blockchain (Block 0).
        """
        genesis_data = f"Genesis Block of {COIN_NAME} Network"
        genesis_block = Block(0, datetime.now(), genesis_data, "0", miner_address="Genesis_Creator")
        genesis_block.current_hash = genesis_block.calculate_hash() # Hash for genesis doesn't need PoW
        self.chain.append(genesis_block)
        print(f"Genesis Block Created: {genesis_block.current_hash}\n")

    @property
    def last_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_data_to_pending(self, data):
        """Adds new data to the list of pending data for the next block."""
        self.pending_data.append(data)
        print(f"'{data}' added to pending data.")

    def mine_block(self, miner_address=MINER_ADDRESS):
        """
        Mines a new block using Proof-of-Work.
        This function iterates nonces until a valid hash is found.
        """
        if not self.pending_data:
            print("No pending data to include in the block. Mining an empty block.")
            block_data = "No new data"
        else:
            block_data = f"Data: {', '.join(self.pending_data)}"
            self.pending_data = [] # Clear pending data after including it

        index = len(self.chain)
        timestamp = datetime.now()
        previous_hash = self.last_block.current_hash
        nonce = 0
        
        print(f"\n--- Starting to mine Block {index} for {miner_address} ---")
        print(f"Difficulty Target: Hash must start with '{self.difficulty_prefix}'")
        print(f"Block Data: {block_data}")
        
        start_time = time.time()
        hashes_tried = 0
        
        # Create a candidate block to start hashing
        block_candidate = Block(index, timestamp, block_data, previous_hash, nonce, miner_address=miner_address)
        current_hash = block_candidate.calculate_hash()

        # Proof-of-Work loop
        while not current_hash.startswith(self.difficulty_prefix):
            nonce += 1
            hashes_tried += 1
            block_candidate.nonce = nonce
            current_hash = block_candidate.calculate_hash()
            # Optional: Print progress every X hashes (can slow down mining)
            # if hashes_tried % 100000 == 0: 
            #     print(f"  Tried {hashes_tried} hashes, current: {current_hash[:10]}...")

        end_time = time.time()
        time_taken = end_time - start_time
        
        # Finalize the block once a valid hash is found
        mined_block = Block(index, timestamp, block_data, previous_hash, nonce, current_hash, miner_address=miner_address)
        self.chain.append(mined_block)
        
        # --- Reward System ---
        self.balances[miner_address] = self.balances.get(miner_address, 0) + BLOCK_REWARD
        
        print(f"\nBlock {index} MINED successfully!")
        print(f"  Hash: {mined_block.current_hash}")
        print(f"  Nonce: {mined_block.nonce}")
        print(f"  Hashes Tried: {hashes_tried}")
        print(f"  Time Taken: {time_taken:.2f} seconds")
        print(f"  Hashrate: {hashes_tried / time_taken:.2f} H/s ({COIN_NAME} mining)")
        print(f"  Reward: {BLOCK_REWARD} {COIN_NAME} to {miner_address}")
        print(f"  New Balance for {miner_address}: {self.balances[miner_address]} {COIN_NAME}")
        return mined_block

    def is_chain_valid(self):
        """
        Verifies the integrity of the blockchain by checking hashes and links.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Recalculate hash and check if it matches the stored hash
            if current_block.current_hash != current_block.calculate_hash():
                print(f"Block {current_block.index}: Hash Mismatch!")
                return False

            # Check if previous_hash matches the actual previous block's hash
            if current_block.previous_hash != previous_block.current_hash:
                print(f"Block {current_block.index}: Previous Hash Mismatch (Chain Broken)!")
                return False
            
            # Check difficulty target (optional, but good for full validation)
            if not current_block.current_hash.startswith(self.difficulty_prefix):
                 print(f"Block {current_block.index}: Hash does not meet difficulty target!")
                 return False

        return True
    
    def print_chain(self):
        """Prints all blocks in the chain."""
        print(f"\n--- Current {COIN_NAME} Blockchain (Length: {len(self.chain)}) ---")
        for block in self.chain:
            print(f"Block {block.index} | Time: {block.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | Miner: {block.miner_address}")
            print(f"  Data: {block.data}")
            print(f"  PrevHash: {block.previous_hash[:15]}...")
            print(f"  Hash: {block.current_hash[:15]}... ({block.current_hash})")
            print(f"  Nonce: {block.nonce}")
            print("-" * 50)
        print(f"\n--- Balances ---")
        for addr, balance in self.balances.items():
            print(f"{addr}: {balance} {COIN_NAME}")
        print("-" * 50)

# --- Main Program Execution ---
if __name__ == "__main__":
    my_blockchain = Blockchain()

    # Simulate adding some "real world data" (e.g., messages, sensor readings, small file hashes)
    my_blockchain.add_data_to_pending("Temperature reading: 25.5°C")
    my_blockchain.add_data_to_pending("User 'Alice' liked 'Bob's' post")
    
    # Mine the first actual block
    my_blockchain.mine_block(MINER_ADDRESS)

    # Add more data and mine another block
    my_blockchain.add_data_to_pending("Sensor data from device X: 1024lux")
    my_blockchain.mine_block(MINER_ADDRESS)

    # You can change the miner address to simulate different miners
    my_blockchain.add_data_to_pending("Transaction: Bob sent 5 EcoCoins to Charlie (not implemented in ledger yet)")
    my_blockchain.mine_block("another_miner_address") # Example of another miner

    # Mine a few more blocks to see the chain grow
    for i in range(2):
        my_blockchain.add_data_to_pending(f"Arbitrary data for block {my_blockchain.last_block.index + 1}")
        my_blockchain.mine_block(MINER_ADDRESS)

    # Print the full chain and balances
    my_blockchain.print_chain()

    # Validate the chain
    print(f"\nBlockchain validity check: {my_blockchain.is_chain_valid()}")

    # Demonstrate changing difficulty (making it harder)
    # Be aware: '000' will take ~16 times longer than '00'
    # '0000' will take ~256 times longer than '00'
    # my_blockchain.difficulty_prefix = "000" 
    # print(f"\n--- Difficulty increased to '{my_blockchain.difficulty_prefix}' ---")
    # my_blockchain.add_data_to_pending("Data after difficulty increase")
    # my_blockchain.mine_block(MINER_ADDRESS)
    # my_blockchain.print_chain()
    