from fastapi.testclient import TestClient

from app import app, normalize_text, similarity

client = TestClient(app)


def test_health():
    assert client.get('/health').json() == {'status': 'ok'}


def test_normalize_text_removes_non_content_tags():
    title, text = normalize_text('<title>Example</title><script>bad()</script><p>Hello world</p>')
    assert title == 'Example'
    assert text == 'Hello world'


def test_similarity_empty_and_identical():
    assert similarity('', '') == 1.0
    assert similarity('one two', 'one two') == 1.0


def test_capture_rejects_non_http_urls():
    response = client.post('/api/capture', json={'url': 'ftp://example.com'})
    assert response.status_code == 400
