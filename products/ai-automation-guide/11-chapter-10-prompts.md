# Chapter 10: The Prompt Template Library — 15 Ready-to-Use Templates

## How to Use These Templates

Each template below is designed to be copied, customized with your specific details (marked with [brackets]), and pasted directly into ChatGPT, Claude, or any compatible AI assistant.

**Customization guide:**
- Replace all [bracketed text] with your specific information
- Remove sections that do not apply to your situation
- Add additional context that is unique to your business
- Test with a few examples before deploying in an automation

The first 10 templates appeared throughout earlier chapters. Here they are collected in one place, along with 5 additional templates.

---

## Customer Support Templates

### Template 1: Email Response Generator

```
ROLE: You are a customer support agent for [Company Name].
TONE: Friendly, professional, empathetic. Use the customer's name.
LENGTH: Under 150 words.

CONTEXT:
Company: [name]
Products/Services: [list]
Return policy: [details]
Shipping times: [details]
Support hours: [details]

CUSTOMER EMAIL:
Subject: {{subject}}
Body: {{body}}
Customer name: {{name}}

INSTRUCTIONS:
1. Address the specific question or concern
2. Provide a clear, actionable answer
3. If you cannot fully resolve the issue, explain next steps
4. If the customer is upset, acknowledge their frustration first
5. End with an invitation to reach out again if needed
6. Never make promises you cannot verify from the information given

Write the response:
```

### Template 2: Complaint De-escalation

```
A customer has written a complaint email. Your job is to
de-escalate the situation and move toward a resolution.

CUSTOMER COMPLAINT:
{{complaint_text}}

COMPANY POLICIES:
[paste relevant policies for refunds, exchanges, compensation]

STRUCTURE YOUR RESPONSE:
1. ACKNOWLEDGE: Name the specific frustration (not generic
   "sorry for the inconvenience")
2. OWN: Take responsibility without making excuses
3. RESOLVE: Offer a specific solution or next step with timeline
4. PREVENT: Briefly mention what you are doing to prevent this
5. GOODWILL: Offer something extra (discount, free shipping, etc.)

TONE: Sincere, not scripted. Do not use phrases like "we value
your business" or "sorry for any inconvenience." Be human.

Write the response:
```

### Template 3: FAQ Answer Generator

```
Based on the following knowledge base, answer the customer's
question. If the answer is not in the knowledge base, say:
"I do not have specific information about that. Please contact
our team at [email] and they will help you within [timeframe]."

KNOWLEDGE BASE:
{{knowledge_base}}

CUSTOMER QUESTION:
{{question}}

RULES:
- Answer in 2-3 sentences maximum
- Include specific details (prices, timeframes, URLs)
- If multiple answers are possible, ask a clarifying question
- Never invent information not in the knowledge base
```

### Template 4: Support Ticket Summary

```
Summarize this support ticket thread for an agent taking over.

TICKET THREAD:
{{ticket_thread}}

Return this format:
CUSTOMER: [name, tier, account age]
ISSUE: [one sentence]
HISTORY: [what has been tried, numbered list]
STATUS: [current state]
NEXT STEP: [recommended action]
RISK LEVEL: [low/medium/high churn risk and why]
```

### Template 5: Customer Feedback Batch Analysis

```
Analyze these customer reviews and provide:

1. Overall sentiment breakdown (positive/neutral/negative %)
2. Top 3 praised aspects (with example quotes)
3. Top 3 complaint areas (with example quotes)
4. Urgent issues needing immediate attention
5. Three actionable recommendations ranked by expected impact

REVIEWS:
{{reviews}}

Format as a brief executive report I can forward to my team.
```

---

## Marketing and Content Templates

### Template 6: Blog Post Outline Generator

