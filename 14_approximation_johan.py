#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import subprocess
import numpy as np
from itertools import compress


# -------- Start Christians Code from hpview3k.py --------
class HPFold:
    def __init__ (self, s):
        legal = {'h':'h', 'p':'p', 'H':'h', 'P':'p'}
        self.seq = []
        i = 1
        for c in s:
            if c in legal.keys():
                if legal[c] == 'h' and i % 2 == 0:
                    self.seq.append('H')
                else:
                    self.seq.append(legal[c])
                i = i + 1


    def __len__ (self):
        return len(self.seq)


    def SetRelFold (self, relfold):
        """
        Fold seq according to a description in relavtive format, i.e.
        a sequence of {f,l,r}'s which describe each step as (f)orward,
        (l)eft, or (r)ight.
        """
        turn = {'f':0, 'l':-1, 'r':1}
        direction = {0:'e', 1:'s', 2:'w', 3:'n'}
        absfold = []
        curr = 0
        for relstep in relfold:
            absstep = (curr + turn[relstep]) % 4
            absfold.append(direction[absstep])
            curr = absstep
        return self.SetAbsFold(absfold)


    def SetAbsFold (self, absfold):
        """
        Fold seq according to a description in absolute format, i.e.
        s sequence of {n,s,e,w}'s which describe each step as (n)orth,
        (s)outh, (e)ast, or (w)est.
        """
        self.legal_fold = (True, 0)
        self.grid = {}
        self.grid[0,0] = [0]
        i = j = self.min_i= self.max_i = self.min_j = self.max_j = 0
        k = 1
        for step in absfold:
            if step == 'n':
                i = i - 1
            elif step == 's':
                i = i + 1
            elif step == 'e':
                j = j + 1
            elif step == 'w':
                j = j - 1
            if (i,j) in self.grid.keys():
                self.legal_fold = (False, k)
                self.grid[i,j].append(k)
            else:
                self.grid[i,j] = [k]
            k = k + 1
            self.min_i = min(i, self.min_i)
            self.max_i = max(i, self.max_i)
            self.min_j = min(j, self.min_j)
            self.max_j = max(j, self.max_j)
        return self.legal_fold[0]


    def ContainNeighbors(self, l1, l2):
        """
        Returns true if there exists k1 in l1 and k2 in l2 such that
        abs(k1-k2) is 1, i.e. if the indices in l1 and l2 contain a
        pair of neighbors in seq.
        """
        res = False
        for k1 in l1:
            for k2 in l2:
                if abs(k1-k2) == 1:
                    res = True
        return res


    def ContainHHs(self, l1, l2):
        """
        Returns true if there exists k1 in l1 and k2 in l2 where there
        is a 'h' at position k1 and k2 in seq, i.e. if the indices in
        l1 and l2 contain a pair which can make a h-h bond.
        """
        res = False
        for k1 in l1:
            for k2 in l2:
                if (self.seq[k1] == "h" or self.seq[k1] == "H") and (self.seq[k2] == "h" or self.seq[k2] == "H"):
                    res = True
        return res


    def PrintFold(self):
        """
        Print fold and output its score
        """
        score = 0
        print()
        for i in range(self.min_i, self.max_i+1):
            for j in range(self.min_j, self.max_j+1):
                if (i,j) in self.grid.keys():
                    l1 = self.grid[i,j]
                    if len(l1) == 1:
                        print(self.seq[l1[0]], end="")
                    else:
                        print("X", end="")
                    if (i,j+1) in self.grid.keys():
                        l2 = self.grid[i,j+1]
                        if self.ContainNeighbors(l1,l2):
                            print("-", end="")
                        elif self.ContainHHs(l1, l2):
                            print("*", end="")
                            score = score + 1
                        else:
                            print(" ", end="")
                    else:
                        print(" ", end="")
                else:
                    print(".", end="")
                    print(" ", end="")
            print()

            for j in range(self.min_j, self.max_j+1):
                if (i,j) in self.grid.keys() and (i+1,j) in self.grid.keys():
                    l1 = self.grid[i,j]
                    l2 = self.grid[i+1,j]
                    if self.ContainNeighbors(l1,l2):
                        print("|", end="")
                    elif self.ContainHHs(l1,l2):
                        print("*", end="")
                        score = score + 1
                    else:
                        print(" ", end="")
                else:
                    print(" ", end="")
                print(" ", end="")
            print()

        if self.legal_fold[0]:
            print("Score: %d" % (score))
        else:
            print("Illegal fold after %d steps" % (self.legal_fold[1]))
        return score


def make_absfold(f):
    absfold = []
    for c in f.lower():
        if c == 'n' or c == 's' or c == 'e' or c == 'w':
            absfold.append(c)
    return absfold


def make_relfold(f):
    relfold = []
    for c in f.lower():
        if c == 'f' or c == 'l' or c == 'r':
            relfold.append(c)
    return relfold


# -------- End Christians Code --------


