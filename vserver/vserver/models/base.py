from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
import inflect
import stringcase

p = inflect.engine()


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Auto generate __tablename__ from class name
    @declared_attr
    def __tablename__(cls) -> str:
        return stringcase.snakecase(p.plural(cls.__name__))
