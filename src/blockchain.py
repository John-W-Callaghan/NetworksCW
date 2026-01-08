import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, votes, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.votes = votes  # List of vote transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        
    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_votes = []
        self.create_genesis_block()
        
    def create_genesis_block(self):
        genesis_block = Block(0, datetime.now().isoformat(), 
                             ["Genesis Block"], "0")
        self.chain.append(genesis_block)
        
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_vote(self, vote_data):
        self.pending_votes.append(vote_data)
        
    def mine_block(self):
        if len(self.pending_votes) == 0:
            return None
            
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=datetime.now().isoformat(),
            votes=self.pending_votes.copy(),
            previous_hash=latest_block.hash
        )
        
        self.chain.append(new_block)
        self.pending_votes = []  # Clear pending votes
        return new_block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check hash integrity
            if current_block.hash != current_block.calculate_hash():
                return False
                
            # Check chain linkage
            if current_block.previous_hash != previous_block.hash:
                return False
                
        return True
    
    def get_blockchain_data(self):
        return [block.to_dict() for block in self.chain]