from __future__ import annotations

import math
from statistics import mean


def rank_data(values: list[float]) -> list[float]:
    """Return average ranks for ties. Smallest value gets rank 1."""
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i + 1
        while j < len(indexed) and indexed[j][1] == indexed[i][1]:
            j += 1
        average_rank = ((i + 1) + j) / 2
        for k in range(i, j):
            ranks[indexed[k][0]] = average_rank
        i = j
    return ranks


def pearson(x: list[float], y: list[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    mx, my = mean(x), mean(y)
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    denominator = math.sqrt(sum(v * v for v in dx) * sum(v * v for v in dy))
    if denominator == 0:
        return None
    return sum(a * b for a, b in zip(dx, dy)) / denominator


def spearman_rank_correlation(x: list[float | None], y: list[float | None]) -> dict:
    pairs = [(float(a), float(b)) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pairs) < 2:
        return {"rho": None, "sample_size": len(pairs), "strength": "insufficient"}

    xs = [a for a, _ in pairs]
    ys = [b for _, b in pairs]
    rho = pearson(rank_data(xs), rank_data(ys))
    if rho is None:
        return {"rho": None, "sample_size": len(pairs), "strength": "undefined"}

    absolute = abs(rho)
    if absolute < 0.2:
        strength = "very weak"
    elif absolute < 0.4:
        strength = "weak"
    elif absolute < 0.6:
        strength = "moderate"
    elif absolute < 0.8:
        strength = "strong"
    else:
        strength = "very strong"

    return {"rho": round(rho, 4), "sample_size": len(pairs), "strength": strength}


def confidence_from_sample(sample_size: int) -> str:
    if sample_size < 14:
        return "insufficient"
    if sample_size < 30:
        return "low"
    if sample_size < 60:
        return "moderate"
    return "high"
