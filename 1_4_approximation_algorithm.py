
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
from math import floor
import itertools

# local imports
import utilities.hpview3k


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
    matching_left = []
    matching_right = []

    # counters for traversing the string
    front = 0
    back = len(S) - 1
    count_left = 0
    count_right = 0

    while front < 1/2 * len(S) or back >= 1/2 * len(S):
        print(front, back)
        if S[front] == "h" and S[back] == "h":
            if front % 2 == 0 and back % 2 == 1: # evens from the left, with odds from the right
                matching_left.append((front, back))
                front += 1
                back  -= 1
                count_left += 1
            elif front % 2 == 1 and back % 2 == 0: # odds from the left, with evens from the right
                matching_right.append((front, back))
                front += 1
                back  -= 1
                count_right += 1
        elif S[front] == "h":
            back -= 1
        else:
            front += 1

    if count_left >= count_right:
        print("Score of matching:", count_left)
        return matching_left
    else:
        print("Score of matching:", count_right)
        return matching_right


def create_absolute_format(current_match, next_match, dir):
    """ Decide the direction to take from the indices that are supposed to match """
    direction = {"east" : ["e", "n", "s"], "west" : ["w", "s", "n"]}
    fold = ""

    dst = abs(next_match - current_match)
    if dst == 1:
        fold += direction[dir][0]
    if dst == 2:
        fold += 2 * direction[dir][0]
    else: # make a turn
        turn = floor(dst / 2)
        if dst % 2 == 0:
            if dir == "west":
                fold += direction[dir][1]
            fold += (turn - 1) * direction[dir][1]
            fold += direction[dir][0]
            fold += (turn - 1) * direction[dir][2]
            if dir == "east":
                fold += direction[dir][0]
        else:
            fold += turn * direction[dir][1]
            fold += direction[dir][0]
            fold += turn * direction[dir][2]

    return fold


def fold(S):
    """ Create a fold from the matching """
    F = "" # fold
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

    fold1 = ""
    fold2 = ""

    # check everything before first match
    if matching[0][0] != 0:
        fold1 += create_absolute_format(0, matching[0][0], "east")

    # do in-between matches
    for i in range(len(matching) - 1):
        fold1 += create_absolute_format(matching[i][0], matching[i + 1][0], "east")
        fold2 += create_absolute_format(matching[i][1], matching[i + 1][1], "west")

    # check everything after last match
    if matching[0][1] != len(S) - 2:
        fold2 += create_absolute_format(matching[0][1], len(S) - 2, "west")

    # match from last match upper half to end
    if matching[-1][0] != half - 1:
        fold1 += create_absolute_format(matching[-1][0], half, "east")

    # match from end to first match lower half
    if matching[-1][1] != half:
        fold2 += create_absolute_format(half, matching[-1][1], "west")

    # create full fold
    F = fold1 +fold2[::-1]

    print(F)
    print(len(S), len(F))

    return F


def main():
    S, visual_fold = parse_arguments()
    F = fold(S)


if __name__ == '__main__':
    main()
