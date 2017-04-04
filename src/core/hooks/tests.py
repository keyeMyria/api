# import json
import pytest


@pytest.mark.urls('core.hooks.urls')
def test_hooks(client):
    r = client.get('/github')
    assert r.status_code == 404           # no get, only post
    r = client.post('/_/hooks/github', {})
    assert r.status_code == 200

    r = client.post(
        '/_/hooks/travis/token',
        {},
        content_type="application/json"
    )
    assert r.status_code == 200

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