def parse_arguments():
    """ Parse the command line arguments """
    S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"
    benchmarks = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="HP-string", default=S)
    parser.add_argument("-b", help="Run program on benchmarks.txt [Y/n]", default=benchmarks)
    args = parser.parse_args()
    S = args.s
    if args.b == "Y" or args.b == "y":
        benchmarks = True

    return S, benchmarks


def read_in_hp_strings(file):
    """ Read the benchmark file to compute the scores for our own algorithm """
    hp_strings = []
    with open(file) as f:
        lines = f.read().splitlines()

    for line in lines:
        split = line.split(" ")
        print(split)
        split[2] = int(split[2]) * -1 # remove - infront of benchmarks score
        hp_strings.append(split[1:])

    return hp_strings


def get_matches(seq_string):
    """ Match evens and odds from both sides and return the matching with the biggest size """
    l   = len(seq_string)
    hp = list(seq_string.lower())

    x = [True, False] * (l // 2)
    if l%2 == 1: x.append(True)

    y = [x == "h" for x in hp]

    z = list(compress(x, y))
    tf = ft = 0
    for i in range(len(z)//2):
        if [z[i], z[-i]] == [True, False]: tf += 1
        if [z[i], z[-i]] == [False, True]: ft += 1
    equals_first = tf>ft

    match = list()
    for i in range(l):
        if i < l//2:
            match.append(y[i] and x[i] == equals_first)
        if i >= l//2:
            match.append(y[i] and x[i] != equals_first)
        # There might be a bug here!

    return match


def get_abs_path(m):
    """ Create a folding of the matching and return a string in absolute format """
    abs_coords = list()
    k = 0

    setting = {"east":{"away": "n", "closer": "s", "forward": "e"},
              "west": {"away": "s", "closer": "n", "forward": "w"}}
    coords = setting["east"]

    while k < len(m):

        if m[k] == False and k == 0:
            while m[k] == False:
                abs_coords.append(coords["forward"])
                k += 1
            abs_coords.append(coords["forward"])
            k += 1

        if m[k] and k == 0:
            abs_coords.append(coords["forward"])
            k += 1


        h = 2

        if k+h > len(m):
            abs_coords.append(coords["forward"]*abs(len(m)-(k+h)))
            break


        while np.sum(m[k:k+h]) < 1:
            h += 1
            if k+h > len(m):
                break

        if np.sum(m[k:k+h]) == 0:
            abs_coords.append(coords["forward"]*(h-1))
            break


        if h%2 == 1:
            abs_coords.append(coords["forward"]*(h//2))
            abs_coords.append(coords["closer"])

            coords = setting["west"] # Now we go back

            abs_coords.append(coords["forward"]*(h//2))

            k += h

        elif h == 2:
            abs_coords.append(coords["forward"]*2)
            k += h

        elif h > 2 and h % 2 == 0:
            bulge_length = h-1
            abs_coords.append(coords["away"]*(bulge_length//2))
            abs_coords.append(coords["forward"])
            abs_coords.append(coords["closer"]*(bulge_length//2))
            abs_coords.append(coords["forward"])
            k += h

    final = "".join(abs_coords)[1:]
    return final


def hp(sequence):
    """ Calculate the fold of the hp sequence and assign to Christians data structure """
    m = get_matches(sequence)#
    print("Length of matching:", len(m))
    print(m)
    fold = get_abs_path(m)

    seq = HPFold(sequence)
    absfold = make_absfold(fold)
    relfold = make_relfold(fold)
    if len(absfold) == len(seq) - 1:
        seq.SetAbsFold(absfold)
    elif len(relfold) == len(seq) - 1:
        seq.SetRelFold(relfold)

    return fold, seq


def main():
    # get command line arguments
    S, benchmarks = parse_arguments()

    # run program on benchmarks
    if benchmarks:
        # read in benchmark strings
        in_file = "benchmarks.txt"
        if os.path.exists(in_file):
             hp_strings = read_in_hp_strings(in_file)
        else:
            sys.exit("Error: " + in_file + " does not exist!")

        # file that holds the scores for each hp string
        out_file = "approximation_results.txt"
        if os.path.exists(out_file):
             os.remove(out_file)

        count = 1
        for hp_string in hp_strings:
            sequence = hp_string[0]
            print("\n---------------------------------------------------------")
            print("Using sequence: " + sequence)

            start_time = time.time()
            fold, seq = hp(sequence)
            end_time = time.time()

            print("Fold in absolute format:", fold)
            print("\nElapsed time:", end_time-start_time)
            print("Benchmark score:", hp_string[1])
            score = seq.PrintFold()

            # write performance of the algorithm to a file
            with open(out_file, "a") as out:
                out.write(str(count) + ": " + hp_string[0] + " " + fold + " -" + str(score) + "\n")
            count += 1
    else: # run program on input sequence
        sequence = S
        print("Using sequence: " + sequence)

        start_time = time.time()
        fold, seq = hp(sequence)
        end_time = time.time()

        print("Fold in absolute format:", fold)
        print("\nElapsed time:", end_time-start_time)
        score = seq.PrintFold()


if __name__ == '__main__':
    main()
