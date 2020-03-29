import random
import time

def main():
    f = open("data/test.txt", 'w', buffering=10)
    switcher = {0: "A", 1: "C", 2: "G", 3: "T"}

    for i in range(1, 100000):
        symbol = random.choice(switcher)
        f.write(symbol)
        time.sleep(0.1)

    f.close()

if __name__ == "__main__":
    main()