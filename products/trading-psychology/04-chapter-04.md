# Chapter 4: Position Sizing — The Only Formula You Need

## The Most Important Calculation in Trading

If you learn nothing else from this book, learn this: position sizing determines whether you survive long enough for your edge to play out. A great strategy with bad position sizing will blow up. A mediocre strategy with good position sizing will survive — and survival is the prerequisite for success.

Position sizing answers one question: "How large should my trade be?"

The answer is never "as much as possible" and never a fixed dollar amount. The answer is always a function of your account size, your predefined risk tolerance, and the distance to your stop loss.

## The Fixed Percentage Risk Model

This is the position sizing model used by the majority of professional traders. It is simple, effective, and self-adjusting.

### The Core Formula

```
Position Size = (Account Size x Risk Percentage) / (Entry Price - Stop Loss Price)
```

For short trades:
```
Position Size = (Account Size x Risk Percentage) / (Stop Loss Price - Entry Price)
```

**Variables:**
- **Account Size:** Your total trading capital (not your net worth — only capital dedicated to trading)
- **Risk Percentage:** The maximum percentage of your account you are willing to lose on a single trade. Standard: 1-2%.
- **Entry Price:** The price at which you enter the trade
- **Stop Loss Price:** The price at which your stop loss is placed

### Example 1: Forex Trade

```
Account size: EUR 10,000
Risk per trade: 1% = EUR 100
Pair: EUR/USD
Entry: 1.0850
Stop loss: 1.0800
Distance to stop: 50 pips = 0.0050

Position size = EUR 100 / 0.0050 = 20,000 units (0.2 standard lots)

If EUR/USD moves against you by 50 pips, you lose EUR 100 = 1% of account.
```

### Example 2: Stock Trade

```
Account size: EUR 25,000
Risk per trade: 1.5% = EUR 375
Stock: ASML
Entry: EUR 750.00
Stop loss: EUR 735.00
Distance to stop: EUR 15.00

Position size = EUR 375 / EUR 15.00 = 25 shares
Position value = 25 x EUR 750 = EUR 18,750

If ASML drops to EUR 735, you lose EUR 375 = 1.5% of account.
```

### Example 3: Crypto Trade

```
Account size: EUR 5,000
Risk per trade: 1% = EUR 50
Asset: Bitcoin (BTC)
Entry: EUR 62,000
Stop loss: EUR 60,500
Distance to stop: EUR 1,500

Position size = EUR 50 / EUR 1,500 = 0.0333 BTC
Position value = 0.0333 x EUR 62,000 = EUR 2,066

If BTC drops to EUR 60,500, you lose EUR 50 = 1% of account.
```

## Why 1-2% Risk Per Trade?

The math of ruin explains why.

### The Ruin Table

This table shows how many consecutive losses it takes to lose a specific percentage of your account at different risk levels:

| Risk per trade | Losses to lose 10% | Losses to lose 25% | Losses to lose 50% |
|---------------|--------------------|--------------------|---------------------|
| 1% | 10 | 29 | 69 |
| 2% | 5 | 14 | 34 |
| 3% | 4 | 10 | 23 |
| 5% | 2 | 6 | 13 |
| 10% | 1 | 3 | 7 |

At 1% risk per trade, you need 69 consecutive losses to lose half your account. That is virtually impossible with any reasonable strategy.

At 5% risk per trade, just 13 consecutive losses (which absolutely happens during drawdowns) wipes out half your account. And recovering from a 50% loss requires a 100% gain — which is extremely difficult.

### The Recovery Problem

This is the mathematical reality that makes excessive risk fatal:

| Loss | Gain needed to recover |
|------|----------------------|
| 5% | 5.3% |
| 10% | 11.1% |
| 20% | 25.0% |
| 30% | 42.9% |
| 40% | 66.7% |
| 50% | 100.0% |
| 75% | 300.0% |
| 90% | 900.0% |

A 10% loss is recoverable. A 50% loss is a crisis. A 75% loss is essentially account death. The relationship is non-linear — the deeper you go, the exponentially harder it is to come back.

This is why position sizing is not about maximizing returns. It is about ensuring that no single trade or string of losses can put you in an unrecoverable position.

### Recommended Risk Levels

| Trader Type | Risk Per Trade | Rationale |
|------------|---------------|-----------|
| Beginner (first year) | 0.5% | Learning phase — prioritize survival |
| Intermediate | 1% | Standard professional risk level |
| Advanced/Full-time | 1-2% | Slightly more aggressive with proven edge |
| Aggressive (proven track record) | 2-3% | Only with demonstrated consistent profitability |
| Never | >5% | This is gambling, not trading |

## Advanced Position Sizing: The Kelly Criterion

The Kelly Criterion is a mathematical formula that determines the optimal position size to maximize long-term account growth. It is used by professional gamblers and some quantitative traders.

### The Formula

