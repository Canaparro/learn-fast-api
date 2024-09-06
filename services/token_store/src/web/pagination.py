from typing import Annotated

from fastapi import Depends


class Pagination:
    def __init__(self, page: int = 0, size: int = 10) -> None:
        self.page = page
        self.size = size


PaginationDep = Annotated[Pagination, Depends(Pagination)]
