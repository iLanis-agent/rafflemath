#!/usr/bin/env python3
# Raffle Math oracle - mirrors engine.js.
import json, math

def _int(x, lo, msg):
    if not math.isfinite(x) or x % 1 != 0 or x < lo:
        raise ValueError(msg)

def _check(tickets, total, prizes):
    _int(total, 1, "tickets sold must be a whole number, 1 or more")
    if total > 10000:
        raise ValueError("keep tickets sold at 10000 or fewer")
    _int(prizes, 1, "prizes must be a whole number, 1 or more")
    if prizes > 100:
        raise ValueError("keep prizes at 100 or fewer")
    if prizes > total:
        raise ValueError("there cannot be more prizes than tickets sold")
    if tickets is not None:
        _int(tickets, 1, "your tickets must be a whole number, 1 or more")
        if tickets > total:
            raise ValueError("you cannot hold more tickets than were sold")

def _s(n, one, many):
    return one if n == 1 else many

def _no_win(k, n, p):
    if k + p > n:
        return 0
    r = 1
    for i in range(p):
        r = r * ((n - k - i) / (n - i))
    return r

def _tenths(t):
    return f"{t // 10}.{t % 10}%"

def _money(c):
    return f"${c // 100}.{c % 100:02d}"

def _fl(x):
    return math.floor(x)

def odds_truth(tickets, total, prizes):
    _check(tickets, total, prizes)
    win = _fl((1 - _no_win(tickets, total, prizes)) * 1000 + 0.5)
    return (f"{tickets} of {total} tickets with {prizes} {_s(prizes, 'prize', 'prizes')}: "
            f"a {_tenths(win)} chance of at least one win, {_tenths(1000 - win)} of none.")

def value_truth(price_d, tickets, total, prizes, prize_d):
    _check(tickets, total, prizes)
    if not math.isfinite(price_d) or price_d < 0:
        raise ValueError("ticket price must be 0 or more")
    if not math.isfinite(prize_d) or prize_d < 0:
        raise ValueError("prize value must be 0 or more")
    price = _fl(price_d * 100 + 0.5)
    prize = _fl(prize_d * 100 + 0.5)
    cost = tickets * price
    ev = _fl((prizes * prize * tickets) / total + 0.5)
    each = _fl((prizes * prize) / total + 0.5)
    diff = ev - cost
    net = f"ahead by {_money(diff)}" if diff > 0 else f"behind by {_money(-diff)}" if diff < 0 else "even"
    return (f"{tickets} {_s(tickets, 'ticket', 'tickets')} at {_money(price)} cost {_money(cost)}. "
            f"Average prize value is {_money(ev)} ({prizes} {_s(prizes, 'prize', 'prizes')} of {_money(prize)} "
            f"over {total} tickets, {_money(each)} per ticket). On average: {net}.")

def _num(x):
    return str(int(x)) if x == int(x) else repr(x)

def target_truth(total, prizes, pct):
    _check(None, total, prizes)
    if not math.isfinite(pct) or pct <= 0 or pct > 100:
        raise ValueError("target must be over 0 and at most 100 percent")
    goal = pct / 100
    for k in range(1, total + 1):
        w = 1 - _no_win(k, total, prizes)
        if w >= goal:
            return (f"To reach a {_num(pct)}% chance with {prizes} {_s(prizes, 'prize', 'prizes')} among {total} "
                    f"tickets, you would hold {k} {_s(k, 'ticket', 'tickets')} ({_tenths(_fl(w * 1000 + 0.5))}).")
    raise ValueError("no ticket count reaches that target")

FNS = {"oddsTruth": odds_truth, "valueTruth": value_truth, "targetTruth": target_truth}

CASES = [
    ("oddsTruth", [5, 200, 3]),
    ("oddsTruth", [1, 200, 1]),
    ("oddsTruth", [200, 200, 3]),
    ("oddsTruth", [198, 200, 3]),
    ("oddsTruth", [50, 100, 1]),
    ("oddsTruth", [0, 200, 3]),
    ("oddsTruth", [201, 200, 3]),
    ("oddsTruth", [5, 200, 0]),
    ("oddsTruth", [5, 2, 3]),
    ("oddsTruth", [2.5, 200, 3]),
    ("valueTruth", [2, 5, 200, 3, 50]),
    ("valueTruth", [0.75, 1, 200, 3, 50]),
    ("valueTruth", [0, 4, 100, 2, 25]),
    ("valueTruth", [10, 10, 100, 1, 500]),
    ("valueTruth", [-1, 5, 200, 3, 50]),
    ("targetTruth", [200, 3, 50]),
    ("targetTruth", [100, 1, 1]),
    ("targetTruth", [100, 1, 100]),
    ("targetTruth", [200, 3, 0]),
    ("targetTruth", [200, 3, 12.5]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
