"Testing some hooks (actually not yet)"
# import json
# import pytest
# import urllib


# Github
def test_github(client, db):
    # Github
    r = client.get('/_/hooks/github')
    assert r.status_code == 405           # no get, only post
    r = client.post('/_/hooks/github', {})
    assert r.status_code == 200


# Travis
def test_travis(client, db):
    # malformed data
    r = client.post(
        '/_/hooks/travis',
        {},
        content_type="application/json"
    )
    assert r.status_code == 400

    # correct data
    # r = client.post(
    #     '/_/hooks/travis',
    #     urllib.parse.urlencode({'payload': '{}'}),
    #     content_type="application/x-www-form-urlencoded"
    #     # {'payload': ['asd']},
    #     # content_type="application/json"
    # )
    # assert r.content == '200'
    # assert r.status_code == 200

    # r = client.post(
    #     '/telegram/token',
    #     json.dumps({
    #         'message': {
    #             'text': '',
    #             'chat': {
    #                 'id': 123
    #             }
    #         }
    #     }),
    #     content_type="application/json")
    # assert r.status_code == 200
