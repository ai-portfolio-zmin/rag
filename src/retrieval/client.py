from src.retrieval.schema import RetrievedDoc
import requests
from typing import List

class HybridRetriever:

    def __init__(self,
                 base_url: str,
                 corpus: str,
                 default_top_k: int = 10,
                 timeout: float = 10):
        self.base_url = base_url
        self.corpus = corpus
        self.default_top_k = default_top_k
        self.timeout = timeout

    def retrieve(self,
                       query: str,
                       top_k: int = None,
                       rerank: bool = True) -> List[RetrievedDoc]:
        url = f'{self.base_url}/retrieve'
        payload = {'corpus': self.corpus,
                   'query': query,
                   'top_k': self.default_top_k if top_k is None else top_k,
                   'rerank': rerank}

        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

        docs: list[RetrievedDoc] = []
        for d in data:
            d['text'] = d['contents']
            d.pop('contents')
            docs.append(RetrievedDoc(**d))

        return docs


def main():
    hr = HybridRetriever(r'http://localhost:8001',
                         'fastapi')
    x = hr.retrieve('How do I define a request body with Pydantic models?')
    return x


if __name__ == '__main__':
    result = main()
    print(result)
