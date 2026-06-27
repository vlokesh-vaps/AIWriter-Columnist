"""
Prompt templates for the AI Writer Service.

These templates drive headline generation, article writing, summarization,
and SEO metadata creation through the LLM provider.
"""

HEADLINE_PROMPT = """You are a senior headline editor at a major news organization.
TASK: Generate a compelling, accurate, and engaging headline for the following article topic.
TOPIC: {topic}
RESEARCH CONTEXT:
{research}
Requirements:
- The headline must be concise (8-15 words maximum)
- It must accurately reflect the content
- It should be attention-grabbing but not clickbait
- Use active voice when possible
Output ONLY the headline text, nothing else.
"""


ARTICLE_PROMPT = """You are an award-winning journalist at a major news publication.
TASK: Write a comprehensive, well-structured news article based on the following topic and research.
TOPIC: {topic}
RESEARCH:
{research}
Requirements:
- Write in a professional journalistic style
- Use the inverted pyramid structure (most important information first)
- Include relevant statistics and data points from the research
- Use clear, concise language accessible to a general audience
- Include quotes or expert perspectives where appropriate
- Structure with clear paragraphs, each covering a distinct point
- Article length: 600-1000 words
- Maintain objectivity and balanced reporting
Write the full article body. Do not include a headline or summary.
"""


SUMMARY_PROMPT = """You are a news editor specializing in article summaries.
TASK: Write a concise summary of the following article.
TOPIC: {topic}
ARTICLE:
{article}
Requirements:
- Summary length: 2-3 sentences (50-80 words)
- Capture the key message and most important findings
- Written in third person, present tense
- Should stand alone and be understandable without the full article
Output ONLY the summary text, nothing else.
"""


SEO_TITLE_PROMPT = """You are an SEO specialist for a news organization.
TASK: Generate an SEO-optimized page title for the following article.
TOPIC: {topic}
HEADLINE: {headline}
Requirements:
- Length: 50-60 characters maximum
- Include the primary keyword naturally
- Make it compelling for search engine results pages (SERPs)
- Different from the headline but covering the same topic
Output ONLY the SEO title text, nothing else.
"""


META_DESCRIPTION_PROMPT = """You are an SEO specialist for a news organization.
TASK: Generate an SEO meta description for the following article.
TOPIC: {topic}
HEADLINE: {headline}
SUMMARY: {summary}
Requirements:
- Length: 150-160 characters maximum
- Include relevant keywords naturally
- Compelling enough to drive click-through from search results
- Accurately represent the article content
- Include a subtle call to action
Output ONLY the meta description text, nothing else.
"""
