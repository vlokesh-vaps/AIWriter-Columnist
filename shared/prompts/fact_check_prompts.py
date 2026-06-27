"""
Prompt templates for the Fact-Check Service.

This template drives the article verification pipeline, instructing
the LLM to analyze consistency, dates, numbers, and factual claims.
"""

FACT_CHECK_PROMPT = """You are an expert fact-checker at a major news organization.
TASK: Thoroughly fact-check the following article and provide a detailed verification report.
TOPIC: {topic}
ARTICLE:
{article}
Perform the following checks:
1. **Consistency Check**: Verify that all claims in the article are internally consistent (no contradictions).
2. **Date Verification**: Check all dates mentioned in the article for plausibility and consistency.
3. **Number Verification**: Verify that all statistics, percentages, and numerical claims are plausible and internally consistent.
4. **Claim Analysis**: Identify any claims that appear unsubstantiated, exaggerated, or potentially misleading.
5. **Source Attribution**: Check if claims are properly attributed to sources.
Provide your response in the following EXACT JSON format (no markdown, no code blocks, just raw JSON):
{{
    "status": "verified" or "flagged" or "rejected",
    "confidence_score": <integer from 0 to 100>,
    "issues": [
        "Description of issue 1",
        "Description of issue 2"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}}
Rules for scoring:
- 90-100: Article is well-written, factually consistent, no significant issues
- 70-89: Minor issues found, article is mostly accurate
- 50-69: Several issues found, article needs revision
- 0-49: Major issues found, article should be rejected
Set status to:
- "verified" if confidence_score >= 80
- "flagged" if confidence_score is 50-79
- "rejected" if confidence_score < 50
Output ONLY the JSON object, nothing else.
"""
