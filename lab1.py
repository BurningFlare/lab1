import csv
import time
import base64
from statistics import median

#student class
#stores student information
class Student:
    def __init__(self, email_address, first_name, last_name, course_id, grade, marks):
        self.email_address = email_address
        self.FirstName = first_name
        self.LastName = last_name
        self.course_id = course_id
        self.Grades = grade
        self.marks = marks

    def display_records(self):
        print(f"Email: {self.email_address}")
        print(f"Name: {self.FirstName} {self.LastName}")
        print(f"Course ID: {self.course_id}")
        print(f"Grade: {self.Grades}")
        print(f"Marks: {self.marks}")
        print("-" * 40)
    
    def to_dict(self):
        return {
            'Email_address': self.email_address,
            'First_name': self.FirstName,
            'Last_name': self.LastName,
            'Course.id': self.course_id,
            'grades': self.Grades,
            'Marks': str(self.marks)
        }

#course class
#stores course information
class Course:
    def __init__(self, course_id, course_name, credits=3, description=""):
        self.Course_id = course_id
        self.Course_name = course_name
        self.Credits = credits
        self.Description = description
    
    def display_courses(self):
        print(f"Course ID: {self.Course_id}")
        print(f"Course Name: {self.Course_name}")
        print(f"Credits: {self.Credits}")
        print(f"Description: {self.Description}")
        print("-" * 40)
    
    def to_dict(self):
        return {
            'Course_id': self.Course_id,
            'Course_name': self.Course_name,
            'Credits': str(self.Credits),
            'Description': self.Description
        }


#professor class
#stores professor information
class Professor:
    def __init__(self, professor_id, name, email_address, rank, course_id):
        self.Professor_id = professor_id
        self.Name = name
        self.email_address = email_address
        self.Rank = rank
        self.course_id = course_id
    
    def professors_details(self):
        print(f"Professor ID: {self.Professor_id}")
        print(f"Name: {self.Name}")
        print(f"Email: {self.email_address}")
        print(f"Rank: {self.Rank}")
        print(f"Course ID: {self.course_id}")
        print("-" * 40)
    
    def to_dict(self):
        return {
            'Professor_id': self.Professor_id,
            'Professor Name': self.Name,
            'email_address': self.email_address,
            'Rank': self.Rank,
            'Course.id': self.course_id
        }


#grades class
#stores grades information
class Grades:
    def __init__(self, grade_id, grade, marks_range):
        self.Grade_id = grade_id
        self.Grade = grade
        self.Marks_range = marks_range
    
    def display_grade_report(self):
        print(f"Grade ID: {self.Grade_id}")
        print(f"Grade: {self.Grade}")
        print(f"Marks Range: {self.Marks_range}")
        print("-" * 40)
    
    def to_dict(self):
        return {
            'Grade_id': self.Grade_id,
            'Grade': self.Grade,
            'Marks range': self.Marks_range
        }


#login user class
#stores login user information
class LoginUser:
    def __init__(self, email_id, password, role="student"):
        self.Email_id = email_id
        self.password = password
        self.role = role
    
    def encrypt_password(self, password):
        """Encrypt password using base64 encoding"""
        return base64.b64encode(password.encode()).decode()
    
    def decrypt_password(self, encrypted_password):
        """Decrypt password from base64"""
        try:
            return base64.b64decode(encrypted_password.encode()).decode()
        except:
            return ""
    
    def Login(self, email_id, password):
        return self.Email_id == email_id and self.decrypt_password(self.password) == password
    
    def Logout(self):
        print(f"User {self.Email_id} logged out successfully.")
    
    def Change_password(self, old_password, new_password):
        if self.decrypt_password(self.password) == old_password:
            self.password = self.encrypt_password(new_password)
            return True
        return False
    
    def to_dict(self):
        return {
            'User_id': self.Email_id,
            'Password': self.password,
            'Role': self.role
        }


