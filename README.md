# EcoFriendlyCoinMiner

## A Simplified, Educational Blockchain & CPU Miner

This project demonstrates a basic, CPU-based Proof-of-Work (PoW) blockchain system written in Python. It's designed for educational purposes to understand the core concepts of mining, block creation, hashing, and a simple reward mechanism.

**Disclaimer:** This is a **toy blockchain** and **NOT a real cryptocurrency**. The `EcoCoin` generated here has no monetary value and operates only within this isolated program. It cannot be exchanged on real-world crypto markets. It is not designed for security or scalability required by production-grade blockchains.

## Features

*   **CPU-Based Mining:** Leverages your CPU to perform SHA-256 hashing for Proof-of-Work. Expected hashrates will be in the Kilohash/s (KH/s) to low Megahash/s (MH/s) range, depending on your CPU.
*   **Custom Coin (`EcoCoin`):** Introduces a custom cryptocurrency called `EcoCoin` that is rewarded to the miner upon successful block discovery.
*   **Simple Block Structure:** Each block contains an index, timestamp, arbitrary "data," the previous block's hash, a nonce, the current block's hash, and the miner's address.
*   **Proof-of-Work (PoW):** Miners must find a nonce that results in a block hash starting with a predefined number of leading zeros (difficulty target).
*   **Basic Chain Validation:** Includes a mechanism to verify the integrity of the blockchain.
*   **"Eco-Friendly" (Conceptual):** While PoW inherently consumes energy, this CPU-based simulation is significantly less energy-intensive than real-world ASIC mining. The term here refers to its low-impact nature compared to industrial crypto mining.

## How it Works (Conceptual Flow)

1.  **Blockchain Node:** The Python script acts as a single node in its own isolated blockchain network.
2.  **Block Candidate:** When you want to "share data" (e.g., a message, a simulated transaction), this data is added to a list of "pending data." When mining starts, this data is assembled into a `Block` candidate along with the previous block's hash, a timestamp, and your designated `MINER_ADDRESS`.
3.  **Hashing (`SHA-256-like function`):** The program repeatedly hashes the entire block candidate (varying the `nonce` value) using Python's `hashlib.sha256` function.
4.  **Proof-of-Work Check:** It checks if the resulting `hash_output` meets the `difficulty_target` (e.g., starts with "00").
5.  **Block Mined!:** If a valid hash is found, the block is considered "mined."
6.  **Reward:** The `MINER_ADDRESS` associated with the mined block receives `BLOCK_REWARD` `EcoCoins` in a simple internal ledger.
7.  **Chain Update:** The new, valid block is added to the blockchain list.

## Setup and Running

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/tootter11/EcoFriendlyCoinMiner.git
    cd EcoFriendlyCoinMiner
    ```
2.  **Install Python:** Ensure you have Python 3.x installed.
3.  **Run the Miner:**
    ```bash
    python EcoFriendlyCoinMiner.py
    ```

## Customization

You can easily customize the following parameters at the top of the `EcoFriendlyCoinMiner.py` file:

*   `COIN_NAME`: Change the name of your cryptocurrency (e.g., "MyCoolCoin").
*   `MINER_ADDRESS`: **CRITICAL! Replace `"your_github_username_miner"` with your actual GitHub username or a unique identifier.** This is where your rewards will accumulate.
*   `BLOCK_REWARD`: Adjust the amount of `EcoCoin` awarded per block.
*   `INITIAL_DIFFICULTY_PREFIX`: Change the mining difficulty.
    *   `"0"`: Easiest (hash must start with one '0')
    *   `"00"`: Medium (hash must start with two '0's) - **Default and Recommended for CPU mining**
    *   `"000"`: Harder (hash must start with three '0's) - Will take significantly longer to mine.
    *   `"0000"`: Very Hard - Expect very long mining times on a CPU.

## Getting Your `EcoCoin` Address

Your `EcoCoin` address is simply the string you define in the `MINER_ADDRESS` variable within the `EcoFriendlyCoinMiner.py` script. When a block is successfully mined, the `BLOCK_REWARD` will be credited to this address in the program's internal ledger.

**Example:** If you set `MINER_ADDRESS = "my_awesome_miner_id"`, then "my_awesome_miner_id" is your address for receiving `EcoCoin` rewards within this simulation.

## Further Development Ideas (Not Implemented)

*   **Networking:** Allow multiple nodes to connect, validate, and synchronize the blockchain.
*   **GPU Mining:** Integrate with PyCUDA or PyOpenCL for faster hashing (much more complex).
*   **Transaction System:** Implement a proper transaction class and validate transactions within blocks.
*   **Peer-to-Peer Discovery:** Mechanisms for nodes to find each other.
*   **Persistence:** Save the blockchain to a file so it's not lost when the program closes.
*   **Dynamic Difficulty Adjustment:** Adjust the `difficulty_prefix` based on the network's average mining speed.
*   **Wallets:** More robust address generation and key management.

---

**Author:** Tootter11

**License:** MIT License (or your preferred open-source license)