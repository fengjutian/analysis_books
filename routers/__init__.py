from .users import router as users_router
from .companies import router as companies_router
from .books import router as books_router
from .author import router as author_router
from .book2author import router as book2author_router
from .school import router as school_router
from .author2school import router as author2school_router

all_routers = [
    users_router,
    companies_router,
    books_router,
    author_router,
    book2author_router,
    school_router,
    author2school_router
]
