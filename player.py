# Nome #01 (quem entregou o código):    [NOME COMPLETO #01]
# RA #01 (quem entregou o código):      [RA #01]
# Nome #02:                             [NOME COMPLETO #02]
# RA #02:                               [RA #02]
guess_type = {"NUMBER": "NUMBER", "RULE": "RULE"}
rule_type = {"MOD": "mod", "POW": "pot", "INT": "int"}
number_direction_type = {"GREATER": "maior", "LESS": "menor"}

CAN_BE_PERFECT_POW = True
can_be_k_of_4096 = False
k_of_4096 = [1, 2, 3, 4, 6]
cannot_be_k_of_4096 = False
not_k_of_4096 = [1, 5, 7, 8, 9, 10]

CAN_BE_INTERVAL = True
CAN_BE_MOD = True

left_bs_left = -1
left_bs_right = -1
right_bs_left = -1
right_bs_right = -1
found_a = False
found_b = False
interval_a = -1
interval_b = -1

n_start = -1
left = -1
right = -1

# Variáveis do Galloping Search Inicial
GALLOP_FACTOR = 9
gallop_exp = 0
start_phase = "gallop"

global attempts
attempts = -1
last_processed_number_guesses = -1


def get_interval_bounds_from_history(number_guesses, n_start):
    left_bound = 1
    right_bound = 100_000

    closest_left_invalid = -1
    closest_right_invalid = 100_001

    for guess, direction, is_valid in number_guesses:
        if not is_valid:
            if guess < n_start:
                closest_left_invalid = max(closest_left_invalid, guess)
            elif guess > n_start:
                closest_right_invalid = min(closest_right_invalid, guess)

    if closest_left_invalid != -1:
        left_bound = closest_left_invalid + 1

    if closest_right_invalid != 100_001:
        right_bound = closest_right_invalid - 1

    return left_bound, right_bound


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
    global CAN_BE_INTERVAL, CAN_BE_MOD
    global left_bs_left, left_bs_right, right_bs_left, right_bs_right
    global found_a, found_b, interval_a, interval_b
    global attempts, n_start, left, right
    global last_processed_number_guesses
    global gallop_exp, start_phase

    attempts += 1

    # ==========================================
    # BUSCA INICIAL DO N_START (Galloping -> Binária)
    # ==========================================
    if n_start == -1:
        if len(number_guesses) and number_guesses[-1][2]:
            n_start = number_guesses[-1][0]
        else:
            if left == -1:
                left = 1
                right = 100_000
                return [guess_type["NUMBER"], 1]

            last_guess, direction, _ = number_guesses[-1]

            if start_phase == "gallop":
                if direction == number_direction_type["GREATER"]:
                    left = last_guess + 1
                    gallop_exp += 7
                    next_guess = 2**gallop_exp

                    if next_guess >= 100_000:
                        start_phase = "bs"
                        right = 100_000
                        return [guess_type["NUMBER"], (left + right) // 2]
                    return [guess_type["NUMBER"], next_guess]
                else:
                    # Overshoot! Passamos do número. Entra em Busca Binária na janela encontrada.
                    right = last_guess - 1
                    start_phase = "bs"
                    return [guess_type["NUMBER"], (left + right) // 2]
            else:
                # Fase de Busca Binária Padrão
                if direction == number_direction_type["LESS"]:
                    right = last_guess - 1
                elif direction == number_direction_type["GREATER"]:
                    left = last_guess + 1

                return [guess_type["NUMBER"], (left + right) // 2]

    # ==========================================

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

        if CAN_BE_INTERVAL and left_bs_left != -1:
            if not found_a:
                if is_valid:
                    left_bs_right = last_guess
                else:
                    if direction == number_direction_type["GREATER"]:
                        left_bs_left = last_guess + 1
                    else:
                        left_bs_right = last_guess - 1
            elif not found_b:
                if is_valid:
                    right_bs_left = last_guess
                else:
                    if direction == number_direction_type["LESS"]:
                        right_bs_right = last_guess - 1
                    else:
                        right_bs_left = last_guess + 1

        last_processed_number_guesses = len(number_guesses)

    if CAN_BE_MOD:
        candidates = list(range(2, 101))
        possible_ks = filter_k_candidates(candidates, n_start, number_guesses)

        for rg in rule_guesses:
            if rg[0] == rule_type["MOD"] and rg[1] in possible_ks:
                possible_ks.remove(rg[1])

        if len(possible_ks) == 1:
            return [
                guess_type["RULE"],
                [rule_type["MOD"], possible_ks[0], n_start % possible_ks[0]],
            ]
        elif len(possible_ks) == 0:
            CAN_BE_MOD = False

    if CAN_BE_INTERVAL:
        if left_bs_left == -1:
            base_left, base_right = get_interval_bounds_from_history(
                number_guesses, n_start
            )
            left_bs_left = max(base_left, max(1, n_start - 100))
            left_bs_right = n_start

        if not found_a:
            if left_bs_left >= left_bs_right:
                interval_a = left_bs_left
                found_a = True

                base_left, base_right = get_interval_bounds_from_history(
                    number_guesses, n_start
                )
                right_bs_left = n_start
                right_bs_right = min(base_right, min(100_000, interval_a + 100))
            else:
                return [guess_type["NUMBER"], (left_bs_left + left_bs_right) // 2]

        if found_a and not found_b:
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

    if CAN_BE_MOD and len(possible_ks) > 1:
        best_guess = -1
        best_diff = float("inf")
        target_split = len(possible_ks) / 2.0
        guesses_set = set(g[0] for g in number_guesses)

        for offset in range(1, 100_000):
            for sign in [1, -1]:
                x = n_start + sign * offset
                if 1 <= x <= 100_000 and x not in guesses_set:
                    valid_count = sum(1 for k in possible_ks if x % k == (n_start % k))
                    if 0 < valid_count < len(possible_ks):
                        diff = abs(valid_count - target_split)
                        if diff < best_diff:
                            best_diff = diff
                            best_guess = x

                        if best_diff == 0 or best_diff == 0.5:
                            break
            if best_diff == 0 or best_diff == 0.5:
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

    guesses_set = set(g[0] for g in number_guesses)
    for fallback_num in range(1, 100_001):
        if fallback_num not in guesses_set:
            return [guess_type["NUMBER"], fallback_num]

    return ["TODO", 0]
