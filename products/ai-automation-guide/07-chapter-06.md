# Chapter 6: AI for Data Analysis — Turn Spreadsheets Into Strategy

## The Spreadsheet Graveyard Problem

Every business has them. Spreadsheets full of data that someone once set up with good intentions, that get updated religiously, but that nobody actually analyzes. They are digital filing cabinets — storage, not intelligence.

The problem is not the data. It is the gap between having data and extracting insight. A skilled data analyst can look at your sales spreadsheet and tell you that your Tuesday customers spend 34% more than your Friday customers, that Product C is cannibalizing Product A, and that your best marketing channel for high-value customers is not the one you are spending the most on. But most small businesses do not have a data analyst. They have a spreadsheet and a vague sense that "the numbers are in there somewhere."

AI bridges that gap. It cannot replace a senior data scientist building predictive models, but it can give every business owner the analytical capabilities of a competent analyst — today, for free, with data they already have.

## Turning Spreadsheet Chaos Into Insights

### The Data Analysis Prompt Framework

The biggest mistake people make when asking AI to analyze data is being too vague. "Analyze this spreadsheet" produces generic observations. Specific questions produce actionable insights.

**Step 1: Prepare your data**

Before feeding data to an AI, clean it up:
- Remove empty rows and columns
- Ensure column headers are clear and consistent
- Check for obvious errors (negative quantities, dates in the future)
- Remove any personally identifiable information (GDPR compliance)
- Export as CSV for easiest processing

**Step 2: Describe your data context**

```
I am uploading a CSV file containing [describe data].

CONTEXT:
Business type: [your business]
Data period: [date range]
Number of records: [approximate]
What each row represents: [e.g., one sales transaction]

COLUMN DESCRIPTIONS:
- [column_name]: [what it contains, unit of measurement]
- [column_name]: [what it contains, unit of measurement]
- [repeat for all columns]

BUSINESS CONTEXT:
- Our average order value is typically EUR [X]
- We consider a "good month" to be [metric]
- Our main concern right now is [specific concern]
```

**Step 3: Ask specific questions**

```
Based on this data, please answer the following questions:

1. TRENDS: What are the most significant trends over this period?
   Show the direction, magnitude, and whether the trend is
   accelerating or decelerating.

2. SEGMENTS: Are there meaningful segments in this data?
   (e.g., customer groups that behave differently, product
   categories with different patterns)

3. ANOMALIES: Are there any data points that are unusual or
   unexpected? What might explain them?

4. CORRELATIONS: Are there any interesting relationships between
   variables? (e.g., does X increase when Y decreases?)

5. PREDICTION: Based on current trends, what do you expect for
   the next [time period]? What assumptions does this depend on?

6. ACTION: Based on this analysis, what are the top 3 actions
   I should consider? For each, estimate the potential impact.

Present your findings in a format I can share with my team:
executive summary (3 sentences), key findings (bullet points),
detailed analysis, and recommendations.
```

### Real-World Example: Sales Data Analysis

Here is a practical example with a fictional e-commerce business:

**Input to AI:**
```
I am uploading our sales data for Q1 2026 (January-March).

Business: Online supplement store (Netherlands)
Each row: One order
Columns: order_date, customer_id, product_name, category,
quantity, unit_price, total, discount_applied, payment_method,
shipping_city, is_returning_customer

My concern: Revenue was flat in March despite increased traffic.
I need to understand why and what to do about it.
```

**The kind of insight AI can produce:**

"Revenue was flat in March because your average order value dropped 18% (from EUR 67 to EUR 55), even though order count increased 12%. Three factors drove this:

1. A 40% increase in orders for your lowest-priced product (Vitamin D, EUR 12.99), likely driven by the spring campaign you ran. These customers ordered 1.2 items on average vs. 2.8 for your typical customer.

2. Your protein powder category, which represents 35% of revenue, saw a 15% price-sensitive shift — more customers chose the 500g size over the 1kg size, suggesting price resistance.

3. Returning customer rate dropped from 42% to 31%. New customers spend 40% less on their first order.

Recommendations:
1. Add a bundle offer on the Vitamin D product page (cross-sell higher-margin items)
2. Test a small discount on the 1kg protein powder (recovering the size upgrade could add EUR 8,400/month)
3. Implement a post-first-purchase email sequence targeting the March new customers to drive repeat purchases within 30 days"

That analysis would take a human analyst 2-4 hours. AI can produce it in 2 minutes — and more importantly, the business owner who does not have an analyst can now get this kind of insight at all.

## Automated Reporting Pipelines

### Weekly Business Dashboard

Instead of manually pulling data from multiple sources every week, automate the entire reporting pipeline.

**The Make/Zapier workflow:**

```
Every Monday at 8:00 AM:

1. Pull this week's data from:
   - Google Analytics (traffic, conversions)
   - Shopify/Stripe (revenue, orders, AOV)
   - Email platform (open rates, click rates, list growth)
   - Support system (ticket count, resolution time, satisfaction)
   - Social media (followers, engagement, reach)

2. Compile into a standardized format

3. Send to ChatGPT API with this prompt:
   "Analyze this week's business metrics compared to last week
   and the 4-week average. Highlight: (1) What improved,
   (2) What declined, (3) What needs attention, (4) One
   specific recommendation for this week. Keep it under 300
   words. Use bullet points."

4. Format the AI analysis into an email template

5. Send to the team
```

### The Executive Summary Prompt

