import json
from src.blockchain import Blockchain, Block

def simulate_hack():
    print("--- Blockchain Integrity Test ---")
    
    # 1. Load the existing blockchain from the file
    with open('data/blockchain.json', 'r') as f:
        data = json.load(f)
    
    # 2. Reconstruct the blockchain object
    bc = Blockchain()
    bc.chain = [] # Clear the default genesis block
    
    for b in data:
        # Re-creating block objects from the JSON data
        new_block = Block(b['index'], b['votes'], b['previous_hash'], b['timestamp'])
        new_block.hash = b['hash'] # Keep the original hash for now
        bc.chain.append(new_block)
    
    print(f"Initial integrity check: {'✅ PASSED' if bc.is_chain_valid() else '❌ FAILED'}")

    # 3. SIMULATE A HACK
    print("\n--- SIMULATING TAMPERING ---")
    print("Changing a vote in Block 1...")
    # We reach into the second block (index 1) and change the candidate
    bc.chain[1].votes[0]['candidate'] = "HACKED_CANDIDATE"
    
    # 4. Final check
    print(f"Post-tamper integrity check: {'✅ PASSED' if bc.is_chain_valid() else '❌ FAILED'}")
    print("Reason: The hash of Block 1 no longer matches the data inside it!")

if __name__ == "__main__":
    simulate_hack()