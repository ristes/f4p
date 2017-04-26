# f4p

This project is based on a ontology from the University domain, containing relations among the following classes: faculty, study program, subject, course, grade, and user. Let us assume that the instances and the triples from this ontology are stored into multiple datasets and graphs, such that there is separate dataset for each **univ:Faculty**, and a distinct graph for each **univ:StudyProgram**.

The data from these datasets will be accessed by the following groups of requesters: 


* **Anonymous** requesters are not associated to any resource from the dataset.
* **Users** are all subjects represented with the class *univ:User*. 
* **Professors** are users that are connected with *univ:Course* through the property *univ:has_professor*.  
* **Students** are users that are connected with *univ:Course* through the property *univ:for_student*. 
* **Technical Staff** are subset of the users with *'TechStaff'* as value of their property *univ:DTYPE*. 

These groups are designed to describe the different duties described in *(Finin et al. 2008)*. The anonymous group is disjoint from all other groups, providing static separation of duty, while the Users group contains the Professors, Students, and Technical Staff groups, and thus presenting hierarchy. The professors and the students are not explicitly separated, giving a possibility for a subject to be professor and student at the same time, which is possible in real life (post-doctoral students can be professors). 
