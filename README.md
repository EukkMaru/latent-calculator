# Latent Kingdom Rating Calculator

Calculates rating results for **Latent Kingdom** from **maimai DX**.

## Overview

This script allows you to calculate your rating based on your accuracy percentage or find the required accuracy to achieve a desired rating for the EXPERT or MASTER difficulty levels.

It uses the game’s ranking system to provide the corresponding rank and rating.

## Requirements

- Python 3.x

## Usage

Run the script from the command line:

```bash
python3 latent_kingdom_calculator.py [options]
```

### Options

- `-p`, `--percent`  
  Provide your accuracy percentage (0.0000–101.0000).  
  Example:  
  ```bash
  python3 latent_kingdom_calculator.py -p 95.5 -d MASTER
  ```

- `-r`, `--desired`  
  Provide your desired rating value to find the required accuracy.  
  Example:  
  ```bash
  python3 latent_kingdom_calculator.py -r 200 -d EXPERT
  ```

- `-d`, `--difficulty`  
  Specify difficulty level (`EXPERT` or `MASTER`). Default is `MASTER`.

## Examples

1. **Calculate rating from accuracy**  

```bash
python3 latent_kingdom_calculator.py -p 98.5 -d MASTER
```

Output:

```
Difficulty: MASTER (14.9)
Rank: S+ (constant 20.3)
Accuracy: 98.5000%
Rating: 302.47
```

2. **Calculate required accuracy for desired rating**  

```bash
python3 latent_kingdom_calculator.py -r 300 -d EXPERT
```

Output:

```
Difficulty: EXPERT (12.8)
Desired Rating: 300.00
Required Rank: SSS (constant 21.6)
Required Accuracy: 99.4444%
Rating Achieved: 300.00
```

## Notes

- If your desired rating is impossible given the maximum achievable accuracy, the script will notify you.  
- The script includes a small humorous comment if your required accuracy is very high.
