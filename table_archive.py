from database import Base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy import create_engine


class archive(Base):
    __tablename__ = "archive"
    __table_args__ = {"schema": "public"}
    name = Column(String)
    student_card = Column(Integer, primary_key=True)
    year_of_admission = Column(Date)
    stage_of_education = Column(String)
    year_of_graduation = Column(Date)
    department_name = Column(String)
    graduated_work_name = Column(String)
    graduated_work_mark = Column(String)



engine = create_engine("postgresql://postgres:1499sd9327@localhost/my_project")

if __name__ == "__main__":
    Base.metadata.create_all(engine)
