import time

def build_guess(state):
    if type(state) == int:
        return ["NUMBER", state]
    else:
        return ["RULE", ["pot", state[1], -1]]

def player(number_guesses, rule_guesses):
    tree = {
        512: {"T": 5, "S": 243, "L": 9},
        5:   {"T": ("rule", 1), "S": ("rule", 9), "L": ("rule", 3)},
        243: {"T": ("rule", 5), "S": 65, "L": ("rule", 8)},
        65:  {"S": ("rule", 10), "L": ("rule", 7)},
        9:   {"T": ("rule", 2), "S": ("rule", 6), "L": ("rule", 4)}
    }
    tree_raw = {'type': 'number', 'n': 512, 'branches': {'T': {'type': 'number', 'n': 5, 'branches': {'T': {'type': 'rule', 'p': 1}, 'S': {'type': 'rule', 'p': 9}, 'L': {'type': 'rule', 'p': 3}}}, 'S': {'type': 'number', 'n': 243, 'branches': {'T': {'type': 'rule', 'p': 5}, 'S': {'type': 'number', 'n': 65, 'branches': {'S': {'type': 'rule', 'p': 10}, 'L': {'type': 'rule', 'p': 7}}}, 'L': {'type': 'rule', 'p': 8}}}, 'L': {'type': 'number', 'n': 9, 'branches': {'T': {'type': 'rule', 'p': 2}, 'S': {'type': 'rule', 'p': 6}, 'L': {'type': 'rule', 'p': 4}}}}}
    curr = tree_raw

    for guess in number_guesses:
        if guess[1] == "maior":
            curr = curr['branches']['L']
        elif guess[1] == 'menor':
            curr = curr['branches']['S']
        else:
            curr = curr['branches']['T']

    if curr['type'] == 'number':
        return ['NUMBER', curr['n']]
    else:
        ret = ['RULE', ['pot', curr['p'], -1]]
        return ret