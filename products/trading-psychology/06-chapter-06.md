# Chapter 6: The Risk-Reward Framework — Only Taking Trades That Matter

## Thinking in R-Multiples

The R-multiple is the most powerful concept in risk management. It normalizes all trades to a common unit — your initial risk — so you can compare apples to apples regardless of position size, instrument, or account size.

```
R-Multiple = Profit or Loss / Initial Risk Amount
```

**Examples:**
- You risk EUR 100 and make EUR 250: that is a +2.5R trade
- You risk EUR 100 and lose EUR 100: that is a -1R trade
- You risk EUR 100 and make EUR 50: that is a +0.5R trade

**Why this matters:** When you think in R-multiples instead of euros, you separate the quality of the trade from the size of the position. A +3R trade is a +3R trade whether you risked EUR 50 or EUR 5,000. This creates clarity and prevents the psychological distortions that come with thinking about absolute dollar amounts.

## The Minimum R:R Threshold

Not every trade is worth taking. The risk-reward ratio tells you whether the potential reward justifies the risk.

```
Risk-Reward Ratio = (Target Price - Entry Price) / (Entry Price - Stop Loss Price)
```

### The 2:1 Rule

For most trading styles, the minimum acceptable R:R is 2:1. This means you need to make at least twice what you risk.

Here is why, using simple math:

**At 2:1 R:R, you only need to win 33.4% of the time to break even:**
```
Break-even win rate = 1 / (1 + R:R)
At 2:1: 1 / (1 + 2) = 0.334 = 33.4%
At 3:1: 1 / (1 + 3) = 0.25 = 25%
At 1:1: 1 / (1 + 1) = 0.50 = 50%
```

**At 1:1 R:R, you need to win more than 50% of your trades to be profitable.** That is difficult to achieve consistently after accounting for spreads, commissions, and slippage.

**At 2:1 R:R, you need to win more than 33.4%.** This is achievable with most reasonable strategies.

**At 3:1 R:R, you need to win more than 25%.** This gives you enormous room for error.

### The R:R Reality Check

| Your Win Rate | Minimum R:R Needed to Break Even | Recommended R:R |
|--------------|----------------------------------|-----------------|
| 70% | 0.43:1 | 1:1 or better |
| 60% | 0.67:1 | 1.5:1 or better |
| 50% | 1:1 | 2:1 or better |
| 40% | 1.5:1 | 2.5:1 or better |
| 30% | 2.33:1 | 3:1 or better |

The relationship between win rate and R:R is inverse. You can succeed with a low win rate if your winners are much larger than your losers. You can succeed with a low R:R if your win rate is very high. But you cannot succeed with both a low win rate AND a low R:R.

## Expected Value: The Real Measure

Expected value (EV) combines win rate and R:R into a single number that tells you whether a trade setup has a positive edge.

```
Expected Value (per trade) = (Win Rate x Average Win) - (Loss Rate x Average Loss)
```

Or in R-multiples:
```
EV (in R) = (Win Rate x Average R-Win) - (Loss Rate x Average R-Loss)
```

**Example:**
```
Win rate: 45%
Average winner: 2.5R
Loss rate: 55%
Average loser: 1R (if using stops correctly, this should always be ~1R)

EV = (0.45 x 2.5) - (0.55 x 1.0)
EV = 1.125 - 0.55
EV = +0.575R per trade
```

This means that on average, every trade in this system generates 0.575 times your initial risk in profit. Over 100 trades risking EUR 100 each, you would expect to make EUR 5,750.

**If EV is positive: the system has an edge. Take every valid setup.**
**If EV is negative: the system loses money over time. Fix it or stop trading it.**

### Calculating Your Personal EV

After 50+ trades with your system, calculate your actual EV:

