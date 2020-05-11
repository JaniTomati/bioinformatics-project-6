
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from math import floor
import itertools

# local imports
import utilities.hpview3k


# S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"
# S2 = "hhphphphphhhhphppphppphpppphppphppphphhhhphphphphh"


def parse_arguments():
    """ Parse the command line arguments """
    S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"
    visual_fold = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="HP-string", default=S)
    parser.add_argument("-o", help="ASCII output [Y/n]", default=visual_fold)
    args = parser.parse_args()
    S = args.s
    if args.o == "Y" or args.o == "y":
        visual_fold = True

    return S, visual_fold


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
    F = 0 # fold
    directions = {"n" : 0, "e" : 0, "s" : 0, "w" : 0}

    # match odd's and even's
    matching = match(S)

    half = floor(1/2 * len(S))
    S1 = S[0:half]
    S2 = S[half:len(S)]

    if even(S1) >= 1/2 * even(S) and odd(S2) >= 1/2 * odd(S):
        print("Condition 1) satisfied")
    elif even(S2) >= 1/2 * even(S) and odd(S1) >= 1/2 * odd(S):
        print("Condition 2) satisfied")
    else:
        print("Turning point does not satisfy condition 1) or 2).")

    # find fold with lowest free energy, i.e. fold with highest amount of connected, non-bonded H-H
    energy = 0
    # i = 0
    # j = len(S2) - 1
    # while i <= len(S1) and j >= 0:
    #     # print (i, j + len(S1))
    #     if S1[i] == "h" and S2[j] == "h":
    #         print(i, j + len(S1))
    #         print(matching[i,j + len(S1)])
    #     if S1[i] == "p" and S2[j] == "h":
    #         str += "s"
    #     i += 1
    #     j -= 1

    # perm = permutations('ennnne', 3)
    # for permutation in permutations('ennnne', 3):
    #     print("1)")
    #     print(permutation)


    for char1 in itertools.product('en', repeat=len(S1)-1):
        fold1 = "".join(char1)
        for char2 in itertools.product('sw', repeat=len(S2)):
            fold2 = "".join(char2)
            print(fold1)
            print(fold2, "\n")
    return F


def main():
    S, visual_fold = parse_arguments()
    F = fold(S)
    pass


if __name__ == '__main__':
    main()
