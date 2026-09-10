"""Small reproducible audit of right-edge periods for Rule 30.

u(t,k) = x(t,t-k), where x is Rule 30 from one central 1-cell.
"""

def right_edge_table(steps: int, offsets: int):
    u = [[0] * (offsets + 2) for _ in range(steps + 1)]
    for t in range(steps + 1):
        u[t][0] = 1
    for t in range(steps):
        for k in range(1, offsets + 1):
            u[t + 1][k] = u[t][k] ^ (u[t][k - 1] | u[t][k - 2])
    return u


def least_period(values, bound):
    for period in range(1, bound + 1):
        if all(values[t] == values[t + period]
               for t in range(len(values) - period)):
            return period
    return None


if __name__ == "__main__":
    limit = 8
    u = right_edge_table(2 ** (limit + 1), limit)
    for k in range(limit + 1):
        period = least_period([row[k] for row in u], 2 ** k)
        print(f"k={k}: period={period}, bound={2 ** k}")
    print("center:", "".join(str(u[n][n]) for n in range(min(9, limit + 1))))
