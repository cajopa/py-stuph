from random import randrange
from itertools import chain, repeat


STANDARD_TEAMS = [list(range(16)), list(range(16,32)), list(range(32,48)), list(range(48,64))]

def weight_ranking(ranked_teams):
    l = len(ranked_teams)
    return chain.from_iterable(repeat(x, l-i) for i,x in enumerate(ranked_teams))

def select_weighted_random(*ranked_teams):
    weighted_teams = list(chain.from_iterable(weight_ranking(x) for x in ranked_teams))
    
    return weighted_teams[randrange(len(weighted_teams))]