```
Generate a detailed blog post outline.

TOPIC: [topic]
TARGET KEYWORD: [primary keyword]
SECONDARY KEYWORDS: [list 3-5]
AUDIENCE: [who will read this]
GOAL: [what should they do after reading]
WORD COUNT TARGET: [number]
COMPETITOR URLS: [optional: paste 2-3 competitor article URLs]

Return:
1. SEO-optimized title (under 60 characters)
2. Meta description (under 155 characters)
3. Introduction hook concept (2 sentences)
4. 6-8 H2 sections, each with:
   - Section heading
   - 2-3 H3 subsections
   - Key points to cover
   - Data or example to include
5. Conclusion with call to action
6. Internal linking opportunities
7. FAQ schema (3 questions and answers)
```

### Template 7: Social Media Week Batch

```
Create a week of [platform] posts for [Company Name].

BRAND: [description]
AUDIENCE: [target]
VOICE: [brand personality — e.g., professional yet approachable]
GOAL: [engagement / traffic / sales / awareness]
THEME THIS WEEK: [optional]

Monday: [type — e.g., industry insight]
Tuesday: [type — e.g., practical tip]
Wednesday: [type — e.g., customer story]
Thursday: [type — e.g., behind the scenes]
Friday: [type — e.g., engagement question]

For each post provide:
- Full post text (formatted for platform)
- 3-5 hashtags
- Image/visual concept description
- Best posting time
- Predicted engagement level (low/medium/high)
```

### Template 8: Email Subject Line Optimizer

```
Generate 10 email subject lines for this email:

EMAIL CONTENT SUMMARY: [describe what the email is about]
AUDIENCE: [who receives it]
PREVIOUS WINNERS: [2-3 past subject lines that got high opens]

For each subject line provide:
- The subject line (under 50 characters)
- Preview text (under 90 characters)
- Psychological trigger used (curiosity/urgency/benefit/
  personalization/social proof)
- Predicted performance (A/B/C)

End with: A/B test recommendation (which 2 to test first)
```

### Template 9: Competitor Content Gap Analysis

```
Analyze these competitor articles on [topic] and find my
opportunity to create something better.

COMPETITOR CONTENT:
[paste summaries or URLs]

Tell me:
1. What ALL competitors cover (table stakes I must include)
2. What only 1-2 cover (potential differentiators)
3. What NONE cover (my unique opportunity)
4. Common weaknesses I can improve on
5. My recommended angle and unique value proposition
6. Suggested title that would stand out in search results
```

### Template 10: Landing Page Copy Framework

```
Write landing page copy for [product/service].

PRODUCT: [name and what it does]
PRICE: [price]
TARGET: [ideal customer in detail]
PAIN POINT: [primary problem it solves]
DIFFERENTIATOR: [why this over alternatives]
PROOF: [testimonials, numbers, or credentials]
CTA: [desired action]

Write each section:

HERO: Headline (under 10 words) + subheadline (under 25 words)
      + CTA button text

PROBLEM: 3-4 sentences agitating the pain point

SOLUTION: 3-4 sentences presenting the product as the answer

FEATURES: 4 features, each as "Feature Name: benefit-focused
description" (what it does for the customer, not what it is)

SOCIAL PROOF: Recommended presentation of available proof

OBJECTIONS: 5 common objections as FAQ questions with answers

FINAL CTA: Closing statement + CTA button text
```

---

## Data and Analysis Templates

### Template 11: Quick Data Summary

```
Analyze this dataset and provide a 1-page executive summary.

DATA: [paste CSV data or describe the dataset]

CONTEXT:
Business type: [your business]
Data period: [date range]
What each row represents: [description]

Provide:
1. Dataset overview (size, date range, completeness)
2. Key statistics for important fields
3. Top 3 findings (each explained in 2-3 sentences)
4. Chart recommendation (what to visualize and how)
5. Recommended next analysis to go deeper

Keep the total summary under 400 words.
```

### Template 12: Period-Over-Period Comparison

```
Compare these two periods and explain the differences.

PERIOD A ([label, e.g., "Q1 2025"]):
[metrics]

PERIOD B ([label, e.g., "Q1 2026"]):
[metrics]

For each metric:
- Absolute change and percentage change
- Significance rating (major/minor/negligible)
- Likely cause
- Recommended action

Conclude with: "The 3 most important changes and their
business impact."
```

