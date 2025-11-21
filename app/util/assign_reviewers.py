import random
from typing import List
from sqlalchemy.orm import Session
from app.models.user import User

def get_assignable_reviewers(db: Session, team_id: int, author_id: int) -> List[User]:
    return (
        db.query(User)
        .filter(
            User.team_id == team_id,
            User.id != author_id,
            User.is_active == True
        )
        .all()
    )

def assign_reviewers(db: Session, pr_id: int, author_id: int) -> List[int]:
    from app.models.user import User
    from app.models.pr import pr_reviewers

    author = db.query(User).filter(User.id == author_id).first()
    if not author or not author.team_id:
        return []

    candidates = get_assignable_reviewers(db, author.team_id, author_id)
    random.shuffle(candidates)
    selected = candidates[:2]

    reviewer_ids = [u.id for u in selected]
    if reviewer_ids:
        values = [{"pr_id": pr_id, "reviewer_id": rid} for rid in reviewer_ids]
        db.execute(pr_reviewers.insert(), values)
        db.commit()

    return reviewer_ids