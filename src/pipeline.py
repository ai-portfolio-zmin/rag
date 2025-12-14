from src.retrieval.client import HybridRetriever
from src.config import CONFIGS, BASE_SYSTEM_PROMPT
from google import genai
from src.util import build_context
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger('RAG pipeline')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RagPipeline:

    def __init__(self, corpus):
        self.corpus = corpus
        self.config = CONFIGS.get(corpus)
        if self.config is None:
            raise ValueError(f'config for {corpus} not available')
        self.retriever = HybridRetriever(base_url=self.config.base_url,
                                         corpus=corpus)
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    def answer(self, query, extra_instruction=''):
        logger.info(f'question: {query}. Extra instruction: {extra_instruction}')
        logger.info(f'context: {self.corpus}')
        retrieved_docs = self.retriever.retrieve(query=query,
                                                 top_k=self.config.top_k,
                                                 rerank=self.config.rerank)
        for doc in retrieved_docs:
            logger.info(doc.model_dump(exclude='text'))
            logger.info(doc.text.strip()[:30])
        context_str = build_context(retrieved_docs)

        contents = self._build_contents(query, context_str, extra_instruction)

        resp = self.client.models.generate_content(model=self.config.model,
                                                   contents=contents)
        return {'query': query,
                'answer': resp.text,
                'contexts': [doc.model_dump() for doc in retrieved_docs]}

    def _build_contents(self, query, context_str, extra_instruction):
        query_str = rf'question: {query}'
        return '\n\n\n\n'.join([BASE_SYSTEM_PROMPT.format(domain=self.corpus,
                                                          domain_instruction=self.config.domain_instruction,
                                                          user_instruction=extra_instruction), query_str, context_str])


if __name__ == '__main__':
    rag_pipeline = RagPipeline('fastapi')
    answer = rag_pipeline.answer('How do I define a request body with Pydantic models?')
    print(answer['answer'])
