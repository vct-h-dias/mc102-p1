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

## jump and hone MOD variables:
jump_bs_left = -1
jump_bs_right = -1
found_v = False
valid_v = -1
possible_ks = []

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
    global jump_bs_left, jump_bs_right, found_v, valid_v, possible_ks

    attempts += 1

    print(f"Attempt #{attempts}")
    print(f"Number guesses: {number_guesses}")
    print(f"Rule guesses: {rule_guesses}")

    # ==========================================
    # SEARCH FROM n_start
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
    # RULE: PERFECT POW
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

        # Jump Binary Search Updates for V (MOD rule)
        elif CAN_BE_MOD and not found_v and jump_bs_left != -1:
            if is_valid:
                valid_v = last_guess
                found_v = True
            else:
                if direction == number_direction_type["LESS"]:
                    jump_bs_right = last_guess - 1
                else:
                    jump_bs_left = last_guess + 1

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
    # RULE: MOD
    # ==========================================
    if CAN_BE_MOD:
        print("The RULE is MOD (Doing Jump & Hone...)")

        # 1. Find a second valid number (V) quickly
        if not found_v:
            if jump_bs_left == -1:
                # Jump forward to a random safe target to avoid tiny gaps
                target = n_start + 3141
                if target > 100_000:
                    target = n_start - 3141

                # We only need to search a window of 100 numbers!
                jump_bs_left = max(1, target - 50)
                jump_bs_right = min(100_000, target + 50)

            if jump_bs_left >= jump_bs_right:
                valid_v = jump_bs_left
                found_v = True
            else:
                mid = (jump_bs_left + jump_bs_right) // 2
                return [guess_type["NUMBER"], mid]

        # 2. Extract Divisors and Filter using History
        # 2. Extract Divisors and Filter using History
        if found_v:
            if len(possible_ks) == 0:
                diff = abs(valid_v - n_start)

                # Get all divisors <= 100
                candidates = [k for k in range(2, 101) if diff % k == 0]

                # Filter candidates using your entire game history
                for k in candidates:
                    r = n_start % k
                    is_possible = True

                    for guess, direction, is_val in number_guesses:
                        # Check 1: Does the validity match?
                        if (guess % k == r) != is_val:
                            is_possible = False
                            break

                        # Check 2: Calculate EXACT closest valid number strictly within bounds [1, 100000]
                        if not is_val:
                            m_base = (guess - r) // k
                            valid_neighbors = []

                            # Generate local numbers in the sequence and filter out-of-bounds
                            for delta in [-2, -1, 0, 1, 2]:
                                v = k * (m_base + delta) + r
                                if 1 <= v <= 100_000:
                                    valid_neighbors.append(v)

                            if not valid_neighbors:
                                continue

                            min_dist = float("inf")
                            best_v = None

                            for v in valid_neighbors:
                                dist = abs(v - guess)
                                if dist < min_dist:
                                    min_dist = dist
                                    best_v = v
                                elif dist == min_dist:
                                    # Tie-breaker: Project spec says middle point returns 'menor' (which means we select the smaller number)
                                    best_v = min(best_v, v)

                            if best_v < guess:
                                expected_dir = number_direction_type["LESS"]
                            elif best_v > guess:
                                expected_dir = number_direction_type["GREATER"]
                            else:
                                continue  # Should not hit this if not is_val

                            if expected_dir != direction:
                                is_possible = False
                                break

                    if is_possible:
                        possible_ks.append(k)

            # 3. Guess the mathematically proven rule!
            if len(possible_ks) == 1:
                # If only one candidate survives the filter, we are mathematically certain!
                guess_k = possible_ks[0]
                print(f"Mathematical certainty! Guessing MOD {guess_k}")
                return [
                    guess_type["RULE"],
                    [rule_type["MOD"], guess_k, n_start % guess_k],
                ]

            elif len(possible_ks) > 1:
                # If multiple candidates survive, we MUST guess a NUMBER to break the tie!
                mid_point = (n_start + valid_v) // 2

                guesses_set = set(g[0] for g in number_guesses)
                while mid_point in guesses_set:
                    mid_point += 1

                print(
                    f"Multiple candidates {possible_ks}. Guessing number {mid_point} to break tie."
                )
                possible_ks = []  # Clear so it recalculates with new data
                return [guess_type["NUMBER"], mid_point]

            else:
                # Ultimate Fallback: The filter eliminated EVERYTHING.
                fallback_guess = valid_v + 1
                guesses_set = set(g[0] for g in number_guesses)
                while fallback_guess in guesses_set or fallback_guess > 100_000:
                    fallback_guess += 1
                    if fallback_guess > 100_000:
                        fallback_guess = 1

                print(
                    f"All candidates eliminated! Forcing new data with number {fallback_guess}"
                )
                found_v = False  # Force it to find a new V next time
                jump_bs_left = -1
                possible_ks = []  # Clear the list
                return [guess_type["NUMBER"], fallback_guess]

            # 3. Guess the mathematically proven rule!
            if len(possible_ks) == 1:
                # If only one candidate survives the filter, we are mathematically certain!
                guess_k = possible_ks[0]
                print(f"Mathematical certainty! Guessing MOD {guess_k}")
                # We do NOT pop it. If we are wrong (impossible), we want to stay in the loop to debug.
                return [
                    guess_type["RULE"],
                    [rule_type["MOD"], guess_k, n_start % guess_k],
                ]

            elif len(possible_ks) > 1:
                # If multiple candidates survive, we MUST guess a NUMBER to break the tie!
                # Do NOT guess a rule, or we will infinite loop.
                # Let's guess a number exactly in the middle of our two valid hits.
                mid_point = (n_start + valid_v) // 2

                # Ensure we don't guess a number we already guessed!
                guesses_set = set(g[0] for g in number_guesses)
                while mid_point in guesses_set:
                    mid_point += 1

                print(
                    f"Multiple candidates {possible_ks}. Guessing number {mid_point} to break tie."
                )

                # Clear the possible_ks list so it recalculates with the new number data next turn
                possible_ks = []
                return [guess_type["NUMBER"], mid_point]

            else:
                # Ultimate Fallback: The filter eliminated EVERYTHING.
                # This usually means valid_v wasn't actually part of the same MOD sequence
                # (edge cases). Let's guess a random number to get more data and prevent the loop.
                fallback_guess = valid_v + 1
                guesses_set = set(g[0] for g in number_guesses)
                while fallback_guess in guesses_set:
                    fallback_guess += 1

                print(
                    f"All candidates eliminated! Forcing new data with number {fallback_guess}"
                )
                found_v = False  # Force it to find a new V next time
                jump_bs_left = -1
                return [guess_type["NUMBER"], fallback_guess]

    return ["TODO", 0]
