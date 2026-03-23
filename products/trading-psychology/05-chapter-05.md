# Chapter 5: Stop-Loss Strategies — Protecting Capital Without Getting Stopped Out

## The Purpose of a Stop Loss

A stop loss serves exactly one purpose: to define the maximum amount you are willing to lose on a trade before the market proves your thesis wrong.

It is not a prediction of where price will go. It is not a target for market makers to hunt. It is your pre-commitment to accept that you were wrong and exit with a controlled, predefined loss.

Traders who do not use stops, or who move stops further away to "give the trade more room," are not managing risk — they are avoiding the psychological discomfort of being wrong. And that avoidance eventually costs them their account.

## The Three Stop-Loss Methods

### Method 1: Structure-Based Stops (Recommended)

Place your stop at a price level where your trade thesis is invalidated by market structure.

**For long trades:**
- Below the most recent significant swing low
- Below a key support level
- Below the low of a setup candle or pattern

**For short trades:**
- Above the most recent significant swing high
- Above a key resistance level
- Above the high of a setup candle or pattern

**Why this works:** Structure-based stops are placed at levels where your analysis is objectively wrong. If you are long because price bounced off support and the stop is below support, then if support breaks, your reason for being in the trade no longer exists. The stop is at the right place logically.

**Example: Long trade at support**
```
Support level: EUR 100.00
Entry: EUR 101.50 (after confirmation bounce)
Stop: EUR 99.50 (below support, with buffer)
Buffer: EUR 0.50 below the exact level to avoid being stopped
on an exact touch of support

Why EUR 99.50 and not EUR 100.00?
Price often touches exact support levels before bouncing.
Placing stops at the exact level guarantees you get stopped
on noise. Adding a buffer (0.25-0.5% below the level)
filters out normal price noise while still exiting if the
level genuinely breaks.
```

### Method 2: ATR-Based Stops

The Average True Range (ATR) measures how much an instrument typically moves in a given period. ATR-based stops adapt to the current volatility of the instrument.

**The formula:**
```
Stop Loss = Entry Price - (ATR x Multiplier)   [for longs]
Stop Loss = Entry Price + (ATR x Multiplier)   [for shorts]
```

**Standard multipliers:**
- Conservative: 2.0x ATR
- Standard: 1.5x ATR
- Aggressive: 1.0x ATR

**Example:**
```
Stock: ASML
Current price / Entry: EUR 750
14-period ATR: EUR 18.50

Conservative stop (2x ATR): EUR 750 - (18.50 x 2) = EUR 713
Standard stop (1.5x ATR): EUR 750 - (18.50 x 1.5) = EUR 722.25
Aggressive stop (1x ATR): EUR 750 - 18.50 = EUR 731.50
```

**Why this works:** ATR stops automatically adjust to volatility. In calm markets, stops are tighter (preserving capital). In volatile markets, stops are wider (avoiding noise stops). This is objectively better than using a fixed pip or point distance.

**When to use:** When there is no clear structural level nearby, or when you want a systematic, non-discretionary approach.

### Method 3: Time-Based Stops

A time-based stop exits the trade after a predefined time if the expected move has not occurred.

**The logic:** If your thesis is "price will break out above resistance within 3 days" and after 3 days price is still sitting at resistance, the thesis has not played out. Even if price has not hit your stop loss, the trade is no longer based on your original analysis.

**Implementation:**
- Day trades: Time stop at end of session if target not hit
- Swing trades: Time stop after 3-5 bars of no progress
- Position trades: Re-evaluate weekly; exit if thesis no longer valid

**When to use:** As a secondary stop alongside a price-based stop. Especially useful for breakout trades where time is part of the thesis.

## Stop Management: When and How to Move Stops

### Rule 1: Never Move a Stop Further Away from Entry

This is the cardinal rule. If you are long and price moves against you, you do not move your stop down to "give it more room." That is not risk management — that is hoping. Hope is not a strategy.

If your original stop placement was correct (based on structure or ATR), it remains correct. If the market hits it, you were wrong. Accept it and move on.

### Rule 2: Move to Breakeven After 1R of Profit

When the trade has moved in your favor by one times your risk (1R), move your stop loss to your entry price. You now have a "free trade" — the worst outcome is breaking even.

**Example:**
```
Entry: EUR 100
Stop: EUR 97 (risk = EUR 3)
Target: EUR 109 (reward = EUR 9, R:R = 3:1)

When price reaches EUR 103 (1R of profit):
Move stop to EUR 100 (breakeven)

Now: worst case = EUR 0 loss. Best case = EUR 9 profit.
```

