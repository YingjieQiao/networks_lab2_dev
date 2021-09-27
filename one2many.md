

The one-to-many relationship is "multiple students for one course". 


```bash
>>> class Student(Base):
...     __tablename__ = "student"
...     id = Column(Integer, primary_key=True, index=True)
...     name = Column(String(50), unique=True, index=True)
...     email = Column(String(100), unique=True, index=True)
...     gpa = Column(Float, unique=False)
...     course_id = Column(Integer, ForeignKey('course.id'))
... 
>>> class Course(Base):
...     __tablename__ = "course"
...     id = Column(Integer, primary_key=True, index=True)
...     title = Column(String, index=True)
...     description = Column(String, index=True)
...     enrolled_students = relationship("Student", backref="course")  # student.course = xxx
... 
>>> course1 = Course()
>>> course2 = Course()
>>> course1
<__main__.Course object at 0x7f83f83ff730>
>>> course2
<__main__.Course object at 0x7f83f83ff970>
>>> 
>>> student1 = Student()
>>> student2 = Student()
>>> student1
<__main__.Student object at 0x7f83f83ffd30>
>>> student2
<__main__.Student object at 0x7f83f83ff6a0>
>>>
>>> course1.enrolled_students.append(student1)
>>> course1.enrolled_students.append(student2)
>>> course1.enrolled_students
[<__main__.Student object at 0x7f83f83ffd30>, <__main__.Student object at 0x7f83f83ff6a0>]
>>> student1.course
<__main__.Course object at 0x7f83f83ff730>
>>>
>>> student1.course = course2
>>> student1.course
<__main__.Course object at 0x7f83f83ff970>
>>> course1.enrolled_students
[<__main__.Student object at 0x7f83f83ff6a0>]
>>> course2.enrolled_students
[<__main__.Student object at 0x7f83f83ffd30>]

```