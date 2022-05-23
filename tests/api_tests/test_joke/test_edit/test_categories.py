"""Tests for joke editing."""
import json
import pytest

from aiocouch import CouchDB
from typing import Tuple

from api_tests.util import auth_token


@pytest.mark.asyncio
async def test_verify_categories_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:  # noqa: E501
    """Test that verifying the categories works for a general user."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["five"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['five']['_id'],
                                              'attributes': {
                                                  'actions': [
                                                      {
                                                          'categories': [
                                                              'test',
                                                              'example',
                                                          ]
                                                      }
                                                  ]
                                              },
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['four']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['categories'] == ['test', 'example']
    assert joke['attributes']['status'] == 'categories-verified'
    for action in joke['attributes']['activity']:
        assert action['action'] != 'categories-verified' or action['user'] == objs['users']['four']['_id']
