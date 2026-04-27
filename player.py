### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
from utils.perfect_pows import perfect_pows

## types:
guess_type = {"NUMBER": "NUMBER", "RULE": "RULE"}
rule_type = {"MOD": "mod", "POW": "pot", "INTERVAL": "int"}
number_direction_type = {"GREATER": "maior", "LESS": "menor"}

## rules control set:
CAN_BE_PERFECT_POW = True
possible_perfect_pows = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

CAN_BE_MOD = True
CAN_BE_INTERVAL = True

## first n found:
n_start = -1
left = -1
right = -1

## DEBUG SECTION
global attempts
attempts = -1


def player(number_guesses, rule_guesses):
    """Função principal do jogador.

    Exemplo de estratégia: chutar regras aleatórias.
    """
    global guess_type, number_direction_type
    global CAN_BE_PERFECT_POW, CAN_BE_MOD, CAN_BE_INTERVAL
    global possible_perfect_pows
    global attempts, n_start, left, right

    attempts += 1

    print(f"Attempt #{attempts}")
    print(f"Number guesses: {number_guesses}")
    print(f"Rule guesses: {rule_guesses}")

    if n_start == -1:
        if len(number_guesses) and number_guesses[-1][2]:
            n_start = number_guesses[-1][0]
            print("n_start find: ", n_start)
            print("with attempts: ", attempts)
            print()
        else:
            if left == -1:
                left = 1
                return [guess_type["NUMBER"], 1]

            if right == -1:
                right = 100000
                return [guess_type["NUMBER"], 100000]

            last_guess, direction, _ = number_guesses[-1]

            if direction == number_direction_type["LESS"]:
                right = last_guess - 1

            elif direction == number_direction_type["GREATER"]:
                left = last_guess + 1

            return [guess_type["NUMBER"], (left + right) // 2]

    if n_start != 1:
        # if the rule is perfect pow, n_start should be 1, because 1 is
        # the only number that is a perfect pow of all k's and the
        # first pointer of binary search is 1, so if n_start is not 1,
        # we can rule out perfect pow rule
        CAN_BE_PERFECT_POW = False

    if CAN_BE_PERFECT_POW:
        print("Trying perfect pow rule...")

        for k in possible_perfect_pows:
            current_pow = possible_perfect_pows.pop()

            print("Trying perfect pow rule with : ", current_pow)

            if len(possible_perfect_pows) == 0:
                CAN_BE_PERFECT_POW = False

            return [guess_type["RULE"], [rule_type["POW"], current_pow, -1]]

    print("Perfect pow rule not found, trying other rules...")
    print()

    return ["TODO", 0]
