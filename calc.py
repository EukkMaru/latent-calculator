#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

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
PRECISION = 0.00001  # binary search precision for percentage
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

def rating_from_percent(difficulty, percent):
    if percent > MAX_ACHIEVABLE:
        percent = MAX_ACHIEVABLE
    mn = magic_number(percent)
    rating = difficulty * mn
    rank, const = find_rank_by_percent(percent)
    return rating, rank, const, mn

def percent_from_desired_rating(difficulty, desired_rating):
    target_mn = desired_rating / difficulty
    low, high = 0.0, MAX_ACHIEVABLE
    while high - low > PRECISION:
        mid = (low + high) / 2
        if magic_number(mid) < target_mn:
            low = mid
        else:
            high = mid
    required_percent = round(high, 4)
    rank, const = find_rank_by_percent(required_percent)
    return required_percent, rank, const, magic_number(required_percent)

def main():
    parser = argparse.ArgumentParser(description="Latent Kingdom Calculator (EXPERT/MASTER)")
    parser.add_argument("-p", "--percent", type=float, help="Accuracy percentage (0.0000–101.0000)")
    parser.add_argument("-r", "--desired", type=float, help="Desired rating value")
    parser.add_argument("-d", "--difficulty", choices=["EXPERT", "MASTER"], default="MASTER")
    args = parser.parse_args()

    if (args.percent is None) == (args.desired is None):
        print("Error: specify one of --percent (-p) or --desired (-r)")
        return

    difficulty = DIFFICULTIES[args.difficulty]

    if args.percent is not None:
        percent = min(args.percent, MAX_PERCENT)
        rating, rank, const, mn = rating_from_percent(difficulty, percent)
        print(f"\nDifficulty: {args.difficulty} ({difficulty})")
        print(f"Rank: {rank} (constant {const})")
        print(f"Accuracy: {percent:.4f}%")
        # print(f"Magic Number: {mn:.4f}")
        print(f"Rating: {rating:.2f}\n")

    elif args.desired is not None:
        desired = args.desired
        required_percent, rank, const, mn = percent_from_desired_rating(difficulty, desired)
        if required_percent > MAX_PERCENT:
            print(f"\nDesired rating {desired:.2f} is impossible (max accuracy {MAX_PERCENT:.4f}%).\n")
            return
        rating = difficulty * mn
        print(f"\nDifficulty: {args.difficulty} ({difficulty})")
        print(f"Desired Rating: {desired:.2f}")
        print(f"Required Rank: {rank} (constant {const})")
        print(f"Required Accuracy: {required_percent:.4f}%")
        # print(f"Magic Number: {mn:.4f}")
        print(f"Rating Achieved: {rating:.2f}\n")
        
        if required_percent > 87.9659:
            print(f"You need to improve {required_percent - 87.9659:.4f}%. YOU ARE TRASH.\n")

if __name__ == "__main__":
    main()
