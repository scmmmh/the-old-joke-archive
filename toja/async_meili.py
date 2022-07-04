"""An asyncio-compatible Meilisearch client."""
import asyncio
import json
import logging

from tornado.httpclient import AsyncHTTPClient, HTTPClientError
from typing import Union, List


logger = logging.getLogger(__name__)


class AsyncMeiliClient(object):
    """An asyncio-compatible Meilisearch client."""

    def __init__(self: 'AsyncMeiliClient', host: str, auth_token: Union[str, None] = None) -> None:
        """Initialise the :class:`~async_meili.AsyncMeiliClient`.

        :param host: The host that the Meilisearch server is reachable at
        :type host: str
        :param auth_token: The optional authentication token to use
        :type auth_token: str
        """
        self._host = host
        self._headers = [('Content-Type', 'application/json')]
        if auth_token:
            self._headers.append(('Authorization', f'Bearer {auth_token}'))
        self._client = AsyncHTTPClient()

    async def wait_for_task(self: 'AsyncMeiliClient', task_id: str) -> dict:
        """Wait for the Meilisearch task with the given ``task_id`` to complete.

        This uses a polling-with-backoff strategy starting at a 0.1 second backoff and doubling that until it reaches
        a maximum of 5 second backoff.

        :param task_id: The id of the task to wait for
        :type task_id: str
        :return: The task details when the task completes
        :return_type: dict
        """
        result = await self.send_request('GET', f'/tasks/{task_id}')
        backoff = 0.1
        while result['status'] not in ['succeeded', 'failed']:
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 5)
            result = await self.send_request('GET', f'/tasks/{task_id}')
        if result['status'] == 'succeeded':
            return result['details']

    async def send_request(self: 'AsyncMeiliClient', method: str, path: str, body: Union[dict, None] = None, sync: bool = False) -> Union[dict, None]:  # noqa: 501
        """Send a request to the Meilisearch server.

        :param method: The HTTP method to use for sending the request
        :type method: str
        :param path: The path to send the request to
        :type path: str
        :param body: An optional body to send with the request
        :type body: dict
        :param sync: Whether to wait for the operation to complete even if it is asynchronous
                     (:class:`~async_meili.AsyncMeiliClient.wait_for_task`)
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        try:
            response = await self._client.fetch(f'{self._host}{path}',
                                                method=method,
                                                headers=self._headers,
                                                body=json.dumps(body) if body else None)
            if response.code == 200:
                return json.loads(response.body)
            elif response.code == 201:
                return json.loads(response.body)
            elif response.code == 202:
                if sync:
                    return await self.wait_for_task(json.loads(response.body)['uid'])
                else:
                    return json.loads(response.body)
            elif response.code == 204:
                return None
            elif response.code == 205:
                return None
        except HTTPClientError as e:
            logger.error(e)

    async def create_index(self: 'AsyncMeiliClient', uid: str, primaryKey: str, sync: bool = False) -> Union[dict, None]:  # noqa: E501
        """Create an index.

        :param uid: The unique id of the index to create
        :type uid: str
        :param primaryKey: The name of the primary key field
        :type primaryKey: str
        :param sync: Whether to wait for the operation to complete
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        return await self.send_request('POST', '/indexes', body={'uid': uid, 'primaryKey': primaryKey}, sync=sync)

    async def delete_index(self: 'AsyncMeiliClient', uid: str, sync: bool = False) -> Union[dict, None]:
        """Delete an index.

        :param uid: The unique id of the index to delete
        :type uid: str
        :param sync: Whether to wait for the operation to complete
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        return await self.send_request('DELETE', f'/indexes/{uid}', sync=sync)

    async def update_index_settings(self: 'AsyncMeiliClient', uid: str, settings: dict, sync: bool = False) -> Union[dict, None]:  # noqa: E501
        """Update the settings of an index.

        :param uid: The unique id of the index to delete
        :type uid: str
        :param settings: The new settings object
        :type settings: dict
        :param sync: Whether to wait for the operation to complete
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        return await self.send_request('POST', f'/indexes/{uid}/settings', settings, sync=sync)

    async def index_documents(self: 'AsyncMeiliClient', index: str, doc: List[dict], sync: bool = False) -> Union[dict, None]:  # noqa: E501
        """Index a document.

        :param index: The unique id of the index to add the document to
        :type index: str
        :param doc: The list of documents to index
        :type doc: list
        :param sync: Whether to wait for the operation to complete
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        return await self.send_request('POST', f'/indexes/{index}/documents', doc, sync=sync)

    async def index_document(self: 'AsyncMeiliClient', index: str, doc: List[dict], sync: bool = False) -> Union[dict, None]:  # noqa: E501
        """Index a document.

        :param index: The unique id of the index to add the document to
        :type index: str
        :param doc: The document to index
        :type doc: dict
        :param sync: Whether to wait for the operation to complete
        :type sync: bool
        :return: The response from the server, if one is sent
        :return_type: dict or None
        """
        return await self.index_documents(index, [doc], sync=sync)

    async def search(self: 'AsyncMeiliClient', index: str, query: dict) -> dict:
        """Run a search query.

        :param index: The unique id of the index to search
        :type index: str
        :param query: The query to send
        :type query: dict
        :return: The query response
        :return_type: dict
        """
        return await self.send_request('POST', f'/indexes/{index}/search', query, sync=False)
