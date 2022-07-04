"""Handlers supporting the exploration of the jokes."""
import logging

from .base import BaseHandler
from .joke import as_jsonapi
from ...utils import meilisearch
from ...validation import validate


logger = logging.getLogger(__name__)
QUERY_SCHEMA = {
    'query': {
        'type': 'string',
        'default': '',
    },
    'facets': {
        'type': 'dict',
        'empty': False,
        'default': {},
        'schema': {
            'categories': {
                'type': 'dict',
                'default': {},
            },
            'topics': {
                'type': 'dict',
                'default': {},
            },
            'publisher': {
                'type': 'dict',
                'default': {},
            },
            'publication': {
                'type': 'dict',
                'default': {},
            },
            'section': {
                'type': 'dict',
                'default': {},
            },
            'year': {
                'type': 'dict',
                'default': {},
            },
            'language': {
                'type': 'dict',
                'default': {},
            },
        }
    }
}


class SearchBase(BaseHandler):
    """Base class for search requests."""

    def construct_query(self: 'SearchBase') -> dict:
        """Construct a Meilisearch query based on the request body."""
        params = validate(QUERY_SCHEMA, self.json_body(), purge_unknown=True)
        facets = []
        for facet_name in ['categories', 'topics', 'language', 'publisher', 'publication', 'section', 'year']:
            if facet_name in params['facets']:
                facets.append(' OR '.join([f'{facet_name}="{value}"'
                                           for value, selected in params['facets'][facet_name].items()
                                           if selected]))
        filters = ' AND '.join([f'({facet})' for facet in facets if facet])
        return {
            'q': params['query'],
            'facetsDistribution': ['*'],
            'filter': filters if filters else '',
        }


class SearchHandler(SearchBase):
    """Handler for the main search API endpoint."""

    async def post(self: 'SearchHandler') -> None:
        """Handle a search request."""
        try:
            results = await meilisearch().search('jokes', self.construct_query())
            user = await self.get_user()
            jokes = [await as_jsonapi({'_id': joke['id']}, user)
                     for joke in results['hits']]
            self.write({
                    'data': jokes,
                    'meta': {
                        'total': results['nbHits'],
                        'facets': results['facetsDistribution'],
                    }
                })
        except Exception as e:
            logger.error(e)
            self.send_error(400)


class SearchExactCountsHandler(SearchBase):
    """Handler for the exact counts API endpoint.

    This does an exhaustive count of both results and facets.
    """

    async def post(self: 'SearchExactCountsHandler') -> None:
        """Return an exhaustive count of results and facets."""
        try:
            query = self.construct_query()
            results = await meilisearch().search('jokes', query)
            query['offset'] = 0
            query['limit'] = results['nbHits']
            results = await meilisearch().search('jokes', query)
            self.write({
                'data': 'ok',
                'meta': {
                    'total': results['nbHits'],
                    'facets': results['facetsDistribution']
                }
            })
        except Exception as e:
            logger.error(e)
            self.send_error(400)
