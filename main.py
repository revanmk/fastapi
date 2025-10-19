from controllers import user_controller, post_controller,oauth_controller,vote_controller
from fastapi import FastAPI

app = FastAPI()
app.include_router(user_controller.router)
app.include_router(post_controller.router)
app.include_router(oauth_controller.router)
app.include_router(vote_controller.router)
