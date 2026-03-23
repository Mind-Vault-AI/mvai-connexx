# Chapter 11: Security, Privacy, and AI Governance

## Why This Chapter Matters More Than Any Other

Everything we have built in this book — the automations, the prompts, the workflows — becomes a liability if you do not handle security and privacy correctly. One data breach, one GDPR violation, one instance of customer data leaking through an AI prompt, and the trust you have built with your customers evaporates overnight.

This is not paranoia. It is professional due diligence. Every business using AI tools needs a clear, documented approach to security and privacy.

## The AI Security Checklist

Print this. Put it on the wall. Review it quarterly.

### Data Classification

Before using any AI tool, classify your data:

- **Public:** Information available on your website, marketing materials, pricing. Safe to use with any AI tool.
- **Internal:** Business processes, strategies, non-sensitive operational data. Safe for paid AI accounts with data protection agreements (ChatGPT Team/Enterprise, Claude Team).
- **Confidential:** Customer data, financial records, employee information, contracts. Only use with AI tools that have explicit data processing agreements and do not train on your data.
- **Restricted:** Passwords, API keys, medical records, government IDs. Never input into any external AI system. Period.

### The Checklist

**Before Using Any AI Tool:**

- [ ] Read the data retention policy. Does the provider store your inputs? For how long?
- [ ] Check training usage. Does the provider use your data to train their models? Can you opt out?
- [ ] Review the Data Processing Agreement (DPA). Does one exist? Is it GDPR-compliant?
- [ ] Identify where data is processed. Which country? Is there an adequate data protection level?
- [ ] Check encryption. Is data encrypted in transit (TLS) and at rest?
- [ ] Verify SOC 2 or ISO 27001 certification if handling confidential data

**When Building Automations:**

- [ ] Never include real customer names, emails, or personal data in prompt templates
- [ ] Use data anonymization or pseudonymization when testing with real data
- [ ] Store API keys in environment variables, never in automation configurations or code
- [ ] Implement least-privilege access: each automation only accesses what it needs
- [ ] Use separate API keys for each automation (easier to revoke if compromised)
- [ ] Enable logging for all automated actions (audit trail)
- [ ] Set up alerts for unusual patterns (sudden spike in API calls, unexpected data access)

**For Team Usage:**

- [ ] Create an AI Acceptable Use Policy (template below)
- [ ] Train all team members on what data can and cannot be shared with AI tools
- [ ] Use team/enterprise plans instead of individual accounts for business data
- [ ] Implement single sign-on (SSO) where available
- [ ] Regularly audit which team members have access to which AI tools
- [ ] Establish a process for offboarding (revoke access when employees leave)

**Ongoing Maintenance:**

- [ ] Review AI tool privacy policies quarterly (they change frequently)
- [ ] Audit API key usage monthly
- [ ] Test automation error handling annually
- [ ] Update your AI Acceptable Use Policy annually
- [ ] Conduct a security review of all automations before scaling

## GDPR and AI: What You Need to Know

If you operate in the EU or serve EU customers, the General Data Protection Regulation applies to your use of AI tools. Here are the key requirements:

### Lawful Basis for Processing

When you send customer data to an AI tool, you are processing personal data. You need a lawful basis:

- **Legitimate interest:** You can argue that using AI to improve customer service is a legitimate business interest, as long as you balance it against the individual's privacy rights. Document this balance test.
- **Consent:** If you tell customers their data may be processed by AI tools and they agree (e.g., in your terms of service), this provides a clear legal basis.
- **Contract performance:** If the AI processing is necessary to fulfill a contract with the customer (e.g., processing their order), this basis may apply.

### Data Minimization

Only send the minimum necessary data to AI tools. If you need AI to categorize a support ticket, send the ticket content — not the customer's full purchase history, address, and payment details.

**Good practice:**
```
Categorize this support ticket:
"My order has not arrived after 10 days."
```

**Bad practice:**
```
Categorize this support ticket from John Smith
(john@email.com, customer since 2023, VIP tier,
address: 123 Main St, Amsterdam, credit card ending 4242):
"My order #45678 has not arrived after 10 days."
```

### Right to Explanation

If you use AI to make decisions that significantly affect individuals (e.g., credit scoring, hiring), GDPR gives individuals the right to an explanation of how the decision was made. Keep records of:
- What AI tool was used
- What data was input
- What output was generated
- What human review was applied

### Data Processing Agreements

Ensure every AI vendor you use has a signed Data Processing Agreement that covers:
- What data they process
- How they protect it
- Where it is stored
- How long they retain it
- Their obligations under GDPR
- Sub-processor list (who else touches your data)

## Building an AI Acceptable Use Policy

Every organization using AI tools needs a clear policy. Here is a template you can adapt:

