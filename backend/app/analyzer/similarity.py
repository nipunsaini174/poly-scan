from typing import List, Tuple
from app.models.schemas import BehaviorGraphModel, SimilarityResult

def calculate_similarity(graph_a: BehaviorGraphModel, graph_b: BehaviorGraphModel) -> SimilarityResult:
    """Calculate behavioral similarity between two graphs."""
    actions_a = [n.action_type for n in graph_a.nodes]
    actions_b = [n.action_type for n in graph_b.nodes]
    
    if not actions_a and not actions_b:
        return SimilarityResult(
            similarity_percentage=0.0,
            matched_actions=[],
            unique_to_a=[],
            unique_to_b=[],
            graph_similarity=0.0,
            explanation="Both codes have no recognized behavioral actions."
        )
        
    if not actions_a or not actions_b:
        return SimilarityResult(
            similarity_percentage=0.0,
            matched_actions=[],
            unique_to_a=actions_a,
            unique_to_b=actions_b,
            graph_similarity=0.0,
            explanation="One of the codes has no recognized actions, while the other does."
        )
        
    matched = []
    unique_a = actions_a.copy()
    unique_b = actions_b.copy()
    
    # Simple intersection for MVP
    for a in actions_a:
        if a in unique_b:
            matched.append(a)
            unique_b.remove(a)
            unique_a.remove(a)
            
    # Calculate similarity percentage based on Jaccard-like index of behaviors
    intersection = len(matched)
    union = len(actions_a) + len(actions_b) - intersection
    
    similarity_percentage = (intersection / union) * 100 if union > 0 else 0.0
    
    # Sequence similarity (simplified for MVP: checking if sequence matches)
    seq_sim = 0.0
    if len(actions_a) > 0 and len(actions_b) > 0:
        # Longest Common Subsequence of tags
        lcs = _lcs(actions_a, actions_b)
        seq_sim = (lcs / max(len(actions_a), len(actions_b))) * 100
        
    explanation = "Code fragments have completely different behaviors."
    if similarity_percentage == 100.0 and seq_sim == 100.0:
        explanation = "Both programs exhibit identical sequence of behaviors."
    elif similarity_percentage > 50.0:
        explanation = f"Significant behavioral overlap detected. Sequence similarity is {seq_sim:.1f}%."
    elif similarity_percentage > 0:
        explanation = "Some behavioral overlap, but significant differences exist."

    return SimilarityResult(
        similarity_percentage=round(similarity_percentage, 1),
        matched_actions=matched,
        unique_to_a=unique_a,
        unique_to_b=unique_b,
        graph_similarity=round(seq_sim, 1),
        explanation=explanation
    )

def _lcs(X, Y):
    m = len(X)
    n = len(Y)
    L = [[0] * (n + 1) for i in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
    return L[m][n]
