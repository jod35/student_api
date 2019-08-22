from flask import Flask ,request,jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app=Flask(__name__)
class DevConfig:
    SQLALCHEMY_DATABASE_URI='sqlite:///api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
app.config.from_object(DevConfig)

db=SQLAlchemy(app)

ma=Marshmallow(app)


#Models

class Student(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(100),unique=True,nullable=False)
    class_room=db.Column(db.String(4),nullable=False)
    description=db.Column(db.String(255),nullable=False)

    def __init__(self,name,class_room,description):
        self.name=name
        self.class_room=class_room
        self.description=description
        
    def __repr__(self,name,class_room,description):
        return '{}'.format(self.name)

class StudentSchema(ma.Schema):
    class Meta:
        fields=('id','name','class_room','description')

student_schema=StudentSchema(strict=True)
students_schema=StudentSchema(strict=True,many=True)

#create a new student
@app.route('/student',methods=['POST'])
def AddStudent():
   name=request.json['name']
   class_room=request.json['class_room']
   description=request.json['description']
   new_student=Student(name,class_room,description)

   db.session.add(new_student)
   db.session.commit()

   return student_schema.jsonify(new_student)
#fetch all students
@app.route('/getstudents',methods=['GET'])
def AllStudents():
   all_students=Student.query.all()
   result=students_schema.dump(all_students)
   return jsonify(result.data)

#get a praticular student
@app.route('/getstudent/<int:id>',methods=['GET'])
def GetAllStudents(id):
   student=Student.query.get(id)
   
   return student_schema.jsonify(student)

#update a certain student
@app.route('/student/<int:id>',methods=['PUT'])
def UpdateStudent(id):
    student=Student.query.get(id)
    name=request.json['name']
    class_room=request.json['class_room']
    description=request.json['description']
    student.name=name
    student.class_room=class_room
    student.description=description

    
    db.session.commit()
    return student_schema.jsonify(student)

#delete a student
#get a praticular student
@app.route('/deletestudent/<int:id>',methods=['DELETE'])
def DeleteAStudent(id):
   student=Student.query.get(id)
   db.session.delete(student)
   db.session.commit()
   return student_schema.jsonify(student)
if __name__ == "__main__":
    app.run(debug=True)