**Caveat:** In volatile markets, moving to breakeven too quickly can result in being stopped out on a pullback before the trade completes. Some traders wait for 1.5R or 2R before moving to breakeven. Adjust based on your instrument's typical pullback depth.

### Rule 3: Trail Your Stop in Trending Markets

If the trade is moving strongly in your favor, trail your stop to lock in profits progressively.

**Trailing methods:**

**Fixed distance trail:** Move stop to X pips or points below the current price (for longs). Simple but can be stopped out on normal pullbacks.

**Swing point trail:** Move stop to below each new higher low (for longs) as the trend develops. More adaptive but requires manual management.

**ATR trail:** Trail stop at entry minus 2x ATR, recalculated periodically. Adapts to changing volatility.

**Moving average trail:** Trail stop to just below a short-term moving average (e.g., 20-period EMA). Exit when price closes below the MA.

### Rule 4: Pre-Plan Your Stop Management

Do not decide how to manage stops in real time. Write your management rules in your trade plan BEFORE you enter:

```
STOP MANAGEMENT PLAN:
1. Initial stop: EUR 97.00 (below support + ATR buffer)
2. Move to breakeven when price reaches: EUR 103.00 (1R)
3. Trail method: Below each new swing low
4. Take partial profits (50%) at: EUR 106.00 (2R)
5. Trail remaining 50% until stop hit or target reached
```

## The Partial Profit Strategy

Taking partial profits reduces the psychological pressure of trade management while locking in gains.

### The 50/25/25 Method

```
Entry: EUR 100
Stop: EUR 97 (3 EUR risk)

Position: 100 shares total

At 2R (EUR 106):
- Sell 50 shares (50% of position)
- Move stop to breakeven
- Locked in: EUR 300 profit (50 shares x EUR 6)

At 3R (EUR 109):
- Sell 25 shares (25% of original)
- Move stop to 2R level (EUR 106)
- Additional locked in: EUR 225 (25 shares x EUR 9)

Trail remaining 25 shares:
- Let the runner ride with a trailing stop
- Final 25 shares trail until stopped out
```

**Why this works psychologically:** After taking partial profits, the pressure is off. You have already banked money. The remaining position is effectively risk-free and can be held with minimal emotional stress. This prevents the common mistake of closing winners too early out of fear.

## Common Stop-Loss Mistakes

### Mistake 1: Stop Too Tight (Getting Stopped on Noise)

If your stop is within normal price noise, you will be stopped out constantly even when your direction is correct. This is the most frustrating experience in trading.

**Fix:** Use ATR to gauge normal price noise. Your stop should be at least 1x ATR from entry, preferably 1.5-2x ATR.

### Mistake 2: Stop Too Wide (Risking Too Much Per Trade)

If your stop is very far away, the position sizing formula produces a very small position. This is fine — it means the trade setup requires more room and the reward needs to be proportionally larger. If the R:R does not justify the wide stop, skip the trade.

**Fix:** If the stop distance makes the risk too large for your target position size, skip the trade. Never widen your risk percentage to accommodate a wide stop.

### Mistake 3: Mental Stops ("I Will Exit If It Hits X")

A mental stop is not a stop. It is a suggestion to your future self that your future self will ignore under emotional pressure.

**Fix:** Always place a hard stop order in the market. The only exception is in very illiquid markets where a resting stop could be hunted — and even then, set a hard alert that forces you to act.

### Mistake 4: Moving Stops to "Round Numbers"

Placing stops at obvious round numbers (EUR 100.00, EUR 50.00) means your stop is at the same level as thousands of other traders. These levels attract liquidity and are more likely to be tested.

**Fix:** Place stops slightly beyond round numbers. Instead of EUR 100.00, use EUR 99.75 (for longs) or EUR 100.25 (for shorts).

---

## Chapter 5 Key Takeaways

- A stop loss defines where your thesis is wrong — place it at a structural invalidation level
- Three methods: structure-based (recommended), ATR-based, and time-based
- Never move a stop further from entry — this is hope, not risk management
- Move to breakeven after 1R profit; trail in trending markets
- Use the partial profit strategy (50/25/25) to reduce psychological pressure
- Always use hard stops, not mental stops
- Avoid obvious round numbers for stop placement
- Pre-plan your stop management before entering the trade

---

*Chapter 6 introduces the Risk-Reward Framework — how to ensure you only take trades that are worth taking.*
