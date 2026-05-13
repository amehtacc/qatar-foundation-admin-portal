from extensions import db
from datetime import datetime


class Opportunity(db.Model):

    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)

    duration = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    skills = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(100), nullable=False)

    future_opportunities = db.Column(db.Text, nullable=False)

    prerequisites = db.Column(db.Text)

    max_applicants = db.Column(db.Integer)

    admin_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "start_date": self.start_date,
            "description": self.description,
            "skills": self.skills,
            "category": self.category,
            "future_opportunities": self.future_opportunities,
            "prerequisites": self.prerequisites,
            "max_applicants": self.max_applicants,
            "admin_id": self.admin_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }