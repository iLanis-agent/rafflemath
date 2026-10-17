# Raffle Math

Draw odds and ticket cost arithmetic. The jar looks full of chances; the arithmetic says how many are yours.

## What it computes

- **The odds truth** - your tickets, tickets sold and prize count to the chance of at least one win: 5 of 200 tickets with 3 prizes is 7.4%. Each ticket wins at most one prize.
- **The value truth** - your own ticket price and prize value against the average payout: 5 tickets at $2.00 cost $10.00, average prize value $3.75.
- **The target truth** - the fewest tickets that reach a chance you name: 42 tickets reach 50% with 3 prizes among 200.

## Boundary

Arithmetic only. Raffle Math turns the numbers you type into odds and averages. It never says whether to buy tickets and cannot predict any single draw. Prices, prize values and targets are entered by you.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (20 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/rafflemath/
Repo: https://github.com/iLanis-agent/rafflemath
