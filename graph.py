#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import plotly.graph_objects as go

DIFFICULTIES = {
    "EXPERT": 12.8,
    "MASTER": 14.9
}

RANKS = [
    ("SSS+", 100.5, 22.4),
    ("SSS", 100.0, 21.6),
    ("SS+", 99.5, 21.1),
    ("SS", 99.0, 20.8),
    ("S+", 98.0, 20.3),
    ("S", 97.0, 20.0),
    ("AAA", 94.0, 16.8),
    ("AA", 90.0, 15.2),
    ("A", 80.0, 13.6)
]

MAX_PERCENT = 101.0
REFERENCE_LINES = {
    263: "B30",
    290: "B1"
}
MAX_ACHIEVABLE = 100.5  # scores over this are rounded down to 100.5

def find_rank_by_percent(percent):
    for rank, threshold, const in RANKS:
        if percent >= threshold:
            return rank, const
    return "Below A", RANKS[-1][2]

def magic_number(percent):
    if percent > MAX_ACHIEVABLE:
        percent = MAX_ACHIEVABLE
    rank, const = find_rank_by_percent(percent)
    return (percent / 100) * const

def generate_curve(difficulty_value):
    percentages = np.linspace(80, MAX_PERCENT, 2101)
    ratings = np.array([difficulty_value * magic_number(p) for p in percentages])
    return percentages, ratings

def main():
    fig = go.Figure()
    colors = {"EXPERT": "#ff8282", "MASTER": "#a23ef3"}

    for name, diff in DIFFICULTIES.items():
        x, y = generate_curve(diff)
        fig.add_trace(go.Scatter(
            x=x, y=y, mode='lines',
            line=dict(color=colors[name], width=3, shape='hv'),  # 'hv' step plot
            name=f"{name} ({diff})"
        ))

    for rating_value, label in REFERENCE_LINES.items():
        fig.add_shape(
            type="line", x0=80, x1=MAX_PERCENT, y0=rating_value, y1=rating_value,
            line=dict(color="blue", width=2, dash="dot")
        )
        fig.add_annotation(
            x=80.5, y=rating_value + 1,
            text=f"{label} ({rating_value})",
            showarrow=False, font=dict(color="blue")
        )

    for rank, threshold, _ in RANKS:
        if threshold >= 80:
            fig.add_shape(
                type="line", x0=threshold, x1=threshold, y0=100, y1=max(REFERENCE_LINES.keys()) + 50,
                line=dict(color="gray", width=1, dash="dash")
            )
            fig.add_annotation(
                x=threshold + 0.2, y=105, text=rank,
                textangle=90, showarrow=False, font=dict(color="gray", size=10)
            )

    fig.update_layout(
        xaxis_title="Accuracy (%)",
        yaxis_title="Rating",
        xaxis=dict(range=[80, MAX_PERCENT]),
        yaxis=dict(range=[100, max(REFERENCE_LINES.keys()) + 50]),
        template="plotly_white",
        legend=dict(font=dict(size=12)),
        margin=dict(l=50, r=50, t=20, b=50)
    )

    fig.show()

if __name__ == "__main__":
    main()