### Template 13: Anomaly Detection

```
Review this time series data for anomalies.

DATA: [paste data with dates and values]
NORMAL RANGE: [if known, e.g., "typically 100-150 per day"]

For each anomaly found:
1. Date and actual value
2. Expected value based on pattern
3. Deviation (% from expected)
4. Three possible explanations
5. Investigation priority (high/medium/low)

Also flag any gradual baseline shifts that might indicate a
fundamental change in the underlying pattern.
```

---

## Operations Templates

### Template 14: Standard Operating Procedure Generator

```
Create a Standard Operating Procedure for: [process name]

ROUGH DESCRIPTION:
[describe the process in your own words]

WHO DOES THIS: [role]
FREQUENCY: [how often]
TOOLS USED: [software, equipment]
COMMON PROBLEMS: [what usually goes wrong]

Generate:
1. PURPOSE (2 sentences)
2. SCOPE (when this applies and when it does not)
3. PREREQUISITES (what must be ready before starting)
4. STEP-BY-STEP INSTRUCTIONS (numbered, with decision points
   marked as "IF... THEN...")
5. SCREENSHOTS NEEDED (describe each screenshot location)
6. COMMON ERRORS (problem → solution, 3-5 entries)
7. QUALITY CHECK (how to verify correctness)
8. ESCALATION (when to escalate and to whom)

Write for someone who has never done this task before.
Use simple language. Bold key actions.
```

### Template 15: Meeting Action Item Extractor

```
Extract structured information from this meeting transcript.

MEETING TRANSCRIPT:
{{transcript}}

Return:

SUMMARY (3 sentences: topic, key discussion, outcome)

DECISIONS MADE:
[numbered list of clear decisions]

ACTION ITEMS:
| # | What | Who | By When | Priority |
[Include every commitment, even implicit ones like
"I will check on that"]

OPEN QUESTIONS:
[Items discussed but not resolved]

FOLLOW-UP NEEDED:
[Suggested agenda items for next meeting]

PARKING LOT:
[Ideas mentioned but deferred for later discussion]
```

---

## Prompt Engineering Principles for Business Use

### The CRISP Framework

Every effective business prompt follows the CRISP framework:

**C — Context:** Give the AI enough background to understand your situation. Industry, company size, audience, constraints.

**R — Role:** Tell the AI who it should be. "You are a customer support agent" produces very different output from "You are a data analyst."

**I — Instructions:** Be specific about what you want. Format, length, structure, tone. The more specific you are, the better the output.

**S — Specifics:** Provide concrete details, examples, and constraints. "Write an email" is vague. "Write a 100-word email in a friendly tone addressing the shipping delay for order #12345" is specific.

**P — Parameters:** Define the boundaries. What should the AI not do? What format should the output take? What tone should it avoid?

### Version Control for Prompts

Treat your prompts like code. When you find a prompt that works well:

1. Save it in a shared document or prompt library
2. Version it (v1.0, v1.1, etc.)
3. Note what changes you made and why
4. Track which version is currently deployed in each automation
5. Review and update quarterly

A simple prompt library can be a Google Sheet:

| ID | Name | Version | Last Updated | Used In | Notes |
|----|------|---------|-------------|---------|-------|
| P001 | Email categorizer | v2.3 | 2026-03-15 | Zapier email triage | Added "sales_inquiry" category |
| P002 | Blog outline | v1.1 | 2026-03-01 | Manual use | Added FAQ schema section |

---

## Chapter 10 Action Checklist

- [ ] Copy all 15 templates to your prompt library
- [ ] Customize at least 5 templates with your business specifics
- [ ] Test each customized template with real examples
- [ ] Deploy your top 3 templates in actual automations
- [ ] Set up your prompt library (Google Sheet or Notion database)
- [ ] Schedule quarterly prompt reviews to update and improve

---

*The final chapter covers the critical topic of security and governance when using AI in your business.*
