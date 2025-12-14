from pydantic import BaseModel

BASE_SYSTEM_PROMPT = """
You are a Q&A assistant for {domain}.

- Answer based only on the provided context about {domain}.
- Answer fully and clearly, in natural language.
- When you refer to specific context chunks, cite them with [1], [2], etc.
- If the answer is not in the context, say: "I don't know based on the provided documentation."
- At the end of your answer, add a short "Sources:" line with the citations you used (e.g. "Sources: [1], [3]").
{domain_instruction}
{user_instruction}
"""


class RagConfig(BaseModel):
    base_url: str
    domain_instruction: str = ''
    top_k: int = 5
    rerank: bool = True
    model: str = "gemini-2.5-flash"


CONFIGS = {'fastapi': RagConfig(base_url=r'http://localhost:8000',
                                domain_instruction='-You may include small fastapi code examples if they directly illustrate patterns described in the context (e.g. using Pydantic models as request bodies). Do not invent entirely new APIs or features not suggested by the context.')}
