from math import comb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

Rs = np.linspace(0,1,num=100,endpoint=True)
Ys = np.linspace(0, 10, num=11, endpoint=True)

import json
 
with open('sample.json', 'r') as openfile:
     json_object = json.load(openfile)
 
TRIALS = json_object["TRIALS"]
TOTAL_HEADS = json_object["TOTAL_HEADS"]
PREV_GAMES = json_object["PREV_GAMES"]
NUM_HEADS = json_object["NUM_HEADS"]


def likelihood_distribution():
    comb1 = comb(TRIALS, TOTAL_HEADS)
    comb2 = comb(PREV_GAMES * 10, TOTAL_HEADS - NUM_HEADS)
    prev = comb2 * (Rs ** (TOTAL_HEADS - NUM_HEADS) ) * ((1-Rs)**((PREV_GAMES * 10) - (TOTAL_HEADS - NUM_HEADS)))
    curr = comb1 * (Rs **(TOTAL_HEADS) ) * ((1-Rs)**((TRIALS) - (TOTAL_HEADS)))
    return (prev, curr)

def get_binomial_pmfs(arr,r):
    def get(x):
        return scipy.stats.binom(10, r).pmf(x)
    np.vectorize(get)
    return get(arr)




def plot_likelihood():
    expected_val_of_r = TOTAL_HEADS / TRIALS
    std = ((TOTAL_HEADS * (TRIALS - TOTAL_HEADS)) / (((TRIALS)**2)*(TRIALS + 1))) ** (1/2)
    to_test1 = (expected_val_of_r + expected_val_of_r -( 2 * std)) / 2
    to_test_2 = (expected_val_of_r + expected_val_of_r + ( 2 * std)) / 2
    prev, curr = likelihood_distribution()
    plt.subplot(2,2,1)
    plt.plot(Rs, prev, color='red', label = f"{PREV_GAMES*10} Trials, {TOTAL_HEADS - NUM_HEADS} Heads")
    plt.plot(Rs, curr, color='green', label = f"{TRIALS} Trials, {TOTAL_HEADS} Heads")
    plt.xlabel("Probability of Head")
    plt.ylabel("Likelihood of x heads in y trials")
    plt.legend()
    colors = ["green", "green", "green", "green", "green", "green", "green", "red", "red", "red", "red"]
    plt.subplot(2,2,2)
    y_axis = get_binomial_pmfs(Ys, expected_val_of_r)
    plt.bar(Ys, y_axis, color=colors)
    plt.xlabel("Num of heads")
    plt.ylabel("Probability")
    plt.subplot(2,2,3)
    y_axis = get_binomial_pmfs(Ys, to_test1)
    plt.bar(Ys, y_axis, color=colors)
    plt.xlabel("Num of heads")
    plt.ylabel("Probability")
    plt.subplot(2,2,4)
    y_axis = get_binomial_pmfs(Ys, to_test_2)
    plt.bar(Ys, y_axis, color=colors)
    plt.xlabel("Num of heads")
    plt.ylabel("Probability")



    plt.show()





def new():

    plot_likelihood()  


new()