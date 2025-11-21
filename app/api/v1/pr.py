from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import Sessioncreating
from app.models.pr import PullRequest, pr_reviewers
from app.pydanticschemas.pr import PRCreate, PRReassign, PROut
from app.util.assign_reviewers import assign_reviewers
from app.services.pr_service import reassign_reviewer

router = APIRouter()

def get_db():
    db = Sessioncreating()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PROut)
def create_pr(pr: PRCreate, db: Session = Depends(get_db)):
    db_pr = PullRequest(title=pr.title, author_id=pr.author_id, status="OPEN")
    db.add(db_pr)
    db.commit()
    db.refresh(db_pr)

    assign_reviewers(db, db_pr.id, pr.author_id)
    db_pr = db.query(PullRequest).filter(PullRequest.id == db_pr.id).first()
    return db_pr

@router.get("/", response_model=list[PROut])
def list_prs(reviewer_id: int = Query(None), db: Session = Depends(get_db)):
    query = db.query(PullRequest)
    if reviewer_id:
        query = query.join(pr_reviewers).filter(pr_reviewers.c.reviewer_id == reviewer_id)
    return query.all()

@router.patch("/{pr_id}/reassign")
def reassign_pr_reviewer(pr_id: int, reassign: PRReassign, db: Session = Depends(get_db)):
    success = reassign_reviewer(db, pr_id, reassign.old_reviewer_id)
    if not success:
        raise HTTPException(status_code=400, detail="Reassignment failed")
    return {"status": "success"}

@router.post("/{pr_id}/merge", response_model=PROut)
def merge_pr(pr_id: int, db: Session = Depends(get_db)):
    pr = db.query(PullRequest).filter(PullRequest.id == pr_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="PR not found")
    if pr.status == "OPEN":
        pr.status = "MERGED"
        db.commit()
        db.refresh(pr)
    return pr