from .comments import router as comment_router
from .notes import router as note_router

routers = [note_router, comment_router]
