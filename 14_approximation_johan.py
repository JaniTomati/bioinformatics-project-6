#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import subprocess
import numpy as np
from itertools import compress


def parse_arguments():
    """ Parse the command line arguments """
    S = "hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh"
    benchmarks = ""
    hpview_location = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="HP-string", default=S)
    parser.add_argument("-b", help="Run program on benchmarks.txt <path-to-benchmark.txt>", default=benchmarks)
    parser.add_argument("-v", help="Validate score using hpview3k.py <path-to-hpview3k.py>", default=hpview_location)
    args = parser.parse_args()
    S = args.s
    if args.b != "":
        benchmarks = args.b
        if not os.path.exists(benchmarks):
            sys.exit("Error: " + benchmarks + " does not exist!")
    if args.v != "":
        hpview_location = args.v
        # check whether hpview3k exists in the given location
        if hpview_location != "":
            if not os.path.exists(hpview_location):
                sys.exit("Error: " + hpview_location + " does not exist!")


    return S, benchmarks, hpview_location


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


def score(hp, fold):
    """ Score the non-connected H-H bonds in the fold of the hp sequence """
    #Find mid
    mid = None
    for i in range(len(fold)):
        if fold[i:i+3] == "esw":
            mid=i
            break
    #Compute guide list
    if hp[0] =="h":
        pos = ["mih"]
    else:
        pos = ["mip"]
    i=1
    while i<mid:
        if fold[i-1] =="n":
            count=0
            while fold[i-1] =="n":
                count+=1
                if hp[i] == "h":
                    pos.append("lih")
                else:
                    pos.append("lip")
                i+=1
            for k in range(count):
                if hp[i+k] =="h":
                    pos.append("lih")
                else:
                    pos.append("lip")
            i=i+count
        else:
            if hp[i]=="h":
                pos.append("mih")
            else:
                pos.append("mip")
            i+=1
    for k in range(2):
        if hp[mid+k] =="h":
            pos.append("mih")
        else:
            pos.append("mip")
    midi=mid+2
    for k in range(2):
        if hp[midi+k] =="h":
            pos.append("mjh")
        else:
            pos.append("mjp")
    j=midi+2
    while j<len(hp):
        if fold[j-1] =="s":
            count=0
            while fold[j-1] =="s":
                count+=1
                if hp[j] == "h":
                    pos.append("ljh")
                else:
                    pos.append("ljp")
                j+=1
            for k in range(count):
                if hp[j+k] =="h":
                    pos.append("ljh")
                else:
                    pos.append("ljp")
            j=j+count
        else:
            if hp[j]=="h":
                pos.append("mjh")
            else:
                pos.append("mjp")
            j+=1
    #Count score
    i=mid
    j=mid+3
    score=0
    while i>=0 or j<len(hp):
        if i<0:
            if pos[j][0] =="l":
                count=0
                while pos[j][0]=="l":
                    count+=1
                    j+=1
                for k in range((count//2)-1):
                    if pos[j-1-k][2] =="h" and pos[j-count+k][2] == "h":
                        score+=1
                if pos[j][2] =="h" and pos[j+count-1][2] =="h":
                    score +=1
            else:
                j+=1
        elif j == len(hp):
            if pos[i][0]=="l":
                count=0
                while pos[i][0]=="l":
                    count+=1
                    i-=1
                for k in range((count//2)-1):
                    if pos[i+1+k][2] =="h" and pos[i+count-k][2] == "h":
                        score+=1
                if pos[i][2] =="h" and pos[i+count+1][2] =="h":
                    score +=1
            else:
                i-=1
        else:
            if pos[i][0] =="m" and pos[j][0] == "m":
                if pos[i][2] == "h" and pos[j][2] == "h":
                    score+=1
                i-=1
                j+=1
            elif pos[i][0]=="l":
                count=0
                while pos[i][0]=="l":
                    count+=1
                    i-=1
                for k in range((count//2)-1):
                    if pos[i+1+k][2] =="h" and pos[i+count-k][2] == "h":
                        score+=1
                if pos[i][2] =="h" and pos[i+count+1][2] =="h":
                    score +=1
            elif pos[j][0] =="l":
                count=0
                while pos[j][0]=="l":
                    count+=1
                    j+=1
                for k in range((count//2)-1):
                    if pos[j-1-k][2] =="h" and pos[j-count+k][2] == "h":
                        score+=1
                if pos[j][2] =="h" and pos[j-count-1][2] =="h":
                    score +=1

    return score


def hp(sequence):
    """ Calculate the fold of the hp sequence and assign to Christians data structure """
    m = get_matches(sequence)
    fold = get_abs_path(m)
    our_score = score(sequence, fold)
    return fold, our_score


def main():
    # get command line arguments
    S, benchmarks, hpview_location = parse_arguments()

    # run program on benchmarks
    if benchmarks != "":
        # file that holds the scores for each hp string
        hp_strings = read_in_hp_strings(benchmarks)

        out_file = "approximation_results.txt"
        if os.path.exists(out_file):
             os.remove(out_file)

        count = 1
        for hp_string in hp_strings:
            sequence = hp_string[0]
            print("\n---------------------------------------------------------")
            print("Using sequence: " + sequence)

            start_time = time.time()
            fold, our_score = hp(sequence)
            end_time = time.time()

            print("Fold in absolute format:", fold)
            print("\nElapsed time:", end_time-start_time)
            print("Our score:", our_score)
            print("Benchmark score:", hp_string[1])

            # write performance of the algorithm to a file
            with open(out_file, "a") as out:
                out.write(str(count) + ": " + hp_string[0] + " " + fold + " -" + str(our_score) + "\n")
            count += 1

            # validate the score by running hpview3k
            if hpview_location != "":
                print("\nValidation:")
                os.system("python3 " + hpview_location + " " + sequence + " " + fold)
    else: # run program on input sequence
        sequence = S
        print("\nUsing sequence: " + sequence)

        start_time = time.time()
        fold, our_score = hp(sequence)
        end_time = time.time()

        print("Fold in absolute format:", fold)
        print("\nElapsed time:", end_time-start_time)
        print("Our score:", our_score)

        # validate the score by running hpview3k
        if hpview_location != "":
            print("\nValidation:")
            os.system("python3 " + hpview_location + " " + sequence + " " + fold)


if __name__ == '__main__':
    main()
