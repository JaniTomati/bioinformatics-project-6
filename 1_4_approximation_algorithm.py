
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

# local imports
import utilities.hpview3k


S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"
S2 = "hhphphphphhhhphppphppphpppphppphppphphhhhphphphphh"


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


def size_threshold(S):
    """ Size >= 1/2 * min(|even(S)|, |odd(S)|)"""
    return 1/2 * min(even(S), odd(S))


def OPT(S):
    """ Optimal fold: An h can form at most 2 bonds with h's of opposite parity """
    return 2 * min(even(S), odd(S))


def match(S):
    """ Match even's from the left with odd's from the right and vice versa """
    matches_left = np.zeros((len(S), len(S)), dtype=int)
    matches_right = np.zeros((len(S), len(S)), dtype=int)

    # counters for traversing the string
    front = 0 # even
    back = len(S) - 1 if len(S) % 2 == 0 else len(S) - 2 # odd
    count_left = 0
    while front <= 1/2 * len(S) or back >= 1/2 * len(S):
        if S[front] == "h" and S[back] == "h":
            # evens from the left, with odds from the right
            matches_left[front, back] = 1
            matches_left[back, front] = 1
            front += 2
            back  -= 2
            count_left += 1
        elif S[front] == "h":
            back -= 2
        else:
            front += 2

    front = 1 # odd
    back = len(S) - 2 if len(S) % 2 == 0 else len(S) - 1 # even
    count_right = 0
    while front <= 1/2 * len(S) or back >= 1/2 * len(S):
        if S[front] == "h" and S[back] == "h":
            # odds from the left, with evens from the right
            matches_right[front, back] = 1
            matches_right[back, front] = 1
            front += 2
            back  -= 2
            count_right += 1
        elif S[front] == "h":
            back -= 2
        else:
            front += 2

    if count_left >= count_right:
        return matches_left
    else:
        return matches_right


def fold(S):
    """ Create a fold from the matching """
    F = 0

    # match odd's and even's
    matching = match(S)


    return F


def main():
    F = fold(S)
    pass


if __name__ == '__main__':
    main()
