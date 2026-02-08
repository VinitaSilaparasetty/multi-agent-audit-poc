import numpy as np
from sklearn.preprocessing import MinMaxScaler

def ml_ranker_node(state):
    items = state.get("results", [])
    if not items:
        return state

    prices = np.array([item['price'] for item in items]).reshape(-1, 1)
    scaler = MinMaxScaler()
    scores = 1 - scaler.fit_transform(prices)
    
    for i, item in enumerate(items):
        # .item() converts a NumPy scalar to a native Python float
        item['ml_score'] = scores[i].item()
        
    ranked_results = sorted(items, key=lambda x: x['ml_score'], reverse=True)
    return {"results": ranked_results}
