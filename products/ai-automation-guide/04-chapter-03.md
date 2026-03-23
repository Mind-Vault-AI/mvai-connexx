# Chapter 3: The Automation Audit — Finding Your Gold Mines

## The Task Inventory Method

Before you automate anything, you need to know what you are working with. The Task Inventory Method is a systematic approach to mapping every repetitive task in your business, scoring its automation potential, and prioritizing your efforts for maximum impact.

This is not exciting work. It is foundational work. Skip this chapter, and you will waste time automating the wrong things. Do it properly, and every automation you build will deliver measurable value.

### How to Conduct a Task Inventory

**Duration:** 1 week of observation, 2 hours of analysis
**Who should participate:** Everyone who does operational work — not just management

**Step 1: The Time Log (5 Business Days)**

For one full work week, every team member (including you) logs every task they perform, along with three data points:

1. **Task description** — What exactly are you doing? Be specific. Not "email" but "reading customer emails and forwarding to the right department."
2. **Time spent** — How long did this instance of the task take?
3. **Frequency** — How often do you do this task? Daily? Weekly? Per customer order?

Use a simple spreadsheet:

| Task | Description | Time (min) | Frequency | Who Does It |
|------|-------------|-----------|-----------|-------------|
| Email sorting | Read incoming emails, categorize, forward to correct person | 45 | Daily | Sarah |
| Invoice data entry | Copy data from PDF invoices into accounting software | 30 | Per invoice (~15/week) | Mike |
| Weekly report | Pull data from 3 sources, compile into slides | 180 | Weekly | Sarah |
| Order confirmation | Check order details, send confirmation email to customer | 10 | Per order (~20/day) | Team |
| Social media posting | Write post, find image, schedule across 3 platforms | 45 | Daily | Lisa |
| Lead qualification | Review new leads, check company size, score priority | 20 | Per lead (~10/day) | Sales team |

**Step 2: Calculate the True Cost**

For each task, calculate the monthly time investment:

```
Monthly hours = Time per instance x Frequency per month
Monthly cost = Monthly hours x Loaded hourly rate
```

The loaded hourly rate includes salary, benefits, overhead, and the opportunity cost of not doing higher-value work. For most businesses, this is 1.5x to 2x the base hourly rate.

**Example:**
- Invoice data entry: 30 min x 60 invoices/month = 30 hours/month
- If Mike's loaded hourly rate is EUR 40: 30 x 40 = EUR 1,200/month on manual data entry

That EUR 1,200/month is what you can save by automating invoice data entry. Suddenly, a $50/month automation tool looks like an exceptional investment.

**Step 3: Score Each Task for Automation Potential**

Not every task can or should be automated. Score each task on four dimensions:

**Repeatability (1-5):** How consistent is this task? Does it follow the same pattern every time?
- 5: Identical every time (e.g., forwarding emails based on subject line)
- 3: Mostly consistent with some variations (e.g., writing social media posts)
- 1: Unique every time (e.g., strategic planning meetings)

**Rule-Based (1-5):** Can you write clear rules for how to do this task?
- 5: Simple if/then logic (e.g., if invoice > EUR 1000, send to manager)
- 3: Some judgment required but generally predictable (e.g., categorizing support tickets)
- 1: Requires deep expertise and creative thinking

**Data Availability (1-5):** Is the information needed for this task available digitally?
- 5: All inputs and outputs are already in software systems
- 3: Some data is digital, some is in emails or documents
- 1: Information requires phone calls, physical inspection, or tacit knowledge

**Impact (1-5):** How much time, money, or quality improvement would automation deliver?
- 5: Major time savings (10+ hours/month) or significant error reduction
- 3: Moderate savings (3-10 hours/month)
- 1: Minimal impact (less than 1 hour/month)

**Automation Score = Repeatability + Rule-Based + Data Availability + Impact**

| Score | Recommendation |
|-------|----------------|
| 16-20 | Automate immediately — this is low-hanging fruit |
| 12-15 | Strong candidate — plan for automation in next 30 days |
| 8-11 | Possible candidate — evaluate further, may need partial automation |
| 4-7 | Not a good candidate — keep manual for now |

## The Automation Priority Matrix

Now plot your top-scoring tasks on a 2x2 matrix:

```
                    HIGH IMPACT
                        |
         Quick Wins     |    Strategic Projects
         (DO FIRST)     |    (PLAN CAREFULLY)
                        |
    LOW EFFORT ---------+--------- HIGH EFFORT
                        |
         Fill-Ins       |    Avoid (for now)
         (DO WHEN       |    (REVISIT LATER)
          TIME ALLOWS)  |
                        |
                    LOW IMPACT
```

**Quick Wins (High Impact, Low Effort):** These are your gold mines. Simple automations that deliver significant value. Email forwarding, data entry, report generation, notification sending. Start here.

