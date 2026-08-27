from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.modules.users.models import AuditLog

class AuditService:
    @staticmethod
    def log(
        db: Session,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        actor_email: Optional[str] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "SUCCESS"
    ) -> AuditLog:
        log_entry = AuditLog(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            actor_id=actor_id,
            actor_email=actor_email,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            status=status
        )
        db.add(log_entry)
        db.commit()
        return log_entry

    @staticmethod
    def get_logs(db: Session, skip: int = 0, limit: int = 50, resource_type: Optional[str] = None) -> (List[AuditLog], int):
        query = db.query(AuditLog)
        if resource_type:
            query = query.filter(AuditLog.resource_type == resource_type)
        total = query.count()
        logs = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
        return logs, total
