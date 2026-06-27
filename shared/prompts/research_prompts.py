"""
Prompt templates for the Research Service.

These templates are used by ResearchService to generate structured
research output through the LLM provider.
"""

RESEARCH_PROMPT = """You are an expert research analyst for a professional newsroom.
TASK: Conduct comprehensive research on the following topic and generate detailed research notes.
TOPIC: {topic}
Provide your research in the following structured format:
1. **Overview**: A comprehensive overview of the topic, covering its current state, significance, and key developments.
2. **Key Findings**: Important facts, statistics, and data points related to the topic. Include specific numbers, percentages, and dates where applicable.
3. **Industry Trends**: Current trends, emerging patterns, and future projections related to the topic.
4. **Expert Perspectives**: Summarize different viewpoints and expert opinions on the topic.
5. **Challenges and Concerns**: Key challenges, risks, or concerns associated with the topic.
6. **Opportunities**: Potential opportunities, innovations, or positive developments.
Write in a factual, objective, and well-organized manner suitable for professional journalism.
Ensure all information is presented clearly and can be verified.
"""


REFERENCES_PROMPT = """You are a research reference specialist for a professional newsroom.
TASK: Based on the following research topic, generate a list of realistic and relevant reference sources that a journalist would use.
TOPIC: {topic}
Generate 5-8 reference entries. For each reference, provide:
- Source name (publication, organization, or institution)
- Title of the report, article, or study
- Year of publication
- Brief description of what the source covers
Format each reference on a single line like:
"Source Name - Title of Work (Year): Brief description"
Only output the references, one per line. Do not include numbering or bullet points.
"""
