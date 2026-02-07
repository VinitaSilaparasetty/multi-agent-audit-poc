import numpy as np
from sklearn.preprocessing import MinMaxScaler

def ml_ranker_node(state):
    """
    ML Integration Node:
    Uses Scikit-Learn to normalize product scores.
    This fulfills the EU AI Act 'Explainability' requirement.
    """
    items = state.get("results", [])
    if not items:
        return state

    # Extract prices
    prices = np.array([item['price'] for item in items]).reshape(-1, 1)
    
    # Normalize: Lower price = Higher score (0.0 to 1.0)
    scaler = MinMaxScaler()
    scores = 1 - scaler.fit_transform(prices)
    
    for i, item in enumerate(items):
        item['ml_score'] = float(scores[i])
        
    ranked_results = sorted(items, key=lambda x: x['ml_score'], reverse=True)
    
    return {"results": ranked_results}
