from src.blockchain import Blockchain
from src.voter import Voter, Vote
from src.anomaly_detector import AnomalyDetector
from src.vote_generator import generate_simulation_data
from src.utils import save_election_data, plot_results # Ensure these are imported
import pandas as pd

def run_election():
    print("--- Initializing Secure E-Voting System ---")
    
    # 1. Setup
    election_ledger = Blockchain()
    ai_auditor = AnomalyDetector()
    
    # 2. Simulate Data & Train AI
    print("Simulating voter behavior and training AI...")
    sim_data = generate_simulation_data(500)
    ai_auditor.train(sim_data[['vote_time', 'submission_speed']])
    
    # 3. Process Votes
    votes_to_audit = []
    print("Processing incoming votes...")
    
    for _, row in sim_data.iterrows():
        # --- LAYER 1: AI ANOMALY DETECTION ---
        status = ai_auditor.detect([row['vote_time'], row['submission_speed']])
        
        if status != "NORMAL":
            print(f"⚠️ AI Alert: Anomalous behavior from {row['voter_id']}! Vote blocked.")
            continue # Skip this vote

        # --- LAYER 2: CRYPTOGRAPHIC & ELIGIBILITY CHECKS ---
        try:
            # 1. Verify Digital Signature (Placeholder for now)
            is_signature_valid = True 
            if not is_signature_valid:
                print(f"❌ Security Alert: Invalid signature for {row['voter_id']}!")
                continue

            # 2. Check for Double Voting (Eligibility)
            # We check if this voter_id already exists in any block in the chain
            already_voted = False
            for block in election_ledger.chain:
                for vote in block.votes:
                    # Handle both object and dict formats
                    existing_id = vote['voter_id'] if isinstance(vote, dict) else vote.voter_id
                    if existing_id == row['voter_id']:
                        already_voted = True
                        break
            
            if already_voted:
                print(f"❌ Fraud Alert: Double voting attempt by {row['voter_id']}!")
                continue

            # --- LAYER 3: BLOCKCHAIN SUBMISSION ---
            # If it passed all checks, create the vote and add to batch
            new_vote = Vote(row['voter_id'], row['candidate'], b"signature_placeholder")
            votes_to_audit.append(new_vote)
            
            # Batch votes (Merkle Tree Optimization: 5 votes per block)
            if len(votes_to_audit) >= 5:
                election_ledger.add_block(votes_to_audit)
                votes_to_audit = []

        except Exception as e:
            print(f"Error verifying vote: {e}")
            

    # 4. Final Validation & Results
    print(f"\nElection Complete!")
    print(f"Blockchain Integrity: {'✅ VALID' if election_ledger.is_chain_valid() else '❌ COMPROMISED'}")
    
    # Save the files so your CSVs/JSON are no longer empty
    save_election_data(sim_data, election_ledger)
    plot_results(sim_data)

if __name__ == "__main__":
    run_election()