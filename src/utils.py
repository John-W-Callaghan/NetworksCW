import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

def save_election_data(voter_df, blockchain):
    # 1. Save the simulation/voter log
    voter_df.to_csv('data/votes_log.csv', index=False)
    
    # 2. Extract results from Blockchain to save to a results CSV
    results_list = []
    for block in blockchain.chain:
        for vote in block.votes:
            v_data = vote.__dict__ if hasattr(vote, '__dict__') else vote
            results_list.append(v_data)
    
    results_df = pd.DataFrame(results_list)
    results_df.to_csv('data/final_blockchain_votes.csv', index=False)
    
    # 3. Save raw JSON for integrity testing
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "previous_hash": block.previous_hash,
            "merkle_root": block.merkle_root,
            "hash": block.hash,
            "votes": [v.__dict__ if hasattr(v, '__dict__') else v for v in block.votes]
        })

    with open('data/blockchain.json', 'w') as f:
        json.dump(chain_data, f, indent=4)
        
    print("✅ All CSV and JSON data files updated in /data folder")

def plot_results(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='vote_time', y='submission_speed', hue='is_anomaly', palette='viridis')
    plt.title("E-Voting Anomaly Detection Map")
    plt.savefig('results/anomaly_report.png')
    print("✅ Visualization saved to results/anomaly_report.png")