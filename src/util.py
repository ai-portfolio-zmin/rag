from typing import List
from src.retrieval.schema import RetrievedDoc


def build_context(docs: List[RetrievedDoc]) -> str:
    """
    todo: title, section, source might not always be avaiable, sth to think about
    :param docs:
    :return:
    """
    documents = []
    for i, doc in enumerate(docs, 1):
        documents.append('\n'.join([f'[{i}] {doc.title} ({doc.section})',
                                    f'source: {doc.source}',
                                    doc.text]))
    documents_joined = '\n\n-----------\n'.join(documents)
    return '\n'.join(['Context:', documents_joined])
