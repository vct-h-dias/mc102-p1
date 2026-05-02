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
