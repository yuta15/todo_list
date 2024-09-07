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
    # /createに対するGET処理
    response = client.get('/create')
    assert b'<input type="submit" value="Register" class="btn btn-primary mt-5 shadow-sm" style="width:10rem">' in response.data
    assert response.status_code == 200
    # /createに対するPOST処理
    post_datas = [
        {'title': 'accurate_data', 'body': '303_test', 'end_time': '2024-09-12T12:12'},
        {'title': 'shortage_body', 'end_time': '2024-09-12T12:12'},
        {'title': 'unowned_body', 'body': None, 'end_time': '2024-09-12T12:12'},
    ]
    for post_data in post_datas:
        response = client.post('/create', data=post_data)
        if post_data['title'] in ('accurate_data'):
            # TODOの作成処理
            assert response.status_code == 303
        elif post_data['title'] in ('shortage_body', 'unowned_body'):
            # 不足したデータ、誤ったデータの処理
            assert response.status_code == 400


def test_edit(client):
    # /1/editに対するGETメソッド
    response = client.get('/1/edit')
    assert response.status_code == 200
    # /1/editに対するPOSTメソッド
    post_datas = [
        {'title': 'change_data_value', 'body': '303_test', 'end_time': '2024-09-23T12:12'},
        {'title': 'is_completed_data', 'body': '303_test', 'end_time': '2024-09-23T12:12', 'is_state': True},
        {'title': 'shortage_endtime', 'body': '400_test'}
    ]
    for post_data in post_datas:
        if post_data['title'] is '303_test':
            # detaの変更、complete状態の変更処理
            response = client.post('/1/edit', data=post_data)
            assert response.status_code == 303
        else:
            # 不足したデータのPOST処理
            response = client.post('/1/edit', data=post_data)
            assert response.status_code == 400


def test_delete(client):
    # /editに対するGETメソッド
    response = client.get('/1/delete')
    assert b'<p>TEST-DATA1</p>' in response.data
    assert response.status_code == 200
    # /editに対するPOSTメソッド
        # 正常系テスト
    response = client.post('/1/delete', data={'id':1})
    assert response.status_code == 303
        # 存在しないデータのテスト
    response = client.post('/10/delete', data={'id':10})
    assert response.status_code == 400


def test_complete(client):
    response = client.get('/complete')
    assert response.status_code == 200