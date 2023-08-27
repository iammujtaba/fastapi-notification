from fasnof.database import Base,SessionLocal
from sqlalchemy import Integer,String,Column
from fasnof.base_domain import BaseModelService

db = SessionLocal()

class UserNotification(Base):
    __tablename__ = "user_notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    title = Column(String(100))
    description = Column(String(500))
    tag = Column(String(50), nullable=True)
    event_name = Column(String(100), nullable=True)
    is_opened = Column(Integer, default=0)

class UserNotificationService(BaseModelService):
    def __init__(self,model=None):
        self.db = db
        self.model = model or UserNotification
        self.table_keys = self.model.__table__.columns.keys()
