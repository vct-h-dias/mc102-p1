### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
from utils.get_interval_bounds import get_interval_bounds_from_history

## types:
guess_type = {"NUMBER": "NUMBER", "RULE": "RULE"}
rule_type = {"MOD": "mod", "POW": "pot", "INT": "int"}
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

left_bs_left = -1
left_bs_right = -1
right_bs_left = -1
right_bs_right = -1
found_a = False
found_b = False
interval_a = -1
interval_b = -1

CAN_BE_MOD = True

## first n found:
n_start = -1
left = -1
right = -1

## DEBUG SECTION
global attempts
attempts = -1
last_processed_number_guesses = -1


def player(number_guesses, rule_guesses):
    """Função principal do jogador."""

    ## print("number_guesses:", number_guesses)
    ## print("rule_guesses:", rule_guesses)

    global guess_type, number_direction_type, rule_type
    global CAN_BE_PERFECT_POW, can_be_k_of_4096, cannot_be_k_of_4096
    global k_of_4096, not_k_of_4096
    global CAN_BE_INTERVAL, left_neighbor_is_valid, right_neighbor_is_valid
    global left_bs_left, left_bs_right, right_bs_left, right_bs_right
    global found_a, found_b, interval_a, interval_b
    global CAN_BE_MOD
    global attempts, n_start, left, right
    global last_processed_number_guesses

    attempts += 1

    print(f"Attempt #{attempts}")
    print(f"Number guesses: {number_guesses}")
    print(f"Rule guesses: {rule_guesses}")

    # ==========================================
    # BUSCA DO N_START
    # ==========================================
    if n_start == -1:
        if len(number_guesses) and number_guesses[-1][2]:
            n_start = number_guesses[-1][0]
            print("n_start found: ", n_start)
            print("with attempts: ", attempts)
            print()
        else:
            if left == -1:
                left = 1
                return [guess_type["NUMBER"], 1]

            if right == -1:
                right = 100_000
                return [guess_type["NUMBER"], 100_000]

            last_guess, direction, _ = number_guesses[-1]

            if direction == number_direction_type["LESS"]:
                right = last_guess - 1
            elif direction == number_direction_type["GREATER"]:
                left = last_guess + 1

            return [guess_type["NUMBER"], (left + right) // 2]

    # ==========================================
    # REGRA: PERFECT POW
    # ==========================================
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

    # ==========================================
    # 1. PROCESS LATEST GUESS & UPDATE STATE
    # ==========================================

    # RESOLVENDO O TODO: Se chutamos um intervalo [a, a] e erramos, só pode ser MOD.
    if len(rule_guesses) > 0 and rule_guesses[-1][0] == rule_type["INT"]:
        print("Interval rule failed! The rule must be MOD.")
        CAN_BE_INTERVAL = False

    # ONLY process if there is a NEW number guess!
    if len(number_guesses) > last_processed_number_guesses and n_start != -1:
        last_guess, direction, is_valid = number_guesses[-1]

        # Check Left Neighbor
        if last_guess == n_start - 1 and left_neighbor_is_valid == -1 and CAN_BE_MOD:
            left_neighbor_is_valid = is_valid
            if is_valid:
                print("Left neighbor is valid. Discarding MOD rule...")
                CAN_BE_MOD = False
            else:
                print(
                    "Left neighbor is not valid. Found start of interval (or it's MOD)."
                )
                found_a = True
                interval_a = n_start

        # Check Right Neighbor
        elif last_guess == n_start + 1 and right_neighbor_is_valid == -1 and CAN_BE_MOD:
            right_neighbor_is_valid = is_valid
            if is_valid:
                print("Right neighbor is valid. Discarding MOD rule...")
                CAN_BE_MOD = False
            else:
                print(
                    "Right neighbor is not valid. Found end of interval (or it's MOD)."
                )
                found_b = True
                interval_b = n_start

        # Binary Search Updates for 'a'
        elif not found_a and left_bs_left != -1:
            if is_valid:
                left_bs_right = last_guess
            else:
                left_bs_left = last_guess + 1

        # Binary Search Updates for 'b'
        elif found_a and not found_b and right_bs_left != -1:
            if is_valid:
                right_bs_left = last_guess
            else:
                right_bs_right = last_guess - 1

        # Mark this guess as processed
        last_processed_number_guesses = len(number_guesses)

    # ==========================================
    # 2. DECIDE THE NEXT GUESS
    # ==========================================
    if CAN_BE_INTERVAL and CAN_BE_MOD:
        print("Trying to define rule by neighborhood...")

        if left_neighbor_is_valid == -1:
            if n_start > 1:
                print("Trying left neighbor: ", n_start - 1)
                return [guess_type["NUMBER"], n_start - 1]
            else:
                left_neighbor_is_valid = None
                found_a = True
                interval_a = 1

        if right_neighbor_is_valid == -1:
            if n_start < 100_000:
                print("Trying right neighbor: ", n_start + 1)
                return [guess_type["NUMBER"], n_start + 1]
            else:
                right_neighbor_is_valid = None
                found_b = True
                interval_b = 100_000

    if CAN_BE_INTERVAL:
        print("The RULE is likely INTERVAL (doing Binary Search...)")

        base_left, base_right = get_interval_bounds_from_history(
            number_guesses, n_start
        )

        # Binary Search for Left Bound (a)
        if not found_a:
            if left_bs_left == -1:
                left_bs_left = max(base_left, max(1, n_start - 100))
                left_bs_right = n_start - 1

            if left_bs_left >= left_bs_right:
                interval_a = left_bs_left
                found_a = True
            else:
                mid = (left_bs_left + left_bs_right) // 2
                return [guess_type["NUMBER"], mid]

        # Binary Search for Right Bound (b)
        if found_a and not found_b:
            if right_bs_left == -1:
                # CRITICAL BUG FIX: Only start above n_start if we explicitly proved it's valid!
                if right_neighbor_is_valid == True:
                    right_bs_left = n_start + 1
                else:
                    right_bs_left = n_start

                right_bs_right = min(base_right, min(100_000, interval_a + 100))

            if right_bs_left >= right_bs_right:
                interval_b = right_bs_right
                found_b = True
            else:
                mid = (right_bs_left + right_bs_right + 1) // 2
                return [guess_type["NUMBER"], mid]

        # Both bounds found!
        if found_a and found_b:
            print(f"Found Interval: [{interval_a}, {interval_b}]")
            return [
                guess_type["RULE"],
                [rule_type["INT"], interval_a, interval_b],
            ]

    # ==========================================
    # REGRA: MOD (Fallback)
    # ==========================================
    if CAN_BE_MOD:
        print("The RULE is MOD")
        # You could add your MOD finding logic here in the future
        # For now, just firing a basic MOD guess:
        return [guess_type["RULE"], [rule_type["MOD"], 2, 0]]

    return ["TODO", 0]
