from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel as PydanticBaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginationParams(PydanticBaseModel):
    page: int = 1
    page_size: int = 20
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams):
        total_pages = (total + params.page_size - 1) // params.page_size if params.page_size > 0 else 1
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )
