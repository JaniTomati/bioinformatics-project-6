
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
    matching_left = np.zeros((len(S), len(S)), dtype=int)
    matching_right = np.zeros((len(S), len(S)), dtype=int)

    # counters for traversing the string
    front = 0
    back = len(S) - 1
    count_left = 0
    count_right = 0
    while front <= 1/2 * len(S) or back >= 1/2 * len(S):
        if S[front] == "h" and S[back] == "h":
            if front % 2 == 0 and back % 2 == 1: # evens from the left, with odds from the right
                matching_left[front, back] = 1
                matching_left[back, front] = 1
                front += 1
                back  -= 1
                count_left += 1
            elif front % 2 == 1 and back % 2 == 0: # odds from the left, with evens from the right
                matching_right[front, back] = 1
                matching_right[back, front] = 1
                front += 1
                back  -= 1
                count_right += 1
        elif S[front] == "h":
            back -= 1
        else:
            front += 1

    if count_left >= count_right:
        return matching_left
    else:
        return matching_right


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
