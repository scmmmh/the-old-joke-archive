"""API Handlers."""
from .frontend import FrontendHandler  # noqa
from .user import UserCollectionHandler, UserItemHandler, LoginHandler, ResetPasswordHandler  # noqa
from .source import SourceCollectionHandler, SourceItemHandler  # noqa
from .joke import JokeCollectionHandler, JokeItemHandler, JokeDataHandler, html_injector as joke_html_injector  # noqa
from .explore import SearchHandler, SearchExactCountsHandler, SuggestionHandler  # noqa
from .admin import AdminSearchHandler  # noqa
