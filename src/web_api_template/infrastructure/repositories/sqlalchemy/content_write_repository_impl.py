from typing import List, Optional

from automapper import mapper
from sqlalchemy import delete, desc, select, text, update
from sqlalchemy.exc import IntegrityError

from web_api_template.core.logging import logger
from web_api_template.core.repository.exceptions import ItemNotFoundException
from web_api_template.core.repository.manager.sqlalchemy.database import Database
from web_api_template.domain.entities import Content, ContentCreate, ContentFilter
from web_api_template.domain.repository import ContentWriteRepository
from web_api_template.infrastructure.models.sqlalchemy import ContentModel


class ContentWriteRepositoryImpl(ContentWriteRepository):
    """Repository implementation for Content"""

    async def create(
        self,
        *,
        # current_user: User,
        entity: ContentCreate,
    ) -> Content:
        """
        Create a content on DB

        Args:
            entity (content): content to create
        Returns:
            content (content): content created
        """

        entity_model: ContentModel = mapper.to(ContentModel).map(entity)

        # set_concurrency_fields(source=entity_model, user=current_user)
        # entity_model.owner_id = str(current_user.id)

        async with Database.get_db_session(self._label) as session:
            try:
                session.add(entity_model)
                await session.commit()
                await session.refresh(entity_model)
            # except IntegrityError as ie:
            #     await session.rollback()
            #     logger.exception("Integrity exception")
            #     error_info: str = str(ie.orig)
            #     detail_message: str = error_info
            #     detail_index = error_info.find("DETAIL:")
            #     if detail_index != -1:
            #         detail_message = error_info[detail_index + len("DETAIL:") :].strip()
            #     raise DuplicatedSlugException(detail_message)
            except Exception as ex:
                logger.exception("Commit error")
                raise ex

            return mapper.to(Content).map(entity_model)

    async def __get_by_id(self, id: str) -> ContentModel | None:
        """Get content model by ID

        Args:
            id (str): _description_

        Returns:
            ContentModel: _description_
        """
        async with Database.get_db_session(self._label) as session:
            try:
                result = await session.execute(
                    select(ContentModel).where(ContentModel.id == id)
                )
                return result.scalar_one_or_none()

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def __delete(self, id: str) -> None:
        """Delete content model by ID

        Args:
            id (str): _description_

        Returns:
            None

        """
        async with Database.get_db_session(self._label) as session:
            try:
                delete_query = delete(ContentModel).where(ContentModel.id == id)
                await session.execute(delete_query)
                await session.commit()
                return

            except Exception as ex:
                logger.exception("Database error")
                raise ex

    async def delete(self, id: str) -> None:
        """Delete content by id

        Args:
            request (Request): request (from fastAPI)
            id: str

        Returns:
            None
        """

        try:
            entity_model: Optional[ContentModel] = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if content is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            # Delete the given (and existing) id
            await self.__delete(id)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    async def __update(self, id: str, model: ContentModel) -> Optional[ContentModel]:
        """update content model with the given ID

        Args:
            id (str): _description_

        Returns:
            ContentModel

        """

        # TODO: concurrency fields
        # model.updated_at = datetime.utcnow()
        # model.updated_by = "fake"

        async with Database.get_db_session(self._label) as session:
            try:
                # Vuild the update query
                update_query = (
                    update(ContentModel)
                    .where(ContentModel.id == id)
                    .values(
                        content_number=model.content_number,
                        person_id=model.person_id,
                        status=model.status,
                    )
                )

                await session.execute(update_query)
                await session.commit()

                return await self.__get_by_id(id)

            except Exception as ex:
                await session.rollback()
                logger.exception("Database error")
                raise ex

    async def update(
        self,
        *,
        id: str,
        content: Content,
        # current_user: User
    ) -> Optional[Content]:
        """
        Update content into DB
        Args:
            id (str): Template ID used to update
            content (Content): Content that will be updated
        Returns:
            Content: Content updated
        """

        try:
            entity_model: Optional[ContentModel] = await self.__get_by_id(id)

            if not entity_model:
                # TODO : check if content is in delete status
                logger.debug("Item with id: {} not found", id)
                raise ItemNotFoundException(f"Item with id: {id} not found")

            new_model: ContentModel = mapper.to(ContentModel).map(content)

            # Update the given (and existing) id
            result: Optional[ContentModel] = await self.__update(id=id, model=new_model)

            return mapper.to(Content).map(result)

        except Exception as ex:
            logger.exception("Database error")
            raise ex

    # async def count_Policies(self) -> int:
    #     with DbConnectionManager() as manager:
    #         search_db: int = (
    #             manager.session.query(ContentModel)
    #             .filter(ContentModel.deleted == False)
    #             .count()
    #         )

    #         return search_db
