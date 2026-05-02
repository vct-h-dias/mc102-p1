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
can_be_k_of_4096 = False
k_of_4096 = [1, 2, 3, 4, 6]
cannot_be_k_of_4096 = False
not_k_of_4096 = [1, 5, 7, 8, 9, 10]

CAN_BE_INTERVAL = True
left_neighbor_is_valid = -1
right_neighbor_is_valid = -1

CAN_BE_MOD = True

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
    global CAN_BE_PERFECT_POW
    global can_be_k_of_4096, cannot_be_k_of_4096
    global k_of_4096, not_k_of_4096

    global CAN_BE_INTERVAL
    global left_neighbor_is_valid, right_neighbor_is_valid

    global CAN_BE_MOD

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
        # if the rule is POW, n_start should be 1, because 1 is
        # the only number that is a perfect pow of all k's and the
        # first pointer of binary search is 1, so if n_start is not 1,
        # we can rule out POW rule
        CAN_BE_PERFECT_POW = False

    if CAN_BE_PERFECT_POW:
        print("Trying POW rule...")

        if number_guesses[-1][0] == 4096 and number_guesses[-1][2]:
            can_be_k_of_4096 = True
        elif number_guesses[-1][0] == 4096 and not number_guesses[-1][2]:
            cannot_be_k_of_4096 = True
        else:
            print("Trying 4096 for POW rule...")
            return [guess_type["NUMBER"], 4096]

        if can_be_k_of_4096:
            current_pow = k_of_4096.pop()

            print("Trying perfect pow rule with : ", current_pow)

            if len(k_of_4096) == 0:
                CAN_BE_PERFECT_POW = False

            return [guess_type["RULE"], [rule_type["POW"], current_pow, -1]]
        elif cannot_be_k_of_4096:
            current_pow = not_k_of_4096.pop()

            print("Trying perfect pow rule with : ", current_pow)

            if len(not_k_of_4096) == 0:
                CAN_BE_PERFECT_POW = False

            return [guess_type["RULE"], [rule_type["POW"], current_pow, -1]]

    print("Perfect pow rule not found")

    if CAN_BE_INTERVAL and CAN_BE_MOD:
        print("Trying to define rule by neighborhood...")

        if number_guesses[-1][0] == n_start - 1 and number_guesses[-1][2]:
            print("Left neighbor is valid. Discarding MOD rule...")
            CAN_BE_MOD = False
            left_neighbor_is_valid = True
        elif number_guesses[-1][0] == n_start - 1 and not number_guesses[-1][2]:
            print("Left neighbor is not valid. Discarding INTERVAL rule...")
            CAN_BE_INTERVAL = False
            left_neighbor_is_valid = False

        if number_guesses[-1][0] == n_start + 1 and number_guesses[-1][2]:
            print("Right neighbor is valid. Discarding MOD rule...")
            CAN_BE_MOD = False
            right_neighbor_is_valid = True
        elif number_guesses[-1][0] == n_start + 1 and not number_guesses[-1][2]:
            print("Right neighbor is not valid. Discarding INTERVAL rule...")
            CAN_BE_INTERVAL = False
            right_neighbor_is_valid = False

        if CAN_BE_INTERVAL and CAN_BE_MOD:
            if left_neighbor_is_valid == -1:
                if n_start > 1:
                    print("Trying left neighbor: ", n_start - 1)
                    return [guess_type["NUMBER"], n_start - 1]
                else:
                    left_neighbor_is_valid = None

            if right_neighbor_is_valid == -1:
                if n_start < 100000:
                    print("Trying right neighbor: ", n_start + 1)
                    return [guess_type["NUMBER"], n_start + 1]
                else:
                    right_neighbor_is_valid = None

    if CAN_BE_INTERVAL:
        print("The RULE is INTERVAL")

    if CAN_BE_MOD:
        print("The RULE is MOD")

    ## TODO: edge case with RULE as INT where a == b (interval with a single number)

    return ["TODO", 0]
