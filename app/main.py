from fastapi import FastAPI
from app.api.v1 import team, user, pr
import uvicorn
app = FastAPI(title="Reviewer Assignment Service")

app.include_router(team.router, prefix="/v1/teams", tags=["teams"])
app.include_router(user.router, prefix="/v1/users", tags=["users"])
app.include_router(pr.router, prefix="/v1/pr", tags=["pull requests"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)