from fastapi import FastApi
from app.api.v1 import team, user, pr

app = FastApi(title="Reviewer Assignment Service")

app.include_router(team.router, prefix="/v1/teams", tags=["teams"])
app.include_router(user.router, prefix="/v1/users", tags=["users"])
app.include_router(pr.router, prefix="/v1/pr", tags=["pull requests"])
""