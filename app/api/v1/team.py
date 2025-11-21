from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import Sessioncreating
from app.models.team import Team
from app.pydanticschemas.team import TeamCreate, TeamOut

router = APIRouter()

def get_db():
    db = Sessioncreating()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TeamOut)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == team.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team