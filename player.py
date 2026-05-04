# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
from utils.get_interval_bounds import get_interval_bounds_from_history

guess_type = {"NUMBER": "NUMBER", "RULE": "RULE"}
rule_type = {"MOD": "mod", "POW": "pot", "INT": "int"}
number_direction_type = {"GREATER": "maior", "LESS": "menor"}

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

n_start = -1
left = -1
right = -1

global attempts
attempts = -1
last_processed_number_guesses = -1


def filter_k_candidates(candidates, n_start, number_guesses):
    filtered = []

    for k in candidates:
        r = n_start % k
        is_possible = True

        for guess, direction, is_valid_guess in number_guesses:
            if (guess % k == r) != is_valid_guess:
                is_possible = False
                break

            if not is_valid_guess:
                m_base = (guess - r) // k
                valid_neighbors = []

                for delta in [0, 1]:
                    v = k * (m_base + delta) + r
                    if 1 <= v <= 100_000:
                        valid_neighbors.append(v)

                if not valid_neighbors:
                    is_possible = False
                    break

                closest = min(valid_neighbors, key=lambda x: abs(x - guess))

                if closest < guess:
                    expected_dir = number_direction_type["LESS"]
                elif closest > guess:
                    expected_dir = number_direction_type["GREATER"]
                else:
                    is_possible = False
                    break

                if expected_dir != direction:
                    is_possible = False
                    break

        if is_possible:
            filtered.append(k)

    return filtered


def player(number_guesses, rule_guesses):
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

    if n_start == -1:
        if len(number_guesses) and number_guesses[-1][2]:
            n_start = number_guesses[-1][0]
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

    if n_start != 1:
        CAN_BE_PERFECT_POW = False

    if CAN_BE_PERFECT_POW:
        if number_guesses[-1][0] == 4096 and number_guesses[-1][2]:
            can_be_k_of_4096 = True
        elif number_guesses[-1][0] == 4096 and not number_guesses[-1][2]:
            cannot_be_k_of_4096 = True
        else:
            return [guess_type["NUMBER"], 4096]

        if can_be_k_of_4096:
            current_pow = k_of_4096.pop()
            if len(k_of_4096) == 0:
                CAN_BE_PERFECT_POW = False
            return [guess_type["RULE"], [rule_type["POW"], current_pow, -1]]

        elif cannot_be_k_of_4096:
            current_pow = not_k_of_4096.pop()
            if len(not_k_of_4096) == 0:
                CAN_BE_PERFECT_POW = False
            return [guess_type["RULE"], [rule_type["POW"], current_pow, -1]]

    if len(rule_guesses) > 0 and rule_guesses[-1][0] == rule_type["INT"]:
        CAN_BE_INTERVAL = False

    if len(number_guesses) > last_processed_number_guesses and n_start != -1:
        last_guess, direction, is_valid = number_guesses[-1]

        if last_guess == n_start - 1 and left_neighbor_is_valid == -1 and CAN_BE_MOD:
            left_neighbor_is_valid = is_valid
            if is_valid:
                CAN_BE_MOD = False
            else:
                found_a = True
                interval_a = n_start

        elif last_guess == n_start + 1 and right_neighbor_is_valid == -1 and CAN_BE_MOD:
            right_neighbor_is_valid = is_valid
            if is_valid:
                CAN_BE_MOD = False
            else:
                found_b = True
                interval_b = n_start

        elif not found_a and left_bs_left != -1:
            if is_valid:
                left_bs_right = last_guess
            else:
                left_bs_left = last_guess + 1

        elif found_a and not found_b and right_bs_left != -1:
            if is_valid:
                right_bs_left = last_guess
            else:
                right_bs_right = last_guess - 1

        last_processed_number_guesses = len(number_guesses)

    if CAN_BE_INTERVAL and CAN_BE_MOD:
        if left_neighbor_is_valid == -1:
            if n_start > 1:
                return [guess_type["NUMBER"], n_start - 1]
            else:
                left_neighbor_is_valid = None
                found_a = True
                interval_a = 1

        if right_neighbor_is_valid == -1:
            if n_start < 100_000:
                return [guess_type["NUMBER"], n_start + 1]
            else:
                right_neighbor_is_valid = None
                found_b = True
                interval_b = 100_000

    if CAN_BE_INTERVAL:
        base_left, base_right = get_interval_bounds_from_history(
            number_guesses, n_start
        )

        if not found_a:
            if left_bs_left == -1:
                left_bs_left = max(base_left, max(1, n_start - 100))
                left_bs_right = n_start - 1
            if left_bs_left >= left_bs_right:
                interval_a = left_bs_left
                found_a = True
            else:
                return [guess_type["NUMBER"], (left_bs_left + left_bs_right) // 2]

        if found_a and not found_b:
            if right_bs_left == -1:
                right_bs_left = (
                    n_start + 1 if right_neighbor_is_valid == True else n_start
                )
                right_bs_right = min(base_right, min(100_000, interval_a + 100))
            if right_bs_left >= right_bs_right:
                interval_b = right_bs_right
                found_b = True
            else:
                return [guess_type["NUMBER"], (right_bs_left + right_bs_right + 1) // 2]

        if found_a and found_b:
            if interval_a == interval_b and CAN_BE_MOD:
                pass
            else:
                return [guess_type["RULE"], [rule_type["INT"], interval_a, interval_b]]

    if CAN_BE_MOD:
        candidates = list(range(2, 101))
        possible_ks = filter_k_candidates(candidates, n_start, number_guesses)

        for rg in rule_guesses:
            if rg[0] == rule_type["MOD"] and rg[1] in possible_ks:
                possible_ks.remove(rg[1])

        if len(possible_ks) == 1:
            k = possible_ks[0]
            return [guess_type["RULE"], [rule_type["MOD"], k, n_start % k]]

        elif len(possible_ks) > 1:
            best_guess = -1
            guesses_set = set(g[0] for g in number_guesses)

            for offset in range(1, 100_000):
                for sign in [1, -1]:
                    x = n_start + sign * offset
                    if 1 <= x <= 100_000 and x not in guesses_set:
                        valid_count = sum(
                            1 for k in possible_ks if x % k == (n_start % k)
                        )
                        if 0 < valid_count < len(possible_ks):
                            best_guess = x
                            break
                if best_guess != -1:
                    break

            if best_guess == -1:
                for offset in range(1, 100_000):
                    for sign in [1, -1]:
                        x = n_start + sign * offset
                        if 1 <= x <= 100_000 and x not in guesses_set:
                            best_guess = x
                            break
                    if best_guess != -1:
                        break

            return [guess_type["NUMBER"], best_guess]

        else:
            CAN_BE_MOD = False
            if found_a and found_b:
                return [guess_type["RULE"], [rule_type["INT"], interval_a, interval_b]]

    guesses_set = set(g[0] for g in number_guesses)
    for fallback_num in range(1, 100_001):
        if fallback_num not in guesses_set:
            return [guess_type["NUMBER"], fallback_num]

    return ["TODO", 0]