```
You are a business analyst creating a weekly performance summary.

THIS WEEK'S METRICS:
Revenue: EUR [X] (last week: EUR [Y], 4-week avg: EUR [Z])
Orders: [X] (last week: [Y], 4-week avg: [Z])
Average Order Value: EUR [X] (last week: EUR [Y])
Website Traffic: [X] sessions (last week: [Y])
Conversion Rate: [X]% (last week: [Y]%)
Email Open Rate: [X]% (last week: [Y]%)
Support Tickets: [X] (last week: [Y])
Avg Resolution Time: [X] hours (last week: [Y])
Customer Satisfaction: [X]/5 (last week: [Y])

FORMAT YOUR RESPONSE AS:

WEEK OF [date] — PERFORMANCE SUMMARY

TRAFFIC LIGHT STATUS:
🟢 [metrics that improved 5%+ vs 4-week avg]
🟡 [metrics within +/- 5% of 4-week avg]
🔴 [metrics that declined 5%+ vs 4-week avg]

KEY INSIGHTS:
[3-5 bullet points, each one sentence, focusing on the most
significant changes and their likely causes]

THIS WEEK'S RECOMMENDATION:
[One specific, actionable recommendation based on the data]

Keep the entire summary under 200 words. Executives do not
read long reports.
```

## Financial Forecasting with AI Assistance

AI is not a crystal ball, but it can help you make more informed projections by identifying patterns in your historical data.

### Revenue Forecasting Prompt

```
I am going to provide my monthly revenue data for the past 24 months.
Help me create a revenue forecast for the next 6 months.

MONTHLY REVENUE (EUR):
[Month 1]: [amount]
[Month 2]: [amount]
...
[Month 24]: [amount]

KNOWN FACTORS:
- Seasonal patterns: [describe any known seasonality]
- Planned changes: [new product launches, price changes, marketing campaigns]
- Market conditions: [any relevant external factors]

PLEASE PROVIDE:
1. Trend analysis: Is revenue growing, flat, or declining?
   What is the average monthly growth rate?
2. Seasonal pattern: Are there consistent monthly patterns?
3. Base forecast: Expected revenue per month for next 6 months
4. Optimistic scenario: What if things go 20% better than trend
5. Pessimistic scenario: What if things go 20% worse than trend
6. Key assumptions: What must be true for the base forecast
7. Risk factors: What could cause significant deviation
8. Confidence level: How confident should I be in this forecast

Present as a table with month, base, optimistic, and pessimistic
columns, followed by your analysis.
```

## Customer Segmentation Automation

### The RFM Analysis Prompt

RFM (Recency, Frequency, Monetary) analysis is one of the most powerful customer segmentation tools. Here is how to do it with AI:

```
I am providing customer transaction data. Perform an RFM analysis.

DATA: [CSV with customer_id, transaction_date, transaction_amount]

FOR EACH CUSTOMER, CALCULATE:
- Recency: Days since last purchase
- Frequency: Total number of purchases
- Monetary: Total amount spent

THEN SEGMENT CUSTOMERS INTO:
1. Champions: Recent, frequent, high spenders (top 20% in all dimensions)
2. Loyal: Frequent buyers with good monetary value
3. Potential Loyalists: Recent customers with growing frequency
4. New Customers: Very recent, low frequency
5. At Risk: Previously good customers who have not bought recently
6. Lost: Have not purchased in a long time, previously active

FOR EACH SEGMENT, PROVIDE:
- Number of customers and percentage of total
- Average revenue per customer
- Recommended action (e.g., "Send win-back campaign")
- Estimated revenue impact of the recommended action
- Priority level (1-5)

Present results as a table followed by a strategy recommendation
for each segment.
```

## Data Analysis Prompt Templates

### Template 11: Quick Data Summary

```
Analyze this dataset and provide a 1-page executive summary.

DATA: [paste or upload]

Include:
1. Dataset overview (rows, columns, date range, completeness)
2. Key statistics (averages, medians, min/max for important fields)
3. Top 3 most important findings
4. One chart description (what chart would best visualize the
   most important finding)
5. Recommended next analysis to go deeper
```

### Template 12: Comparison Analysis

```
Compare these two time periods and explain the differences:

PERIOD A: [description, e.g., "Q1 2025"]
[data or metrics for Period A]

PERIOD B: [description, e.g., "Q1 2026"]
[data or metrics for Period B]

For each metric:
- Show absolute change and percentage change
- Rate significance (major/minor/negligible)
- Suggest likely cause
- Recommend action if needed

End with: "The 3 most important differences are..." with
business impact estimated for each.
```

### Template 13: Anomaly Detection

```
Review this time series data and identify any anomalies
(data points that are significantly different from the expected
pattern).

DATA: [paste time series data]

For each anomaly found:
1. Date and value
2. Expected value based on pattern
3. Deviation (how far off from expected)
4. Potential explanations (list 2-3 possibilities)
5. Whether it requires investigation (yes/no)

Also flag any gradual shifts in the baseline that might indicate
a fundamental change in the underlying pattern.
```

---

## Chapter 6 Action Checklist

- [ ] Export your most important business data as a clean CSV
- [ ] Run the data analysis prompt framework on your sales data
- [ ] Set up a weekly automated reporting pipeline
- [ ] Perform an RFM analysis on your customer data
- [ ] Create a revenue forecast for the next 6 months
- [ ] Identify 3 data-driven decisions you can make based on findings
- [ ] Schedule a monthly "data review" where you run these analyses

---

*In Chapter 7, we cover AI for operations and administration — the unsexy but high-impact automations.*
