"""Create test data

Revision ID: 553ba4edc9ce
Revises: cc8e6fbfe8d7
Create Date: 2024-09-29 17:27:57.162369

"""

from datetime import datetime
from typing import Sequence, Union

from faker import Faker
from ksuid import Ksuid
from sqlalchemy.engine import reflection

from alembic import context, op

# revision identifiers, used by Alembic.
revision: str = "553ba4edc9ce"
down_revision: Union[str, None] = "cc8e6fbfe8d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Get the dialect name from the Alembic context
db_dialect = context.get_context().dialect.name


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    for _ in range(1, 35):
        id: str = str(Ksuid())
        name: str = Faker().first_name()
        surname: str = Faker().last_name()
        email: str = Faker().email()
        identification_number: str = Faker().numerify(text="##########")
        created_by: str = "FAKE"
        # created_at: str = datetime.now().isoformat()
        created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if db_dialect == "mysql":
            query = (
                f"INSERT INTO persons (id, `name`, surname, email, identification_number, created_by, created_at, updated_by, updated_at) "
                f"VALUES('{id}', '{name}', '{surname}', '{email}', '{identification_number}', '{created_by}', '{created_at}', '{created_by}', '{created_at}');"
            )
        elif db_dialect == "postgresql":
            query = (
                f'INSERT INTO public.persons (id, "name", surname, email, identification_number, created_by, created_at, updated_by, updated_at) '
                f"VALUES('{id}', '{name}', '{surname}', '{email}', '{identification_number}', '{created_by}', '{created_at}', '{created_by}', '{created_at}');"
            )
        else:
            raise ValueError(f"Unsupported database dialect: {db_dialect}")

        op.execute(query)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DELETE FROM persons;")
    # ### end Alembic commands ###