```
Kelly % = W - (1-W)/R

Where:
W = Win rate (decimal)
R = Average win / Average loss (reward-to-risk ratio)
```

### Example

```
Your strategy has:
Win rate: 55% (W = 0.55)
Average winner: EUR 200
Average loser: EUR 100
R = 200/100 = 2.0

Kelly % = 0.55 - (1 - 0.55) / 2.0
Kelly % = 0.55 - 0.225
Kelly % = 0.325 = 32.5%
```

### Why You Should Use Half-Kelly or Less

The full Kelly percentage is theoretically optimal for long-term growth, but it produces enormous drawdowns. In practice, most professionals use "Half-Kelly" or "Quarter-Kelly":

- **Full Kelly (32.5%):** Maximum growth rate, but expect 50%+ drawdowns. Only for the mathematically fearless.
- **Half-Kelly (16.25%):** 75% of the growth with dramatically less risk.
- **Quarter-Kelly (8.1%):** Very conservative, very smooth equity curve.
- **Fixed 1-2%:** Practical equivalent of quarter-Kelly for most retail traders.

**Our recommendation:** Unless you have precise, statistically significant metrics for your win rate and reward-to-risk ratio (requiring 100+ trades minimum), stick with fixed 1-2% risk. Kelly requires accurate inputs, and most traders overestimate their edge.

## Position Sizing for Different Account Sizes

### Small Accounts (Under EUR 5,000)

The challenge with small accounts is that 1% risk is very small (EUR 50 on a EUR 5,000 account), which limits your instrument choices and can result in position sizes below the minimum lot size.

**Solutions:**
- Trade instruments with tight spreads and small minimum sizes (micro lots in forex, fractional shares in stocks)
- Accept slightly higher risk per trade (up to 2%) in the early stages, with the understanding that you are trading smaller absolute amounts
- Focus on building skills, not account size. A 20% return on EUR 5,000 is EUR 1,000 — not life-changing, but the skills transfer to larger capital later

### Medium Accounts (EUR 5,000 - EUR 50,000)

This is the sweet spot for the fixed percentage model. 1% of EUR 25,000 is EUR 250 per trade — enough to be meaningful but not devastating.

**Key consideration:** At this size, you can trade most instruments comfortably. Your focus should be on consistency and building your track record.

### Large Accounts (EUR 50,000+)

Larger accounts introduce liquidity considerations. A 1% risk of EUR 100,000 is EUR 1,000 per trade. The position sizes required to risk EUR 1,000 on tight stops can be large enough to affect less liquid instruments.

**Solutions:**
- Reduce risk percentage to 0.5% for less liquid instruments
- Be mindful of position size relative to average volume
- Consider splitting entries across multiple price levels

## Position Sizing Mistakes That Destroy Accounts

### Mistake 1: Martingale (Doubling Down)

"I lost, so I will double my next position to make it back faster."

This is the fastest path to account death. A losing streak of 5 trades with doubling produces a 31x multiplier on your original risk. If you started with EUR 100 risk, your fifth trade risks EUR 3,200.

**Never increase position size after a loss. Period.**

### Mistake 2: The "Feel" Method

"I feel really good about this trade, so I will go bigger."

Your feelings are not a risk management tool. Position size is a mathematical output, not an emotional decision. Use the formula. Every time.

### Mistake 3: Risking a Fixed Dollar Amount Regardless of Stop Distance

"I always risk EUR 200 per trade."

This seems disciplined but is actually dangerous. If your stop is 10 pips away, EUR 200 risk produces a reasonable position. If your stop is 100 pips away, EUR 200 risk produces a position 10x smaller. You end up with wildly inconsistent R-values and some trades that are significantly larger (in dollar terms) than others.

Use the formula. Let the stop distance determine your position size, with the risk percentage as the constant.

### Mistake 4: Not Accounting for Correlation

If you have three open positions in EUR/USD, GBP/USD, and AUD/USD, you essentially have three correlated long-dollar positions. Your real risk is not 1% x 3 = 3%. It could be closer to the full account being exposed to a single directional move in the dollar.

**Solution:** If you take multiple positions in correlated instruments, reduce each position's risk so that the total correlated risk stays within your tolerance. A useful rule: no more than 3-5% total risk across correlated positions.

---

## Chapter 4 Key Takeaways

- Position size = (Account x Risk %) / Distance to Stop Loss
- Risk 1-2% of your account per trade — never more
- The math of ruin explains why: a 50% loss requires a 100% return to recover
- The Kelly Criterion provides theoretical optimal sizing, but use half-Kelly or less in practice
- Position sizing is mathematical, not emotional — use the formula every time
- Never martingale, never size on feel, always account for correlated positions
- Your position sizing discipline is worth more than any entry signal

---

*Chapter 5 covers stop-loss strategies — where to place them, when to move them, and how to protect capital without getting stopped out on noise.*
