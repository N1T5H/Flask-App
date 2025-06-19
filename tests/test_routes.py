def test_add_quote(client):
    response = client.post('/quote', json={'text': 'Stay hungry, stay foolish.'})
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Quote added successfully'

def test_get_quote(client):
    # Add a quote first
    client.post('/quote', json={'text': 'Be yourself; everyone else is already taken.'})
    response = client.get('/quote')
    assert response.status_code == 200
    data = response.get_json()
    assert 'quote' in data
