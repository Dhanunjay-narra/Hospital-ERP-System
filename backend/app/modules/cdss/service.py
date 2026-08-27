from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.modules.cdss.models import CDSSRule, CDSSAlertLog
from app.modules.cdss.schemas import CDSSRuleCreate, CDSSAlertCreate
from app.core.exceptions import NotFoundError

class CDSSService:
    @staticmethod
    def get_rules(db: Session) -> List[CDSSRule]:
        return db.query(CDSSRule).all()

    @staticmethod
    def create_rule(db: Session, rule_in: CDSSRuleCreate) -> CDSSRule:
        existing = db.query(CDSSRule).filter(CDSSRule.rule_code == rule_in.rule_code).first()
        if existing:
            return existing
        rule = CDSSRule(**rule_in.model_dump())
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule

    @staticmethod
    def get_alerts(db: Session, skip: int = 0, limit: int = 20) -> Tuple[List[CDSSAlertLog], int]:
        total = db.query(CDSSAlertLog).count()
        alerts = db.query(CDSSAlertLog).order_by(CDSSAlertLog.triggered_at.desc()).offset(skip).limit(limit).all()
        return alerts, total

    @staticmethod
    def log_alert(db: Session, alert_in: CDSSAlertCreate, created_by: Optional[str] = None) -> CDSSAlertLog:
        alert = CDSSAlertLog(**alert_in.model_dump(), created_by=created_by)
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
