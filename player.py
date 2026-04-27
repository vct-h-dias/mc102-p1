### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]

## types:
guess_type = {"NUMBER": "NUMBER", "RULE": "RULE"}
number_direction_type = {"GREATER": "maior", "LESS": "menor"}

## rules control set:
CAN_BE_PERFECT_POW = True
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
    global attempts, n_start, left, right
    global CAN_BE_PERFECT_POW, CAN_BE_MOD, CAN_BE_INTERVAL
    global guess_type, number_direction_type

    attempts += 1

    print(f"Attempt #{attempts}")
    print(f"Number guesses: {number_guesses}")
    print(f"Rule guesses: {rule_guesses}")
    print()

    if n_start == -1:
        if len(number_guesses) and number_guesses[-1][2]:
            n_start = number_guesses[-1][0]
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

    print("n_start find: ", n_start)
    print("with attempts: ", attempts)

    return ["TODO", 0]
