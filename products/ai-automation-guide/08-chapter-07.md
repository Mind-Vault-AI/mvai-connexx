# Chapter 7: AI for Operations and Administration

## The Hidden Cost of Admin Work

Operations and administration are the unglamorous backbone of every business. Nobody gets excited about processing invoices, extracting data from documents, or compiling meeting notes. But these tasks consume an enormous amount of time — often 30-40% of a knowledge worker's week.

The good news: administrative tasks are among the easiest to automate because they are typically repetitive, rule-based, and well-documented.

## Document Processing and Extraction

### Extracting Data from PDFs and Images

One of the most common admin bottlenecks is extracting information from documents — invoices, contracts, receipts, forms — and entering it into your systems.

**The extraction prompt (works with ChatGPT-4 Vision or Claude with file upload):**

```
I am uploading a [document type: invoice/receipt/contract/form].

Extract the following information and return it as JSON:

For invoices:
{
  "vendor_name": "",
  "vendor_address": "",
  "invoice_number": "",
  "invoice_date": "",
  "due_date": "",
  "subtotal": "",
  "tax_amount": "",
  "tax_rate": "",
  "total_amount": "",
  "currency": "",
  "line_items": [
    {
      "description": "",
      "quantity": "",
      "unit_price": "",
      "line_total": ""
    }
  ],
  "payment_terms": "",
  "bank_details": ""
}

If any field is not present in the document, use null.
If any value is ambiguous, include a "notes" field explaining
the ambiguity.
```

**Automation workflow for invoice processing:**

1. **Trigger:** New email with attachment in invoices@yourcompany.com
2. **Filter:** Attachment is PDF or image
3. **Action 1:** Upload to AI (ChatGPT Vision API or similar)
4. **Action 2:** Extract data using the prompt above
5. **Action 3:** Parse JSON response
6. **Action 4:** Create entry in accounting software (Xero, QuickBooks, etc.)
7. **Action 5:** If total > EUR 500, send approval request to manager
8. **Action 6:** Log the processing in your Automation Log

**Real savings:** If you process 50 invoices per month and each takes 5 minutes manually, that is 4+ hours per month. Automated, it takes zero human time for standard invoices and 1-2 minutes each for exceptions.

## Meeting Notes and Action Item Extraction

### The Meeting Summary Workflow

**Step 1: Record and transcribe**
Use Otter.ai, Fireflies.ai, or the built-in recording features of Zoom/Teams/Google Meet to get a transcript.

**Step 2: AI extraction prompt**

```
Here is a meeting transcript. Extract the following:

1. MEETING SUMMARY (3-5 sentences — what was this meeting about
   and what was decided)

2. KEY DECISIONS (numbered list — each decision should be one
   clear sentence)

3. ACTION ITEMS (table format):
   | # | Action Item | Owner | Deadline | Priority |
   [Extract every commitment made, including implicit ones like
   "I will look into that"]

4. OPEN QUESTIONS (items that were discussed but not resolved —
   need follow-up)

5. NEXT MEETING (date/time if mentioned, suggested agenda items
   based on open questions and upcoming deadlines)

MEETING TRANSCRIPT:
[paste transcript]

FORMAT: Use markdown. Be concise. Action items should be specific
enough that someone who was not in the meeting knows exactly what
to do.
```

**Step 3: Automate distribution**

**Zapier workflow:**
1. Trigger: New transcript in Otter.ai / Fireflies.ai
2. Action 1: Send transcript to ChatGPT for extraction
3. Action 2: Create tasks in project management tool (Asana, Notion, Trello) for each action item
4. Action 3: Send meeting summary email to all participants
5. Action 4: Schedule follow-up reminders for action items

## HR and Recruitment Screening

### Resume Screening Automation

Before using AI for HR tasks, a critical warning: AI can introduce or amplify bias in hiring. Always use AI screening as a first-pass filter, never as the final decision. Human review of AI recommendations is mandatory.

**The screening prompt:**

