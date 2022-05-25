"""Tests for joke editing."""
import json
import pytest

from aiocouch import CouchDB
from typing import Tuple

from api_tests.util import auth_token


@pytest.mark.asyncio
async def test_annotate_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:  # noqa: E501
    """Test that annotating the text works for a user."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["six"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['six']['_id'],
                                              'attributes': {
                                                  'actions': [
                                                      {
                                                          'annotated': {
                                                              'type': 'doc',
                                                              'content': [
                                                                  {
                                                                      'type': 'paragraph',
                                                                      'content': [
                                                                          {
                                                                              'type': 'text',
                                                                              'text': 'This is a '
                                                                          },
                                                                          {
                                                                              'type': 'text',
                                                                              'text': 'joke',
                                                                              'marks': [
                                                                                  {
                                                                                      'type': 'annotation',
                                                                                      'attrs': {
                                                                                          'test': 'test'
                                                                                      }
                                                                                  }
                                                                              ]
                                                                          },
                                                                          {
                                                                              'type': 'text',
                                                                              'text': '!'
                                                                          }
                                                                      ]
                                                                  }
                                                              ]
                                                          }
                                                      }
                                                  ]
                                              },
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['six']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert objs['users']['six']['_id'] in joke['attributes']['transcriptions']
    assert joke['attributes']['transcriptions'][objs['users']['six']['_id']] == {
        'type': 'doc',
        'content': [
            {
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': 'This is a '
                    },
                    {
                        'type': 'text',
                        'text': 'joke',
                        'marks': [
                            {
                                'type': 'annotation',
                                'attrs': {
                                    'test': 'test'
                                }
                            }
                        ]
                    },
                    {
                        'type': 'text',
                        'text': '!'
                    }
                ]
            }
        ]
    }
    assert joke['attributes']['status'] == 'categories-verified'
    assert len(joke['attributes']['activity']) == 1


@pytest.mark.asyncio
async def test_annotate_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that transcribing works for an editor."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["three"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['three']['_id'],
                                              'attributes': {
                                                  'actions': [
                                                      {
                                                          'annotated': {
                                                              'type': 'doc',
                                                              'content': [
                                                                  {
                                                                      'type': 'paragraph',
                                                                      'content': [
                                                                          {
                                                                              'type': 'text',
                                                                              'text': 'This is a '
                                                                          },
                                                                          {
                                                                              'type': 'text',
                                                                              'text': 'joke',
                                                                              'marks': [
                                                                                  {
                                                                                      'type': 'annotation',
                                                                                      'attrs': {
                                                                                          'test': 'test'
                                                                                      }
                                                                                  }
                                                                              ]
                                                                          },
                                                                          {
                                                                              'type': 'text',
                                                                              'text': '!'
                                                                          }
                                                                      ]
                                                                  }
                                                              ]
                                                          }
                                                      },
                                                      {
                                                          'status': 'annotated'
                                                      }
                                                  ]
                                              },
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['transcriptions'][objs['users']['editor']['_id']] == {
        'type': 'doc',
        'content': [
            {
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': 'This is a '
                    },
                    {
                        'type': 'text',
                        'text': 'joke',
                        'marks': [
                            {
                                'type': 'annotation',
                                'attrs': {
                                    'test': 'test'
                                }
                            }
                        ]
                    },
                    {
                        'type': 'text',
                        'text': '!'
                    }
                ]
            }
        ]
    }
    assert joke['attributes']['transcriptions']['annotated'] == {
        'type': 'doc',
        'content': [
            {
                'type': 'paragraph',
                'content': [
                    {
                        'type': 'text',
                        'text': 'This is a '
                    },
                    {
                        'type': 'text',
                        'text': 'joke',
                        'marks': [
                            {
                                'type': 'annotation',
                                'attrs': {
                                    'test': 'test'
                                }
                            }
                        ]
                    },
                    {
                        'type': 'text',
                        'text': '!'
                    }
                ]
            }
        ]
    }
    assert joke['attributes']['status'] == 'annotated'
    assert len(joke['attributes']['activity']) == 4
