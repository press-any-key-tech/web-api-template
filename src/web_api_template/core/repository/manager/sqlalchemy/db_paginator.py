import math
from typing import Any
from uuid import UUID

from sqlalchemy import asc, desc, func, or_
from sqlalchemy.orm import Query, Session

from web_api_template.core.logging import logger


class DbPaginator:
    """Database paginator (for SQLALchemy)

    Returns:
        _type_: _description_
    """

    _session: Session
    _model: Any
    _query: Query

    def __init__(self, session: Session):
        self._session = session

    def list(
        self,
        *,
        model: Any,
        filter_by: dict = {},
        order_by: list = [],
        page: int = 1,
        size: int = 10,
    ) -> dict:
        """Makes pagination query and returns a paginated object
        TODO: Change return parameter to an object

        Args:
            model (Any, optional): SQLAlchemy model.
            filter_by (dict, optional): Dictionary with field, value to filter on (uses AND). Defaults to {}.
            order_by (list, optional): Array with sorting columns (- desc, nothing asc). Defaults to [].
            page (int, optional): Page number. Defaults to 1.
            size (int, optional): Page size. Defaults to 10.

        Returns:
            dict: _description_
        """
        items: list[model] = []
        self._model = model
        self._query = self._session.query(model)

        self._filter(filter_by)
        self._sort(order_by)

        # Get number of elements
        count: int = self._query.distinct().count()

        # Calculate offset and limit
        # Pages, round up

        pages: int = 0 if count == 0 else int(math.ceil(count / size))

        if count > 0:
            # If requested page > page set the last page
            if page > pages:
                page = pages

            offset = (page - 1) * size

            items = self._query.distinct().offset(offset).limit(size).all()

        # Build the return object
        return {"total": count, "pages": pages, "page": page, "items": items}

    def _filter(self, filter_by: dict = {}):
        """Builds the filter object for SQLAlchemy

        Args:
            model (Any): _description_
            filter_by (dict, optional): _description_. Defaults to {}.

        Returns:
            list: _description_
        """
        logger.debug(filter_by)
        # Add filter deleted
        self._query = self._query.filter(getattr(self._model, "deleted").is_not(True))

        for key, value in filter_by.items():
            if type(value) == str:
                self._query = self._query.filter(
                    getattr(self._model, key).ilike(f"%{value}%")
                )
            elif type(value) == int or type(value) == UUID:
                column: Any = getattr(self._model, key, None)
                self._query = self._query.filter(getattr(self._model, key) == value)

    def _sort(self, order_by: list = []):
        """Builds the sort object for SQLAlchemy

        Args:
            order_by (dict, optional): _description_. Defaults to {}.

        Returns:
            list: _description_
        """

        # Improved to sort by the main object and ignore joins
        for sort_column in order_by:
            self._query = self._query.order_by(
                desc(getattr(self._model, sort_column[1:]))
                if sort_column[:1] == "-"
                else asc(getattr(self._model, sort_column))
            )
