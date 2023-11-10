from fastapi import FastAPI
from pydantic import BaseModel

# modelos
class SubjectGrade(BaseModel):
    name: str
    grade: int

class Student(BaseModel):
    name: str
    alias: str
    age: int
    grades: list[SubjectGrade]

app = FastAPI(title="Students API")


@app.post("/students/grades")
def get_student_averages(students: list[Student]):
    final_grades = []
    for student in students:
        accum = sum([g.grade for g in student.grades])
        avg = accum / len(student.grades)
        final_grades.append({"name": student.name, "final": avg})
    return final_grades

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("validacion:app", reload=True)