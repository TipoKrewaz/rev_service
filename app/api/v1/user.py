from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import Sessioncreating
from app.models.user import User
from app.models.team import Team
from app.pydanticschemas.user import UserCreate, UserOut

router = APIRouter()

def get_db():
    db = Sessioncreating()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_team = db.query(Team).filter(Team.name == user.team_name).first()
    if not db_team:
        raise HTTPException(status_code=400, detail="Team not found")

    db_user = db.query(User).filter(User.name == user.name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(name=user.name, team_id=db_team.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"status": "deactivated"}