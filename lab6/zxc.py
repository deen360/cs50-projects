# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for read in reader:
            teams.append(team)
    print(f"{team[0]}")