**Strategic Projects (High Impact, High Effort):** These are worth doing but require planning. Customer onboarding workflows, complete content pipelines, AI-powered support systems. Plan these for month 2-3.

**Fill-Ins (Low Impact, Low Effort):** Nice to have. Set these up when you have spare time or want to practice. Calendar reminders, file organization, simple notifications.

**Avoid (Low Impact, High Effort):** Not worth the investment right now. Revisit in 6 months when you have more automation experience and the effort calculation may have changed.

## Identifying Your Top 5 Automation Candidates

From your scored and prioritized task inventory, select your top 5 automation candidates. These should be:

1. At least 3 Quick Wins (high impact, low effort)
2. No more than 2 Strategic Projects
3. Distributed across different business functions (do not automate only marketing tasks if your biggest pain is in operations)

For each of your top 5, fill in this brief:

### Automation Candidate Brief

```
Task Name: _________________________________
Current process (step by step):
1. ___________________________________________
2. ___________________________________________
3. ___________________________________________
4. ___________________________________________
5. ___________________________________________

Who does this now: _________________________
Time per instance: _______ minutes
Frequency: _______ times per _______________
Monthly time cost: _______ hours
Monthly financial cost: EUR ________________

Desired outcome:
What should happen automatically: ___________
What still needs human involvement: _________

Success metric:
Before: _____________________________________
Target after: _______________________________
How to measure: _____________________________
```

### Example: Completed Brief

```
Task Name: Customer order confirmation emails
Current process:
1. Order comes in via Shopify notification
2. Sarah opens Shopify, reviews order details
3. Sarah opens email, writes personalized confirmation
4. Sarah includes estimated delivery date (checks spreadsheet)
5. Sarah sends email, logs in CRM

Who does this now: Sarah (customer success)
Time per instance: 8 minutes
Frequency: 20 times per day
Monthly time cost: 53 hours
Monthly financial cost: EUR 2,120

Desired outcome:
What should happen automatically: Order triggers confirmation
email with personalized details and estimated delivery date.
Email is logged in CRM automatically.
What still needs human involvement: Exception handling —
orders with special notes, custom products, or payment issues
should be flagged for Sarah to review.

Success metric:
Before: 8 minutes per order, 53 hours/month
Target after: 0 minutes for standard orders (90% of volume),
Sarah reviews only exceptions (~10%)
How to measure: Track automated vs manual confirmations
in CRM, measure Sarah's time on order confirmation tasks
```

## Common Automation Opportunities by Business Type

If you are struggling to identify candidates, here are the most common automation opportunities by business type:

### E-Commerce
1. Order confirmation and shipping notification emails
2. Inventory level alerts and reorder triggers
3. Customer review requests (timed after delivery)
4. Return and refund processing
5. Abandoned cart follow-up sequences

### Professional Services (Consultants, Agencies, Freelancers)
1. Lead qualification and intake forms
2. Client onboarding document collection
3. Time tracking and invoice generation
4. Project status update reports
5. Proposal and contract generation

### SaaS / Tech
1. User onboarding email sequences
2. Usage-based feature recommendations
3. Churn risk alerts from usage patterns
4. Bug report categorization and routing
5. Knowledge base article suggestions from support tickets

### Retail / Local Business
1. Appointment booking and reminders
2. Customer loyalty program management
3. Social media content scheduling
4. Local inventory updates to Google My Business
5. Customer feedback collection and response

### B2B / Wholesale
1. Quote generation from product catalogs
2. Order processing and fulfillment tracking
3. Customer payment reminders
4. Inventory and supply chain alerts
5. Competitive price monitoring

## The Pre-Automation Cleanup

Before you automate any task, spend 15 minutes cleaning it up. Answer these questions:

1. **Is every step actually necessary?** Remove steps that exist because "we have always done it this way."
2. **Are there unnecessary handoffs?** Every time work moves from one person to another, delays and errors increase.
3. **Is the data clean?** If your spreadsheet has inconsistent formatting, fix that before you automate.
4. **Are there clear rules for exceptions?** Document what happens when the normal process does not apply.
5. **Does everyone agree on how this task should be done?** If three people do the same task three different ways, standardize first.

This cleanup often saves 20-30% of the task time even before automation. It also ensures that when you do automate, you are automating the best version of the process.

---

## Chapter 3 Action Checklist

- [ ] Start your Task Inventory this week — log every repetitive task for 5 business days
- [ ] Calculate the monthly time and financial cost of each task
- [ ] Score each task on the Automation Potential framework (Repeatability, Rule-Based, Data Availability, Impact)
- [ ] Plot your top tasks on the Priority Matrix
- [ ] Select your Top 5 automation candidates
- [ ] Complete the Automation Candidate Brief for each of your Top 5
- [ ] Do the Pre-Automation Cleanup for your number 1 candidate
- [ ] Share your Top 5 with your team and get their input

---

*In Chapter 4, we will tackle one of the highest-impact automation areas: customer communication and support.*