```
Step 1: List all trade results in R-multiples
Example: +2.5R, -1R, +1.8R, -1R, +3.2R, -1R, -1R, +2.1R...

Step 2: Sum all R-multiples
Total R = +2.5 - 1 + 1.8 - 1 + 3.2 - 1 - 1 + 2.1...

Step 3: Divide by number of trades
EV per trade = Total R / Number of trades

Step 4: Assess
If EV > 0: You have an edge. Focus on execution consistency.
If EV < 0: Your system needs work. Adjust entries, stops, or targets.
If EV ≈ 0: You are breaking even. Small improvements in any area
will push you into profitability.
```

## Expectancy-Based Position Sizing

Once you know your system's expected value, you can optimize your position sizing for maximum growth.

```
Optimal risk per trade = EV / Average Winner (in R)
```

This is a simplified version of the Kelly Criterion. For most traders, this produces a number between 1-5% — but remember to use half or quarter of this value for safety.

## The Pre-Trade R:R Assessment

Before every trade, fill in this assessment:

```
TRADE R:R ASSESSMENT

Entry price: ___________
Stop loss price: ___________
Target price: ___________

Risk per share/unit: ___________ (Entry - Stop)
Reward per share/unit: ___________ (Target - Entry)
R:R ratio: ___________

MINIMUM R:R CHECK:
[ ] R:R >= 2:1 (or my minimum threshold: ___)

If R:R is below threshold: DO NOT TAKE THE TRADE.
No exceptions. Find a better entry or skip it.

EXPECTED VALUE CHECK:
Based on my system's win rate (___%), this R:R produces:
EV = (win rate x R:R) - (loss rate x 1.0) = ___R per trade

[ ] EV is positive? Trade is valid.
[ ] EV is negative? Do not take this trade.
```

## Multi-Target Strategies

Real trades often have multiple potential targets. Here is how to plan for that:

### The Tiered Target Approach

```
Entry: EUR 50.00
Stop: EUR 48.00 (Risk = EUR 2.00)

Target 1: EUR 54.00 (2R) — Take 50% of position
Target 2: EUR 58.00 (4R) — Take 25% of position
Target 3: Trail remaining 25% — capture maximum move

Blended R:R if all targets hit:
(0.50 x 2R) + (0.25 x 4R) + (0.25 x estimated 6R)
= 1.0 + 1.0 + 1.5
= 3.5R blended

Blended R:R if only Target 1 hit:
(0.50 x 2R) + (0.50 x -1R) [remaining stopped at breakeven]
= 1.0 - 0.5
= 0.5R
```

This approach ensures you capture some profit on most winning trades while leaving room for the occasional big winner.

## When to Skip a Trade

Even if a setup meets your technical criteria, skip it if:

1. **R:R is below your minimum.** A beautiful setup with a 1:1 R:R is not worth taking if your system requires 2:1.

2. **The stop cannot be placed at a logical level.** If the only logical stop is so far away that the R:R becomes unfavorable, skip it.

3. **You already have maximum correlated exposure.** If you are already long EUR/USD and long GBP/USD, another long dollar trade adds correlated risk.

4. **Your emotional state is compromised.** If you are trading for revenge, FOMO, or boredom, the expected value of any trade drops because your execution will be impaired.

5. **The market environment does not suit your strategy.** Trend-following strategies struggle in ranges. Mean-reversion strategies fail in trends. Know when your edge is present and when it is not.

The trades you skip are as important as the trades you take. Skipping a -EV trade is the same as making money — you are preserving capital that would otherwise be lost.

---

## Chapter 6 Key Takeaways

- Think in R-multiples, not dollars — normalize all trades to your initial risk
- Minimum 2:1 R:R for most strategies (adjustable based on win rate)
- Expected Value (EV) is the true measure of a system's edge
- Calculate your personal EV after 50+ trades — it is the most important number in your trading
- Use the pre-trade R:R assessment before every trade
- Multi-target strategies balance profit-taking with trend-riding
- The trades you skip are as important as the trades you take

---

*Chapter 7 brings everything together into a complete, written trading plan.*
