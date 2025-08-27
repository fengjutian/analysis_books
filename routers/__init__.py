from .users import router as users_router
from .companies import router as companies_router

all_routers = [
    users_router,
    companies_router,
]
