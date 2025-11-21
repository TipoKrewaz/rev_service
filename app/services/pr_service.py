from sqlalchemy.orm import Session
from app.models.pr import PullRequest, pr_reviewers
from app.models.user import User
from app.util.assign_reviewers import get_assignable_reviewers

def reassign_reviewer(db: Session, pr_id: int, old_reviewer_id: int) -> bool:
    pr = db.query(PullRequest).filter(PullRequest.id == pr_id).first()
    if not pr or pr.status == "MERGED":
        return False

    old_reviewer = db.query(User).filter(User.id == old_reviewer_id).first()
    if not old_reviewer or not old_reviewer.team_id:
        return False

    
    candidates = get_assignable_reviewers(db, old_reviewer.team_id, pr.author_id)
    candidates = [u for u in candidates if u.id != old_reviewer_id]

    if not candidates:
        return False 

    new_reviewer = candidates[0] 


    db.execute(
        pr_reviewers.delete().where(
            (pr_reviewers.c.pr_id == pr_id) &
            (pr_reviewers.c.reviewer_id == old_reviewer_id)
        )
    )
    db.execute(
        pr_reviewers.insert().values(pr_id=pr_id, reviewer_id=new_reviewer.id)
    )
    db.commit()
    return True