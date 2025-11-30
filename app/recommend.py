
from app.monitoring import RECOMMEND_REQ, SERVICE
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import hashlib, os
from elasticsearch import Elasticsearch

router = APIRouter()
ES_URL = os.getenv('ES_URL', 'http://localhost:9200')
INDEX = os.getenv('ES_INDEX', 'books')

class Query(BaseModel):
    text: str
    k: int = 5

def get_embedding(text: str):
    h = hashlib.sha256(text.encode('utf-8')).digest()
    vec = []
    seed = h
    while len(vec) < 384:
        seed = hashlib.sha256(seed).digest()
        for b in seed:
            vec.append((b / 255.0) * 2 - 1)
            if len(vec) >= 384:
                break
    arr = np.array(vec, dtype=float)
    norm = np.linalg.norm(arr)
    if norm == 0:
        return arr.tolist()
    return (arr / norm).tolist()

@router.post('/recommend')
async def recommend(q: Query):
    if not q.text:
        raise HTTPException(400, 'text required')
    emb = get_embedding(q.text)
    es = Elasticsearch(ES_URL)
    body = {
        "size": q.k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": emb}
                }
            }
        }
    }
    res = es.search(index=INDEX, body=body)
    hits = res.get('hits', {}).get('hits', [])
    results = []
    for h in hits:
        src = h.get('_source', {})
        score = h.get('_score')
        results.append({'id': h.get('_id'), 'score': score, 'source': src})
    return {'ok': True, 'results': results}