#student manager class
#manages student information
class StudentManager:
    def __init__(self, csv_file="students.csv"):
        self.csv_file = csv_file
        self.students = []
        self.load_students()
    
    def load_students(self):
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student = Student(
                        row['Email_address'],
                        row['First_name'],
                        row['Last_name'],
                        row['Course.id'],
                        row['grades'],
                        float(row['Marks'])
                    )
                    self.students.append(student)
        except FileNotFoundError:
            self.create_csv_file()
        except Exception as e:
            print(f"Error loading students: {e}")
    
    def create_csv_file(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Email_address', 'First_name', 'Last_name', 'Course.id', 'grades', 'Marks'])
            writer.writeheader()
    
    def save_students(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['Email_address', 'First_name', 'Last_name', 'Course.id', 'grades', 'Marks']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students:
                    writer.writerow(student.to_dict())
            return True
        except Exception as e:
            print(f"Error saving students: {e}")
            return False
    
    def add_new_student(self, email_address, first_name, last_name, course_id, grade, marks):
        if not email_address or not email_address.strip():
            print("Error: Student email cannot be empty!")
            return False
        
        if any(s.email_address == email_address for s in self.students):
            print(f"Student with email {email_address} already exists!")
            return False
        
        student = Student(email_address, first_name, last_name, course_id, grade, marks)
        self.students.append(student)
        return self.save_students()
    
    def delete_new_student(self, email_address):
        original_count = len(self.students)
        self.students = [s for s in self.students if s.email_address != email_address]
        if len(self.students) < original_count:
            return self.save_students()
        print(f"Student with email {email_address} not found!")
        return False
    
    def update_student_record(self, email_address, **kwargs):
        student = next((s for s in self.students if s.email_address == email_address), None)
        if not student:
            print(f"Student with email {email_address} not found!")
            return False
        
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        
        return self.save_students()
    
    def check_my_grades(self, email_address):
        student = next((s for s in self.students if s.email_address == email_address), None)
        if student:
            student.display_records()
            return student
        print(f"Student with email {email_address} not found!")
        return None
    
    def check_my_marks(self, email_address):
        student = next((s for s in self.students if s.email_address == email_address), None)
        if student:
            print(f"Marks for {student.FirstName} {student.LastName}: {student.marks}")
            return student.marks
        print(f"Student with email {email_address} not found!")
        return None
    
    def search_students(self, search_term, field='email_address'):
        start_time = time.time()
        results = []
        for student in self.students:
            value = getattr(student, field, "")
            if search_term.lower() in str(value).lower():
                results.append(student)
        end_time = time.time()
        search_time = (end_time - start_time) * 1000  # Convert to milliseconds
        print(f"Search completed in {search_time:.4f} milliseconds")
        return results, search_time
    
    def sort_students_by_name(self):
        student_list = self.students.copy()
        student_list.sort(key=lambda x: x.FirstName)
        return student_list
    
    def sort_students_by_marks(self):
        student_list = self.students.copy()
        student_list.sort(key=lambda x: x.marks, reverse=True)
        return student_list
    
    def get_average_score(self, course_id=None):
        student_list = self.students
        if course_id:
            student_list = [s for s in student_list if s.course_id == course_id]
        
        if not student_list:
            return 0
        
        total = sum(s.marks for s in student_list)
        return total / len(student_list)
    
    def get_median_score(self, course_id=None):
        student_list = self.students
        if course_id:
            student_list = [s for s in student_list if s.course_id == course_id]
        
        if not student_list:
            return 0
        
        marks_list = [s.marks for s in student_list]
        return median(marks_list)
    
    def display_all_students(self):
        for student in self.students:
            student.display_records()


#course manager class
#manages course information
class CourseManager:
    def __init__(self, csv_file="courses.csv"):
        self.csv_file = csv_file
        self.courses = []
        self.load_courses()
    
    def load_courses(self):
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course = Course(
                        row['Course_id'],
                        row['Course_name'],
                        int(row.get('Credits', 3)),
                        row.get('Description', '')
                    )
                    self.courses.append(course)
        except FileNotFoundError:
            self.create_csv_file()
        except Exception as e:
            print(f"Error loading courses: {e}")
    
    def create_csv_file(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Course_id', 'Course_name', 'Credits', 'Description'])
            writer.writeheader()
    
    def save_courses(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['Course_id', 'Course_name', 'Credits', 'Description']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for course in self.courses:
                    writer.writerow(course.to_dict())
            return True
        except Exception as e:
            print(f"Error saving courses: {e}")
            return False
    
    def add_new_course(self, course_id, course_name, credits=3, description=""):
        if not course_id or not course_id.strip():
            print("Error: Course ID cannot be empty!")
            return False
        
        if any(c.Course_id == course_id for c in self.courses):
            print(f"Course with ID {course_id} already exists!")
            return False
        
        course = Course(course_id, course_name, credits, description)
        self.courses.append(course)
        return self.save_courses()
    
    def delete_new_course(self, course_id):
        original_count = len(self.courses)
        self.courses = [c for c in self.courses if c.Course_id != course_id]
        if len(self.courses) < original_count:
            return self.save_courses()
        print(f"Course with ID {course_id} not found!")
        return False
    
    def modify_course(self, course_id, **kwargs):
        course = next((c for c in self.courses if c.Course_id == course_id), None)
        if not course:
            print(f"Course with ID {course_id} not found!")
            return False
        
        for key, value in kwargs.items():
            if hasattr(course, key):
                setattr(course, key, value)
        
        return self.save_courses()
    
    def display_courses(self):
        for course in self.courses:
            course.display_courses()
    
    def get_course_by_id(self, course_id):
        return next((c for c in self.courses if c.Course_id == course_id), None)


#professor manager class
#manages professor information
class ProfessorManager:
    def __init__(self, csv_file="professors.csv"):
        self.csv_file = csv_file
        self.professors = []
        self.load_professors()
    
    def load_professors(self):
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    professor = Professor(
                        row['Professor_id'],
                        row['Professor Name'],
                        row['email_address'],
                        row['Rank'],
                        row['Course.id']
                    )
                    self.professors.append(professor)
        except FileNotFoundError:
            self.create_csv_file()
        except Exception as e:
            print(f"Error loading professors: {e}")
    
    def create_csv_file(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Professor_id', 'Professor Name', 'email_address', 'Rank', 'Course.id'])
            writer.writeheader()
    
    def save_professors(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['Professor_id', 'Professor Name', 'email_address', 'Rank', 'Course.id']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for professor in self.professors:
                    writer.writerow(professor.to_dict())
            return True
        except Exception as e:
            print(f"Error saving professors: {e}")
            return False
    
    def add_new_professor(self, professor_id, name, email_address, rank, course_id):
        if not professor_id or not professor_id.strip():
            print("Error: Professor ID cannot be empty!")
            return False
        
        if any(p.Professor_id == professor_id for p in self.professors):
            print(f"Professor with ID {professor_id} already exists!")
            return False
        
        professor = Professor(professor_id, name, email_address, rank, course_id)
        self.professors.append(professor)
        return self.save_professors()
    
    def delete_professore(self, professor_id):
        original_count = len(self.professors)
        self.professors = [p for p in self.professors if p.Professor_id != professor_id]
        if len(self.professors) < original_count:
            return self.save_professors()
        print(f"Professor with ID {professor_id} not found!")
        return False
    
    def modify_professor_details(self, professor_id, **kwargs):
        professor = next((p for p in self.professors if p.Professor_id == professor_id), None)
        if not professor:
            print(f"Professor with ID {professor_id} not found!")
            return False
        
        for key, value in kwargs.items():
            if hasattr(professor, key):
                setattr(professor, key, value)
        
        return self.save_professors()
    
    def show_course_details_by_professor(self, professor_id):
        professor = next((p for p in self.professors if p.Professor_id == professor_id), None)
        if professor:
            print(f"Professor: {professor.Name}")
            print(f"Course ID: {professor.course_id}")
            return professor.course_id
        print(f"Professor with ID {professor_id} not found!")
        return None


#login manager class
#manages login user information
class LoginManager:
    def __init__(self, csv_file="login.csv"):
        self.csv_file = csv_file
        self.users = []
        self.load_users()
    
    def load_users(self):
        try:
            with open(self.csv_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user = LoginUser(row['User_id'], row['Password'], row.get('Role', 'student'))
                    self.users.append(user)
        except FileNotFoundError:
            self.create_csv_file()
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def create_csv_file(self):
        with open(self.csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['User_id', 'Password', 'Role'])
            writer.writeheader()
    
    def save_users(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                fieldnames = ['User_id', 'Password', 'Role']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for user in self.users:
                    writer.writerow(user.to_dict())
            return True
        except Exception as e:
            print(f"Error saving users: {e}")
            return False
    
    def register_user(self, email_id, password, role="student"):
        if any(u.Email_id == email_id for u in self.users):
            print(f"User with email {email_id} already exists!")
            return False
        
        user = LoginUser(email_id, "", role)
        user.password = user.encrypt_password(password)
        self.users.append(user)
        return self.save_users()
    
    def login(self, email_id, password):
        user = next((u for u in self.users if u.Email_id == email_id), None)
        if user and user.Login(email_id, password):
            print(f"Login successful! Welcome {email_id}")
            return user
        print("Invalid email or password!")
        return None
    
    def change_password(self, email_id, old_password, new_password):
        user = next((u for u in self.users if u.Email_id == email_id), None)
        if user and user.Change_password(old_password, new_password):
            return self.save_users()
        print("Failed to change password. Check your old password.")
        return False


#report generator class
#generates reports
class ReportGenerator:
    def __init__(self, student_manager, course_manager, professor_manager):
        self.student_manager = student_manager
        self.course_manager = course_manager
        self.professor_manager = professor_manager
    
    def generate_course_wise_report(self, course_id):
        print(f"\n=== Course-wise Report for {course_id} ===")
        course = self.course_manager.get_course_by_id(course_id)
        if course:
            course.display_courses()
        
        students = [s for s in self.student_manager.students if s.course_id == course_id]
        print(f"\nTotal Students: {len(students)}")
        if students:
            print("\nStudent Details:")
            for student in students:
                student.display_records()
            
            avg_score = self.student_manager.get_average_score(course_id)
            median_score = self.student_manager.get_median_score(course_id)
            print(f"\nAverage Score: {avg_score:.2f}")
            print(f"Median Score: {median_score:.2f}")
        else:
            print("No students enrolled in this course.")
    
    def generate_professor_wise_report(self, professor_id):
        print(f"\n=== Professor-wise Report ===")
        professor = next((p for p in self.professor_manager.professors if p.Professor_id == professor_id), None)
        if professor:
            professor.professors_details()
            course_id = professor.course_id
            self.generate_course_wise_report(course_id)
        else:
            print(f"Professor with ID {professor_id} not found!")
    
    def generate_student_wise_report(self, email_address):
        print(f"\n=== Student-wise Report ===")
        student = next((s for s in self.student_manager.students if s.email_address == email_address), None)
        if student:
            student.display_records()
            course = self.course_manager.get_course_by_id(student.course_id)
            if course:
                print("\nCourse Details:")
                course.display_courses()
        else:
            print(f"Student with email {email_address} not found!")


#main checkmygrade application class
#manages the application
class CheckMyGradeApp:
    def __init__(self):
        self.student_manager = StudentManager()
        self.course_manager = CourseManager()
        self.professor_manager = ProfessorManager()
        self.login_manager = LoginManager()
        self.report_generator = ReportGenerator(
            self.student_manager,
            self.course_manager,
            self.professor_manager
        )
        self.current_user = None
    

    
    def display_menu(self):
        print("\n" + "="*50)
        print("CheckMyGrade Application")
        print("="*50)
        print("1. Login")
        print("2. Register")
        print("3. Add Student")
        print("4. Delete Student")
        print("5. Update Student Record")
        print("6. View Student Grades")
        print("7. Search Students")
        print("8. Sort Students (by Name)")
        print("9. Sort Students (by Marks)")
        print("10. Add Course")
        print("11. Delete Course")
        print("12. Modify Course")
        print("13. Add Professor")
        print("14. Delete Professor")
        print("15. Modify Professor")
        print("16. Generate Course-wise Report")
        print("17. Generate Professor-wise Report")
        print("18. Generate Student-wise Report")
        print("19. Get Statistics (Average/Median)")
        print("20. Display All Students")
        print("21. Display All Courses")
        print("22. Change Password")
        print("23. Logout")
        print("0. Exit")
        print("="*50)
    
    def run(self):
        print("Welcome to CheckMyGrade Application!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == "0":
                print("Thank you for using CheckMyGrade Application!")
                break
            elif choice == "1":
                email = input("Enter email: ").strip()
                password = input("Enter password: ").strip()
                self.current_user = self.login_manager.login(email, password)
            elif choice == "2":
                email = input("Enter email: ").strip()
                password = input("Enter password: ").strip()
                role = input("Enter role (student/professor): ").strip() or "student"
                self.login_manager.register_user(email, password, role)
            elif choice == "3":
                email = input("Enter email: ").strip()
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()
                course_id = input("Enter course ID: ").strip()
                grade = input("Enter grade: ").strip()
                marks = float(input("Enter marks: ").strip())
                self.student_manager.add_new_student(email, first_name, last_name, course_id, grade, marks)
            elif choice == "4":
                email = input("Enter student email to delete: ").strip()
                self.student_manager.delete_new_student(email)
            elif choice == "5":
                email = input("Enter student email: ").strip()
                print("Enter new values (press Enter to skip):")
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                course_id = input("Course ID: ").strip()
                grade = input("Grade: ").strip()
                marks = input("Marks: ").strip()
                kwargs = {}
                if first_name:
                    kwargs['FirstName'] = first_name
                if last_name:
                    kwargs['LastName'] = last_name
                if course_id:
                    kwargs['course_id'] = course_id
                if grade:
                    kwargs['Grades'] = grade
                if marks:
                    kwargs['marks'] = float(marks)
                self.student_manager.update_student_record(email, **kwargs)
            elif choice == "6":
                email = input("Enter student email: ").strip()
                self.student_manager.check_my_grades(email)
            elif choice == "7":
                search_term = input("Enter search term: ").strip()
                field = input("Search by field (email_address/FirstName/LastName/course_id) [default: email_address]: ").strip() or "email_address"
                results, search_time = self.student_manager.search_students(search_term, field)
                print(f"\nFound {len(results)} results:")
                for student in results:
                    student.display_records()
            elif choice == "8":
                sorted_students = self.student_manager.sort_students_by_name()
                print("\nStudents sorted by name:")
                for student in sorted_students:
                    student.display_records()
            elif choice == "9":
                sorted_students = self.student_manager.sort_students_by_marks()
                print("\nStudents sorted by marks (descending):")
                for student in sorted_students:
                    student.display_records()
            elif choice == "10":
                course_id = input("Enter course ID: ").strip()
                course_name = input("Enter course name: ").strip()
                credits = input("Enter credits [default: 3]: ").strip()
                credits = int(credits) if credits else 3
                description = input("Enter description: ").strip()
                self.course_manager.add_new_course(course_id, course_name, credits, description)
            elif choice == "11":
                course_id = input("Enter course ID to delete: ").strip()
                self.course_manager.delete_new_course(course_id)
            elif choice == "12":
                course_id = input("Enter course ID: ").strip()
                course_name = input("New course name (press Enter to skip): ").strip()
                credits = input("New credits (press Enter to skip): ").strip()
                description = input("New description (press Enter to skip): ").strip()
                kwargs = {}
                if course_name:
                    kwargs['Course_name'] = course_name
                if credits:
                    kwargs['Credits'] = int(credits)
                if description:
                    kwargs['Description'] = description
                self.course_manager.modify_course(course_id, **kwargs)
            elif choice == "13":
                email = input("Enter professor email: ").strip()
                name = input("Enter professor name: ").strip()
                rank = input("Enter rank: ").strip()
                course_id = input("Enter course ID: ").strip()
                self.professor_manager.add_new_professor(email, name, email, rank, course_id)
            elif choice == "14":
                professor_id = input("Enter professor email to delete: ").strip()
                self.professor_manager.delete_professore(professor_id)
            elif choice == "15":
                professor_id = input("Enter professor email: ").strip()
                name = input("New name (press Enter to skip): ").strip()
                email = input("New email (press Enter to skip): ").strip()
                rank = input("New rank (press Enter to skip): ").strip()
                course_id = input("New course ID (press Enter to skip): ").strip()
                kwargs = {}
                if name:
                    kwargs['Name'] = name
                if email:
                    kwargs['email_address'] = email
                if rank:
                    kwargs['Rank'] = rank
                if course_id:
                    kwargs['course_id'] = course_id
                self.professor_manager.modify_professor_details(professor_id, **kwargs)
            elif choice == "16":
                course_id = input("Enter course ID: ").strip()
                self.report_generator.generate_course_wise_report(course_id)
            elif choice == "17":
                professor_id = input("Enter professor email: ").strip()
                self.report_generator.generate_professor_wise_report(professor_id)
            elif choice == "18":
                email = input("Enter student email: ").strip()
                self.report_generator.generate_student_wise_report(email)
            elif choice == "19":
                course_id = input("Enter course ID (press Enter for all courses): ").strip()
                course_id = course_id if course_id else None
                avg = self.student_manager.get_average_score(course_id)
                med = self.student_manager.get_median_score(course_id)
                scope = f"for course {course_id}" if course_id else "for all courses"
                print(f"\nStatistics {scope}:")
                print(f"Average Score: {avg:.2f}")
                print(f"Median Score: {med:.2f}")
            elif choice == "20":
                self.student_manager.display_all_students()
            elif choice == "21":
                self.course_manager.display_courses()
            elif choice == "22":
                email = input("Enter email: ").strip()
                old_password = input("Enter old password: ").strip()
                new_password = input("Enter new password: ").strip()
                self.login_manager.change_password(email, old_password, new_password)
            elif choice == "23":
                if self.current_user:
                    self.current_user.Logout()
                    self.current_user = None
                else:
                    print("No user logged in.")
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    app = CheckMyGradeApp()
    app.run()
    