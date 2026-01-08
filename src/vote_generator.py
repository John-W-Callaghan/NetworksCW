import random
import time
import pandas as pd

def generate_simulation_data(num_voters=200):
    data = []
    candidates = ["Candidate A", "Candidate B", "Candidate C"]
    
    for i in range(num_voters):
        is_anomaly = random.random() < 0.1  # 10% anomalies
        
        if not is_anomaly:
            # Normal behavior
            vote_time = random.uniform(0, 86400)
            submission_speed = random.uniform(30, 120)
            session_entropy = random.uniform(0.6, 0.9) # High randomness (human)
        else:
            # Anomalous behavior (Bot-like)
            vote_time = random.uniform(72000, 75000)
            submission_speed = random.uniform(0.1, 2.0)
            session_entropy = random.uniform(0.1, 0.3) # Low randomness (scripted)
            
        data.append({
            "voter_id": f"voter_{i}",
            "candidate": random.choice(candidates),
            "vote_time": vote_time,
            "submission_speed": submission_speed,
            "session_entropy": session_entropy, # Third dimension
            "is_anomaly": 1 if is_anomaly else 0
        })
        
    return pd.DataFrame(data)