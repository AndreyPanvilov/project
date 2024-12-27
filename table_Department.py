from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine


class Department(Base):
    __tablename__ = "department"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    head_name = Column(String)


engine = create_engine("postgresql://postgres:1499sd9327@localhost/my_project")

if __name__ == "__main__":
    Base.metadata.create_all(engine)