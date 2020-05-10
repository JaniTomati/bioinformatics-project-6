
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

# local imports
import utilities.hpview3k


S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"


def even(S):
    """ Hydrophobes in S at even-indexed positions """
    result = 0
    for i in range(len(S)):
        if S[i] == "h" and i % 2 == 0:
            result += 1
    return result


def odd(S):
    """ Hydrophobes in S at odd-indexed positions """
    result = 0
    for i in range(len(S)):
        if S[i] == "h" and i % 2 == 1:
            result += 1
    return result


def match(S):
    """ Match even's from the left with odd's from the right and vice versa """
    n = len(S)
    matches = np.zeros((n, n), dtype=int)

    front = 0
    back  = len(S) - 1 # counters for traversing the string

    while front <= 1/2 * len(S) or back >= 1/2 * len(S):
        if S[front] == "h" and S[back] == "h":
            if front % 2 == 1 and back % 2 == 0:
                # print(front, back)
                matches[front, back] = 1
                matches[back, front] = 1
                front += 1
                back  -= 1
            elif front % 2 == 0 and back % 2 == 1:
                # print(front, back)
                matches[front, back] = 1
                matches[back, front] = 1
                front += 1
                back  -= 1
            else:
                front += 1
        elif S[front] == "h":
            back -= 1
        else:
            front += 1

    return matches


def main():
    # match odd's and even's
    matches = match(S)

    pass


if __name__ == '__main__':
    main()
