from .users import router as users_router
from .companies import router as companies_router
from .books import router as books_router

all_routers = [
    users_router,
    companies_router,
    books_router,
]