```
AI ACCEPTABLE USE POLICY
[Company Name]
Version: 1.0
Effective Date: [date]

1. PURPOSE
This policy governs the use of AI tools (including but not
limited to ChatGPT, Claude, Gemini, and AI features within
business applications) by all employees and contractors.

2. APPROVED AI TOOLS
The following AI tools are approved for business use:
- [Tool 1] — approved for [data classification levels]
- [Tool 2] — approved for [data classification levels]
All other AI tools must be approved by [role] before use.

3. DATA HANDLING RULES
3.1 NEVER input into any AI tool:
    - Passwords, API keys, or credentials
    - Customer payment information
    - Government identification numbers
    - Medical or health information
    - Employee personal data (salary, reviews, disciplinary)
    - Trade secrets or proprietary algorithms

3.2 MAY input into approved AI tools (Team/Enterprise plans):
    - General customer inquiries (anonymized where possible)
    - Business documents and processes
    - Marketing content and strategies
    - Public information and research

3.3 Before inputting customer data:
    - Remove or anonymize personal identifiers when possible
    - Use only the minimum data necessary
    - Log what data was shared and with which tool

4. OUTPUT VERIFICATION
AI-generated content must be reviewed by a human before:
- Sending to customers
- Publishing externally
- Making business decisions
- Entering into legal or financial systems

5. INCIDENT REPORTING
If you accidentally share sensitive data with an AI tool,
report it immediately to [contact] and delete the conversation
if the platform allows it.

6. COMPLIANCE
Violation of this policy may result in disciplinary action.
This policy will be reviewed and updated annually.

Acknowledged by: _________________ Date: _________
```

## Vendor Risk Assessment for AI Tools

Before adding any new AI tool to your stack, evaluate it:

| Factor | Question | Weight |
|--------|----------|--------|
| Data handling | Does the vendor store your data? For how long? | Critical |
| Training | Is your data used to train models? Can you opt out? | Critical |
| Compliance | GDPR compliant? SOC 2? ISO 27001? | Critical |
| DPA | Is a Data Processing Agreement available? | Critical |
| Encryption | Data encrypted in transit and at rest? | High |
| Location | Where is data processed and stored? | High |
| Access control | SSO, MFA, role-based access? | High |
| Uptime | SLA for availability? Incident history? | Medium |
| Vendor lock-in | Can you export your data? Switch easily? | Medium |
| Longevity | Is the vendor financially stable? | Medium |

Score each factor: 3 (good), 2 (acceptable), 1 (concerning), 0 (unacceptable). Any "0" on a critical factor is a hard stop — do not use that vendor for business data.

## Incident Response for AI-Related Issues

### Common AI Incidents

1. **Data leak:** Sensitive data was shared with an AI tool
2. **Hallucination impact:** AI generated incorrect information that was sent to a customer or used for a decision
3. **Automation failure:** An automated workflow malfunctioned and took incorrect actions at scale
4. **Prompt injection:** A malicious user manipulated an AI-powered chatbot to reveal system instructions or sensitive information

### Response Protocol

**Step 1: Contain (within 1 hour)**
- Stop the affected automation immediately
- Revoke relevant API keys
- If a chatbot is affected, take it offline
- Preserve logs and evidence

**Step 2: Assess (within 4 hours)**
- What happened? What data was affected?
- How many customers or records are impacted?
- Is this a GDPR-reportable breach? (If personal data of EU residents is compromised, you may have 72 hours to report to your data protection authority)
- What is the business impact?

**Step 3: Remediate (within 24 hours)**
- Fix the root cause
- Implement additional safeguards
- Test the fix thoroughly before re-enabling

**Step 4: Communicate (as appropriate)**
- Notify affected customers if their data was compromised
- Report to data protection authorities if required by GDPR
- Brief your team on what happened and what changed

**Step 5: Learn (within 1 week)**
- Document the incident: what happened, why, impact, resolution
- Update your security checklist and policies
- Add monitoring or safeguards to prevent recurrence
- Share lessons learned with the team

---

## Chapter 11 Action Checklist

- [ ] Classify your business data (Public, Internal, Confidential, Restricted)
- [ ] Complete the AI Security Checklist for every AI tool you currently use
- [ ] Review the data handling policies of ChatGPT, Claude, and any other AI tools
- [ ] Create your AI Acceptable Use Policy using the template
- [ ] Train your team on AI data handling rules
- [ ] Conduct a vendor risk assessment for your primary AI tools
- [ ] Set up an incident response plan for AI-related issues
- [ ] Schedule quarterly security reviews
- [ ] Ensure GDPR compliance if you serve EU customers
- [ ] Document all AI processing activities for accountability

---

*You have now completed the full guide. Turn to the appendices for the tool comparison matrix, glossary, and printable checklists.*
