import csv
import sys


# compute the maximum count

def get_max(x, subx):
    count = [0] * len(x)
    for i in range(len(x) - len(subx), -1, -1):
        if x[i: i + len(subx)] == subx:
            if i + len(subx) > len(x) - 1:
                count[i] = 1
            else:
                count[i] = 1 + count[i + len(subx)]
    return max(count)
    

# checks if the count maches

def print_match(reader, actual):
    for line in reader:
        person = line[0]
        values = [int(val) for val in line[1:]]
        if values == actual:
            print(person)
            return
    print("no match")


def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    else:
        with open(sys.argv[1], "r") as file:
            database = csv.reader(file)
            
            all_seq = next(database)[1:]
        
            with open(sys.argv[2]) as file2:
                str_dic = file2.read()
            
                sample = [get_max(str_dic, seq) for seq in all_seq]
            print_match(database, sample)
            
            
if __name__ == "__main__":
    main()

