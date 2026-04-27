def perfect_pows(n):
    if n < 1:
        return []

    if n == 1:
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    res = []

    k = 2
    while (1 << k) <= n:  # same as 2^k <= n
        m = round(n ** (1 / k))

        if m > 1 and m**k == n:
            res.append(k)

        k += 1

    return res
