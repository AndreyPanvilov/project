from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from table_Students import students
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Grad_work(Base):
    __tablename__ = "graduation_work"
    __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    mark = Column(Integer)
    id_student = Column(Integer, ForeignKey(students.student_card), name="id_student")


engine = create_engine("postgresql://postgres:1499sd9327@localhost/my_project")

if __name__ == "__main__":
    Base.metadata.create_all(engine)