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
    assert response.status_code == 200
    
    # POST
    post_datas = [
        {'title': '303_test', 'body': '303_test', 'end_time': '2024-09-12T12:12'},
        {'title': '400_test', 'end_time': '2024-09-12T12:12'},
        {'title': 'AAAAAAAAA', 'body': 'AAAAAAAAA', 'end_time': '2024-09-12T12:12'},
    ]
    for post_data in post_datas:
        response = client.post('/create', data=post_data)
        if post_data['title'] is '303_test':
            print(response)
            assert response.status_code == 303
            # assert len(response.history) == 1
            # assert response.request.path == '/'

        elif post_data['title'] is '400_test':
            assert response.status_code == 400
    

