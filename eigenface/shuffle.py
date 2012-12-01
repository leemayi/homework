import sys
import random


def main():
    data = sys.stdin.readlines()
    random.shuffle(data)
    sys.stdout.writelines(data)


if __name__ == '__main__':
    main()
