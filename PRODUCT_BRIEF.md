# Product Brief: Pipeline Reality Checker (Track 2)

## 1. Problem Statement
Sales managers routinely look at CRM pipelines that appear healthy, only to miss end-of-month revenue targets. This discrepancy happens because CRM data relies heavily on subjective updates from sales representatives who are naturally over-optimistic or too busy to flag stalling deals. Traditional CRMs treat a deal in the "Proposal" stage as highly viable, ignoring underlying risk signals like conversational stagnation, unaddressed objections, or missing decision-makers.

## 2. User Persona
* **Name:** Marcus Vance, Sales Manager
* **Context:** Manages a team of 6 B2B Account Executives. He spends hours reviewing pipeline health in weekly 1-on-1s, relying on his reps' verbal accounts and messy CRM activity notes.
* **Core Pain:** Marcus gets blindsided at the end of the quarter when deals that were marked "90% likely to close" abruptly fall through or push out to the next fiscal period.

## 3. Job-to-be-Done (JTBD) Statement
> **When** I review my sales pipeline,
> **I want to** immediately isolate which deals are statistically and contextually at risk of slipping,
> **So that** I can direct my coaching and deal-intervention strategies where they matter most before the revenue window closes.

## 4. Why AI? (Critical Thinking)
Traditional software uses strict rules-based filters (e.g., *“If last activity > 14 days, mark red”*). While useful, this approach misses nuanced context. 
* **What Logic Handles Best:** High-accuracy quantitative checks (e.g., exact days since last email, deal size deviations, pipeline stage stagnation periods).
* **What AI Handles Best:** Unstructured qualitative text analysis. AI reads between the lines of a sales rep's messy update notes to spot hidden red flags, such as budget hesitation, competitive threats, shifting timelines, or a champion losing internal influence.

## 5. Feature List (Value vs. Effort)

| Feature | Description | Value | Effort |
| :--- | :--- | :--- | :--- |
| **Structured Intake Form** | Standardized ingestion of deal metrics and unstructured notes. | High | Low |
| **Pre-AI Deterministic Logic** | Calculates hard stagnation thresholds and flags low activity instantly. | High | Low |
| **Contextual Risk LLM Parser**| Extracts conversational risk factors and maps out the *why*. | Critical | Medium |
| **Prescriptive Next-Action Engine**| Generates a hyper-specific, actionable tactic to save the deal. | High | Medium |
| **Historical Admin Dashboard** | Audits past analyses and visualizes deal decay over time. | High | Medium |

## 6. Failure Mode Analysis & Mitigation
* **Primary Failure Mode:** **False Positive Over-Flagging.** If the application flags every single deal as "at risk," the Sales Manager will experience alert fatigue and stop trusting the tool entirely.
* **Mitigation Strategy:** Establish a calibrated **Confidence Score**. The AI must explicitly score its confidence based on the depth of evidence found in the notes. If the text is brief or inconclusive, the tool will report a low confidence score, signaling to Marcus that it requires more thorough CRM input rather than ringing a false alarm.

## 7. AI Trade-offs
* **Model Choice:** We use a lightweight, instruct-tuned LLM (like `gpt-4o-mini`). 
* **Trade-off:** While a larger model might capture ultra-deep corporate dynamics, it introduces high latency and cost. An optimized, smaller model combined with tight systemic logic delivers sub-2-second responses, which keeps the sales workflow fast and highly responsive.

## 8. Cost & Sustainability
* **Input Tokens per Deal:** ~800 tokens (System prompt + Deal details + 500 words of notes).
* **Output Tokens per Deal:** ~300 tokens (Structured JSON analysis + Next Action recommendation).
* **Unit Economics:** At current API rates, analyzing 100 deals costs roughly $0.15. This is an incredibly sustainable operational cost for any enterprise B2B sales org.

## 9. Architectural Reflection
An AI product is only as reliable as its guardrails. By parsing data through a hard-coded Python logic layer *before* it hits the LLM, we ground the generation in absolute reality (e.g., exact timestamps). This prevents the AI from hallucinating a deal's timeline, forcing it to focus entirely on its true job: contextual risk diagnosis.
