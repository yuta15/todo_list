import pytest
from datetime import datetime

from todo.db import get_db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<td scope="col" style="width: 10%" id="1">1</td>' in response.data
    assert b'<td scope="col" style="width: 10%" id="2">2</td>' in response.data
    assert b'<td scope="col" style="width: 10%" id="3">3</td>' not in response.data
    


def test_create(client):
    """
    create関数のテスト用
    getとpostをそれぞれテスト実施
    """
    # GET
    response = client.get('/create')
    assert b'<input type="submit" value="Register" class="btn btn-primary mt-5 shadow-sm" style="width:10rem">' in response.data
    
    # POST
    data = [
        {},
        {},
        {}
    ]
    response = client.post('/create', data={
        'title': 'pytest',
        'body': 'pytest',
        'end_time': '2024-12-12T12:12'
    })
    assert response.status_code == 200
    