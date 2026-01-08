import uuid
import time 
from ecdsa import SigningKey, SECP256k1

class Voter:
    def __init__(self, name):
        self.voter_id = str(uuid.uuid4())
        self.name = name
        # Generate Private Key (keep secret) and Public Key (ID on blockchain)
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.verifying_key
        self.has_voted = False

    def sign_vote(self, vote_data):
        # Converts vote info to bytes and signs it
        return self.private_key.sign(vote_data.encode())

class Vote:
    def __init__(self, voter_id, candidate, signature):
        self.voter_id = voter_id
        self.candidate = candidate
        self.timestamp = time.time()
        self.signature = signature.hex() # Stored as hex for JSON compatibility