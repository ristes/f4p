from z3 import *
import os
import platform
import datetime
import sys

#code for cleaning the terminal so you always get fresh one
if platform.system().lower() == 'windows':
	os.system('cls') #for window
else:
	os.system('clear') #for Linux

printTactic = False

if "printt" in map(str.lower, sys.argv):
	printTactic = True



#z3 solver settings
set_option(rational_to_decimal=True)

#declare the goal where we insert the assertions i.e. requirements
goal = Goal()
solver = Then('smt','simplify', 'qe').solver()
solver.set('unsat_core', True)
solver.set('mbqi', True)
solver.set('mbqi.max_iterations', 10000)
solver.set('pull_nested_quantifiers', True)

_user = Int("user")
_grade = Int("grade")
_course = Int("course")
_student = Int("_student")
_professor = Int("_professor")

USER = 1
PROFESSOR = 2
STUDENT = 3
COURSE = 4


#resolves the type for the user, 1: basic user, 2 profa, 3 student
dType = Function("dType", IntSort(), IntSort())

#predicate that checks wheter a given professor is resposnsible for a given course
#first param is professor, second course
isResponsible = Function("isResponsible", IntSort(), IntSort(), BoolSort())

#predicate that checks wheter a given student is taking a given course
#first param is student, second course
isEnrolledInCourse = Function("isEnrolledInCourse", IntSort(), IntSort(), BoolSort())

#this predicate returns a grade that a given student has for a given course; 
#first param is student, second course
returnGradeStudentCourse = Function("returnGradeStudentCourse", IntSort(), IntSort(), IntSort())

gradeStudentCourse = Function("gradeStudentCourse", IntSort(), IntSort(), IntSort(), IntSort(), BoolSort())

#grade, student 
gradeForCourse = Function("gradeForCourse", IntSort(), IntSort(), BoolSort())
#grade, course 
gradeForStudent = Function("gradeForStudent", IntSort(), IntSort(), BoolSort())
gradeValue = Function("gradeValue", IntSort(), IntSort())

#forbit being resposible and student in a same time
disjointProfessorStudent = ForAll([_user, _course], Implies(isResponsible(_user, _course) == True,isEnrolledInCourse(_user, _course) == False))
solver.assert_and_track(disjointProfessorStudent, "disjointProfessorStudent")

gradeValidRange = ForAll([_student, _course], And(returnGradeStudentCourse(_student, _course) > 4,  returnGradeStudentCourse(_student, _course) < 11))
solver.assert_and_track(gradeValidRange, "gradeValidRange")

gradeStudent = ForAll([_professor, _student, _course, _grade], 
                      Implies(gradeStudentCourse(_professor, _student, _course, _grade) == True, And(isResponsible(_professor, _course) == True, isEnrolledInCourse(_student, _course) == True, gradeForCourse(_grade, _student) == True, gradeForCourse(_grade, _course) == True, gradeValue(_grade) >= 5, gradeValue(_grade) <= 10
                          )
                      )
                )
solver.assert_and_track(gradeStudent, "gradeStudent")

#from here we start definition of policy
studentAccessOwnGrades = Function("studentAccessOwnGrades", IntSort(), IntSort(), BoolSort())

studentAccessOwnGradesRule = ForAll([_student, _course, _grade], Implies(studentAccessOwnGrades(_student, _grade) == True, And(isEnrolledInCourse(_student, _course) == True, gradeForCourse(_grade, _course)))) 
solver.assert_and_track(studentAccessOwnGradesRule, "studentAccessOwnGradesRule")

professorAccessOwnGrades = Function("professorAccessOwnGrades", IntSort(), IntSort(), BoolSort())

professorAccessOwnGradesRule = ForAll([_professor, _course, _grade], Implies(professorAccessOwnGrades(_professor, _grade) == True, And(isResponsible(_professor, _course) == True, gradeForCourse(_grade, _course)))) 
solver.assert_and_track(professorAccessOwnGradesRule, "professorAccessOwnGradesRule")

brakePolicyOne = Exists([_professor, _student, _course, _grade], And(isEnrolledInCourse(_student, _course) == True, gradeStudentCourse(_student, _student, _course, _grade)))
solver.assert_and_track(brakePolicyOne, "brakePolicyOne")


begining = datetime.datetime.now()
print ("Checking started at: %s\n" % begining)
verd = solver.check()
print "Checking satisfiability: {}\n".format(verd)
if verd == sat:
	print "Printing the model:"
	print solver.model()
if verd == unsat:
	print "The following predicates are not consistent:"
	print solver.unsat_core()
end = datetime.datetime.now()
duration = end - begining
print ("Checking completed at: {}\nIt took {}".format(end, duration))
#print all the tactics in z3py
#print describe_tactics()