"""Tests for joke editing."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple

from api_tests.util import auth_token


@pytest.mark.asyncio
async def test_transcribe_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that transcribing works for an user who has not done anything previously."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["three"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['three']['_id'],
                                              'attributes': {
                                                  'actions': [
                                                      {
                                                          'transcription': {
                                                              'type': 'doc',
                                                              'content': []
                                                          }
                                                      }
                                                  ]
                                              },
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['three']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['transcriptions'][objs['users']['three']['_id']] == {
        'type': 'doc', 'content': []
    }
    assert 'final' not in joke['attributes']['transcriptions']
    assert joke['attributes']['status'] == 'auto-transcribed'
    assert len(joke['attributes']['activity']) == 1
    assert joke['attributes']['activity'][0]['action'] == 'transcribe'
    assert joke['attributes']['activity'][0]['user'] == objs['users']['three']['_id']


@pytest.mark.asyncio
async def test_fail_transcribe_previous_user_one(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that transcribing fails for a user who has extracted a joke."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/jokes/{objs["jokes"]["three"]["_id"]}',
                                 body={'type': 'jokes',
                                       'id': objs['jokes']['three']['_id'],
                                       'attributes': {
                                           'actions': [
                                               {
                                                   'transcription': {
                                                       'type': 'doc',
                                                       'content': []
                                                   }
                                               }
                                           ]
                                       },
                                       'relationships': {'source': {'data': {'type': 'sources',
                                                                             'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                 token=auth_token(objs['users']['one']))
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_fail_transcribe_previous_user_two(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that transcribing fails for a user who has verified the joke extraction."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/jokes/{objs["jokes"]["three"]["_id"]}',
                                 body={'type': 'jokes',
                                       'id': objs['jokes']['three']['_id'],
                                       'attributes': {
                                           'actions': [
                                               {
                                                   'transcription': {
                                                       'type': 'doc',
                                                       'content': []
                                                   }
                                               }
                                           ]
                                       },
                                       'relationships': {'source': {'data': {'type': 'sources',
                                                                             'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                 token=auth_token(objs['users']['two']))
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_confirm_transcription_verified_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:  # noqa: E501
    """Test that verifying the transcription works for the editor."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["four"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['four']['_id'],
                                              'attributes': {
                                                  'actions': [
                                                      {
                                                          'verified_transcription': {
                                                              'type': 'doc',
                                                              'content': {
                                                                  'type': 'paragraph',
                                                                  'content': [
                                                                      {
                                                                          'type': 'text',
                                                                          'text': 'This is a test'
                                                                      }
                                                                  ]
                                                              }
                                                          }
                                                      }
                                                  ]
                                              },
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert 'verified' in joke['attributes']['transcriptions']
    assert joke['attributes']['transcriptions']['verified'] == {
        'type': 'doc',
        'content': {
            'type': 'paragraph',
            'content': [
                {
                    'type': 'text',
                    'text': 'This is a test'
                }
            ]
        }
    }
    for action in joke['attributes']['activity']:
        assert action['action'] != 'transcription-verified' or action['user'] == objs['users']['editor']['_id']
    assert joke['attributes']['status'] == 'transcription-verified'


@pytest.mark.asyncio
async def test_fail_transcription_verified_normal_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:  # noqa: E501
    """Test that transcribing fails for a user."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/jokes/{objs["jokes"]["four"]["_id"]}',
                                 body={'type': 'jokes',
                                       'id': objs['jokes']['four']['_id'],
                                       'attributes': {
                                           'actions': [
                                               {
                                                   'verified_transcription': {
                                                       'type': 'doc',
                                                       'content': {
                                                           'type': 'paragraph',
                                                           'content': [
                                                               {
                                                                  'type': 'text',
                                                                  'text': 'This is a test'
                                                               }
                                                           ]
                                                       }
                                                   }
                                               }
                                           ]
                                       },
                                       'relationships': {'source': {'data': {'type': 'sources',
                                                                             'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                 token=auth_token(objs['users']['five']))
    assert exc_info.value.code == 400
