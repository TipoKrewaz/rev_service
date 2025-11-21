from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

pr_reviewers = Table(
    "pr_reviewers",
    Base.metadata,
    Column("pr_id", Integer, ForeignKey("pull_requests.id"), primary_key=True),
    Column("reviewer_id", Integer, ForeignKey("users.id"), primary_key=True),
)

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum( "OPEN", "MERGED", name="pr_status"), default="OPEN", nullable=False)

    author = relationship("User", foreign_keys=[author_id])
    reviewers = relationship("User", secondary=pr_reviewers, back_populates="reviewed_prs")