```
I am hiring for the position of [job title].

KEY REQUIREMENTS (must-have):
1. [requirement 1]
2. [requirement 2]
3. [requirement 3]

PREFERRED QUALIFICATIONS (nice-to-have):
1. [qualification 1]
2. [qualification 2]

RESUME TEXT:
[paste resume text]

EVALUATION:
1. Score each must-have requirement: Met / Partially Met / Not Met
2. Score each preferred qualification: Present / Not Present
3. Overall fit score: 1-10
4. Key strengths for this role (2-3 bullets)
5. Potential concerns or gaps (2-3 bullets)
6. Recommended action: Advance to interview / Maybe / Pass

IMPORTANT: Base your evaluation ONLY on the information in the
resume. Do not make assumptions about the candidate based on
name, location, school name, or graduation year.
```

### Interview Question Generation

```
Generate interview questions for [job title] position.

JOB REQUIREMENTS:
[paste key requirements]

GENERATE:
1. Five behavioral questions (STAR format) targeting the key skills
2. Three situational questions relevant to the role
3. Two technical/knowledge questions
4. One culture-fit question

FOR EACH QUESTION:
- The question itself
- What a strong answer looks like
- What a weak answer looks like
- Follow-up probe questions
```

## Project Management Automation

### Automated Status Reports

```
Based on these project updates, generate a status report.

PROJECT: [name]
REPORTING PERIOD: [date range]

TASK UPDATES:
[paste task list with status updates]

GENERATE:
1. Executive summary (3 sentences: overall status, key progress,
   main risk)
2. Traffic light status: 🟢 On track / 🟡 At risk / 🔴 Behind
3. Completed this period (bullet list)
4. In progress (bullet list with % complete)
5. Blocked items (with blocker description and who can unblock)
6. Upcoming milestones (next 2 weeks)
7. Resource needs or escalations
8. Updated risk register (risk, probability, impact, mitigation)
```

### Task Breakdown from Requirements

```
Break down this project requirement into actionable tasks.

REQUIREMENT:
[paste the requirement or feature description]

FOR EACH TASK:
- Task name (clear and actionable, starts with a verb)
- Description (what "done" looks like)
- Estimated effort (hours)
- Dependencies (which other tasks must be done first)
- Required skills/role
- Priority (P1/P2/P3)

Organize tasks in recommended execution order.
Include a total estimated effort and suggested timeline
assuming [X] people working [Y] hours per day on this.
```

## Standard Operating Procedure (SOP) Generation

One of the most undervalued automation opportunities is creating and maintaining SOPs. AI can help you document processes that currently exist only in people's heads.

```
Help me create a Standard Operating Procedure (SOP) for:
[process name]

PROCESS DESCRIPTION (rough):
[describe the process in your own words, including any steps
you can remember]

WHO PERFORMS THIS: [role/person]
FREQUENCY: [how often]
TOOLS USED: [software, equipment]

GENERATE AN SOP WITH:
1. Purpose: Why this process exists and what outcome it produces
2. Scope: When this SOP applies (and when it does not)
3. Prerequisites: What must be in place before starting
4. Step-by-step instructions: Numbered, specific, with
   decision points clearly marked
5. Screenshots needed: Where in the process should screenshots
   be added (describe what each screenshot should show)
6. Common errors: What typically goes wrong and how to fix it
7. Quality check: How to verify the process was done correctly
8. Escalation: When to escalate and to whom
9. Version history: Template for tracking changes

FORMAT: Use numbered steps, bold key actions, and indent
sub-steps. Write for someone who has never done this before.
```

---

## Chapter 7 Action Checklist

- [ ] Set up automated invoice processing for your most common vendor invoices
- [ ] Implement meeting transcription and AI-powered summary for your next meeting
- [ ] Create one SOP using the AI-assisted template for your most critical process
- [ ] If hiring, test the resume screening prompt on recent applicants (compare to your own assessments)
- [ ] Build an automated status report for your current projects
- [ ] Identify the top 3 admin tasks consuming the most time in your organization

---

*Chapter 8 takes a deep dive into building powerful workflows on Zapier, Make, and n8n.*
