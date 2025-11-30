import click, os, json
from elasticsearch import Elasticsearch, helpers
from app.recommend import get_embedding

ES_URL = os.getenv('ES_URL', 'http://localhost:9200')
INDEX = os.getenv('ES_INDEX', 'books')

@click.command()
def reindex():
    es = Elasticsearch(ES_URL)
    if es.indices.exists(INDEX):
        click.echo(f"Deleting index {INDEX}")
        es.indices.delete(index=INDEX)
    mapping = {
        'mappings': {
            'properties': {
                'title': {'type':'text'},
                'author': {'type':'keyword'},
                'embedding': {'type':'dense_vector', 'dims': 384},
                'copies_available': {'type':'integer'}
            }
        }
    }
    es.indices.create(index=INDEX, body=mapping)
    click.echo('Index created. Now indexing sample documents...')
    sample_books = [
        {'id': '1', 'title': 'Python Darslari', 'author': 'Ali', 'copies_available': 3},
        {'id': '2', 'title': 'FastAPI Guide', 'author': 'Bob', 'copies_available': 2},
        {'id': '3', 'title': "Ma'lumotlar bazasi", 'author': 'Karim', 'copies_available': 5},
    ]
    actions = []
    for b in sample_books:
        emb = get_embedding(b['title'] + ' ' + b['author'])
        actions.append({
            '_op_type': 'index',
            '_index': INDEX,
            '_id': b['id'],
            '_source': {**b, 'embedding': emb}
        })
    helpers.bulk(es, actions)
    click.echo('Indexed sample books.')
if __name__ == '__main__':
    reindex()
