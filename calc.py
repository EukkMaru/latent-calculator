#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

DIFFICULTIES = {
    "EXPERT": 12.8,
    "MASTER": 14.9,
}

# (Rank, threshold %, constant)
RANKS = [
    ("SSS+", 100.5, 22.4),
    ("SSS", 100.0, 21.6),
    ("SS+", 99.5, 21.1),
    ("SS", 99.0, 20.8),
    ("S+", 98.0, 20.3),
    ("S", 97.0, 20.0),
    ("AAA", 94.0, 16.8),
    ("AA", 90.0, 15.2),
    ("A", 80.0, 13.6),
]

MAX_INPUT = 101.0          # UI/input cap
MAX_ACHIEVABLE = 100.5     # rating cap
PRECISION = 1e-5
BELOW_A_CONST = 0.0        # constant below A

def find_rank_by_percent(percent: float):
    for rank, threshold, const in RANKS:
        if percent >= threshold:
            return rank, const
    return "Below A", BELOW_A_CONST

def clamped(percent: float) -> float:
    return max(0.0, min(percent, MAX_ACHIEVABLE))

def magic_number(percent: float) -> float:
    p = clamped(percent)
    _, const = find_rank_by_percent(p)
    return (p / 100.0) * const

def max_rating_for_difficulty(difficulty: float) -> float:
    return difficulty * magic_number(MAX_ACHIEVABLE)

def rating_from_percent(difficulty: float, percent: float):
    p = clamped(percent)
    mn = magic_number(p)
    rating = difficulty * mn
    rank, const = find_rank_by_percent(p)
    return rating, rank, const, p, mn

def percent_from_desired_rating(difficulty: float, desired_rating: float):
    # Feasibility check against true max (at 100.5%)
    max_rating = max_rating_for_difficulty(difficulty)
    if desired_rating > max_rating + 1e-9:
        return None, None, None, None  # impossible

    target_mn = desired_rating / difficulty
    low, high = 0.0, MAX_ACHIEVABLE
    while high - low > PRECISION:
        mid = (low + high) / 2.0
        if magic_number(mid) < target_mn:
            low = mid
        else:
            high = mid
    required_percent = round(high, 4)
    rank, const = find_rank_by_percent(required_percent)
    mn = magic_number(required_percent)
    return required_percent, rank, const, mn

def main():
    parser = argparse.ArgumentParser(description="Latent Kingdom Calculator (EXPERT/MASTER)")
    parser.add_argument("-p", "--percent", type=float, help="Accuracy percentage (0.0000–101.0000)")
    parser.add_argument("-r", "--desired", type=float, help="Desired rating value")
    parser.add_argument("-d", "--difficulty", choices=["EXPERT", "MASTER"], default="MASTER")
    args = parser.parse_args()

    # Require exactly one of --percent or --desired
    if (args.percent is None) == (args.desired is None):
        print("Error: specify one of --percent (-p) or --desired (-r)")
        return

    difficulty_name = args.difficulty
    difficulty = DIFFICULTIES[difficulty_name]

    if args.percent is not None:
        # Sanitize input and apply rating clamp consistently
        percent_in = max(0.0, min(args.percent, MAX_INPUT))
        rating, rank, const, percent_used, mn = rating_from_percent(difficulty, percent_in)
        print(f"\nDifficulty: {difficulty_name} ({difficulty})")
        print(f"Rank: {rank} (constant {const})")
        print(f"Accuracy: {percent_used:.4f}%")
        print(f"Rating: {rating:.2f}")
        print(f"Max rating at {MAX_ACHIEVABLE:.4f}%: {max_rating_for_difficulty(difficulty):.2f}\n")

    else:
        desired = max(0.0, args.desired)
        required_percent, rank, const, mn = percent_from_desired_rating(difficulty, desired)
        if required_percent is None:
            max_r = max_rating_for_difficulty(difficulty)
            print(f"\nDesired rating {desired:.2f} is impossible "
                  f"(max rating {max_r:.2f} at {MAX_ACHIEVABLE:.4f}%).\n")
            return
        rating = difficulty * mn
        print(f"\nDifficulty: {difficulty_name} ({difficulty})")
        print(f"Desired Rating: {desired:.2f}")
        print(f"Required Rank: {rank} (constant {const})")
        print(f"Required Accuracy: {required_percent:.4f}%")
        print(f"Rating Achieved: {rating:.2f}")
        print(f"Max rating at {MAX_ACHIEVABLE:.4f}%: {max_rating_for_difficulty(difficulty):.2f}\n")

if __name__ == "__main__":
    main()
