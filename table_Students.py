from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from table_Department import Department
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class students(Base):
    __tablename__ = "students"
    __table_args__ = {"schema": "public"}
    name = Column(String)
    student_card = Column(Integer, primary_key=True)
    year_of_admission = Column(Date)
    stage_of_education = Column(String)
    year_of_graduation = Column(Date)
    indicator = Column(String)
    id_department = Column(Integer, ForeignKey(Department.id), name='id_department')

    department = relationship(Department)



engine = create_engine("postgresql://postgres:1499sd9327@localhost/my_project")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
