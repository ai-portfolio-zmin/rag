from fastapi import FastAPI
from pydantic import BaseModel
from src.pipeline import RagPipeline
from functools import lru_cache
from src.config import CONFIGS

app = FastAPI(title='RAG system')


@lru_cache(10)
def get_rag_pipeline(corpus):
    if corpus not in CONFIGS.keys():
        raise ValueError(f'please enter a valid corpus')
    return RagPipeline(corpus=corpus)


class RagInput(BaseModel):
    corpus: str
    query: str
    extra_instruction: str = ''


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/answer')
def answer(payload: RagInput):
    rag_pipeline = get_rag_pipeline(payload.corpus)
    answer = rag_pipeline.answer(query=payload.query,
                                 extra_instruction=payload.extra_instruction)
    return answer
