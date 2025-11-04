import unittest
import csv
import os
import time
from lab1 import (
    Student, Course, Professor, LoginUser,
    StudentManager, CourseManager, ProfessorManager, LoginManager,
    ReportGenerator
)


class TestStudentManager(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "test_students.csv"
        self.student_manager = StudentManager(self.test_csv)
    
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_add_student(self):
        result = self.student_manager.add_new_student(
            "test@example.com", "John", "Doe", "CS101", "A", 95.5
        )
        self.assertTrue(result)
        self.assertEqual(len(self.student_manager.students), 1)
        
        result = self.student_manager.add_new_student(
            "test@example.com", "Jane", "Smith", "CS102", "B", 85.0
        )
        self.assertFalse(result)
        self.assertEqual(len(self.student_manager.students), 1)
    
    def test_delete_student(self):
        self.student_manager.add_new_student(
            "delete@example.com", "Delete", "Me", "CS101", "A", 90.0
        )
        self.assertEqual(len(self.student_manager.students), 1)
        
        result = self.student_manager.delete_new_student("delete@example.com")
        self.assertTrue(result)
        self.assertEqual(len(self.student_manager.students), 0)
        
        result = self.student_manager.delete_new_student("nonexistent@example.com")
        self.assertFalse(result)
    
    def test_update_student(self):
        self.student_manager.add_new_student(
            "update@example.com", "Update", "Me", "CS101", "B", 85.0
        )
        
        result = self.student_manager.update_student_record(
            "update@example.com", 
            FirstName="Updated",
            Grades="A",
            marks=95.0
        )
        self.assertTrue(result)
        
        student = next(s for s in self.student_manager.students if s.email_address == "update@example.com")
        self.assertEqual(student.FirstName, "Updated")
        self.assertEqual(student.Grades, "A")
        self.assertEqual(student.marks, 95.0)
    
    def test_search_students(self):
        for i in range(100):
            self.student_manager.add_new_student(
                f"student{i}@example.com",
                f"First{i}",
                f"Last{i}",
                "CS101",
                "A",
                90.0 + i % 10
            )
        
        start_time = time.time()
        results, search_time = self.student_manager.search_students("student50", "email_address")
        end_time = time.time()
        
        self.assertEqual(len(results), 1)
        self.assertGreater(search_time, 0)
        search_time_seconds = search_time / 1000
        print(f"\nsearch time for 100 records: {search_time_seconds:.6f} seconds")
    
    def test_sort_students_by_marks(self):
        self.student_manager.add_new_student("a@test.com", "Alice", "Smith", "CS101", "B", 85)
        self.student_manager.add_new_student("b@test.com", "Bob", "Johnson", "CS101", "A", 92)
        self.student_manager.add_new_student("c@test.com", "Charlie", "Brown", "CS101", "A", 90)
        
        start_time = time.time()
        sorted_students = self.student_manager.sort_students_by_marks()
        end_time = time.time()
        
        self.assertEqual(sorted_students[0].marks, 92)
        self.assertEqual(sorted_students[1].marks, 90)
        self.assertEqual(sorted_students[2].marks, 85)
        
        sort_time = end_time - start_time
        print(f"\nsort by marks time: {sort_time:.6f} seconds")
    
    def test_sort_students_by_email(self):
        self.student_manager.add_new_student("c@test.com", "Charlie", "Brown", "CS101", "A", 90)
        self.student_manager.add_new_student("a@test.com", "Alice", "Smith", "CS101", "B", 85)
        self.student_manager.add_new_student("b@test.com", "Bob", "Johnson", "CS101", "A", 92)
        
        start_time = time.time()
        sorted_students = sorted(self.student_manager.students, key=lambda x: x.email_address)
        end_time = time.time()
        
        self.assertEqual(sorted_students[0].email_address, "a@test.com")
        self.assertEqual(sorted_students[1].email_address, "b@test.com")
        self.assertEqual(sorted_students[2].email_address, "c@test.com")
        
        sort_time = end_time - start_time
        print(f"\nsort by email time: {sort_time:.6f} seconds")
    
    def test_get_statistics(self):
        self.student_manager.add_new_student("a@test.com", "Alice", "Smith", "CS101", "A", 90)
        self.student_manager.add_new_student("b@test.com", "Bob", "Johnson", "CS101", "B", 80)
        self.student_manager.add_new_student("c@test.com", "Charlie", "Brown", "CS101", "C", 70)
        
        avg = self.student_manager.get_average_score()
        median_score = self.student_manager.get_median_score()
        
        self.assertEqual(avg, 80.0)
        self.assertEqual(median_score, 80)


class TestCourseManager(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "test_courses.csv"
        self.course_manager = CourseManager(self.test_csv)
    
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_add_course(self):
        result = self.course_manager.add_new_course(
            "CS101", "Introduction to Computer Science", 3, "Basic CS course"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.course_manager.courses), 1)
        
        result = self.course_manager.add_new_course(
            "CS101", "Duplicate Course", 3, "Should fail"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.course_manager.courses), 1)
    
    def test_delete_course(self):
        self.course_manager.add_new_course("CS101", "Test Course", 3, "Test")
        self.assertEqual(len(self.course_manager.courses), 1)
        
        result = self.course_manager.delete_new_course("CS101")
        self.assertTrue(result)
        self.assertEqual(len(self.course_manager.courses), 0)
        
        result = self.course_manager.delete_new_course("CS999")
        self.assertFalse(result)
    
    def test_modify_course(self):
        self.course_manager.add_new_course("CS101", "Original Name", 3, "Original")
        
        result = self.course_manager.modify_course(
            "CS101",
            Course_name="Updated Name",
            Credits=4,
            Description="Updated description"
        )
        self.assertTrue(result)
        
        course = self.course_manager.get_course_by_id("CS101")
        self.assertEqual(course.Course_name, "Updated Name")
        self.assertEqual(course.Credits, 4)
        self.assertEqual(course.Description, "Updated description")
    
    def test_get_course_by_id(self):
        self.course_manager.add_new_course("CS101", "Test Course", 3, "Test")
        
        course = self.course_manager.get_course_by_id("CS101")
        self.assertIsNotNone(course)
        self.assertEqual(course.Course_id, "CS101")
        
        course = self.course_manager.get_course_by_id("CS999")
        self.assertIsNone(course)


class TestProfessorManager(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "test_professors.csv"
        self.professor_manager = ProfessorManager(self.test_csv)
    
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_add_professor(self):
        result = self.professor_manager.add_new_professor(
            "prof1@university.edu",
            "Dr. John Smith",
            "prof1@university.edu",
            "Associate Professor",
            "CS101"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.professor_manager.professors), 1)
        
        result = self.professor_manager.add_new_professor(
            "prof1@university.edu",
            "Dr. Jane Doe",
            "prof1@university.edu",
            "Professor",
            "CS102"
        )
        self.assertFalse(result)
        self.assertEqual(len(self.professor_manager.professors), 1)
    
    def test_delete_professor(self):
        self.professor_manager.add_new_professor(
            "prof1@university.edu",
            "Dr. Delete Me",
            "prof1@university.edu",
            "Professor",
            "CS101"
        )
        self.assertEqual(len(self.professor_manager.professors), 1)
        
        result = self.professor_manager.delete_professore("prof1@university.edu")
        self.assertTrue(result)
        self.assertEqual(len(self.professor_manager.professors), 0)
        
        result = self.professor_manager.delete_professore("nonexistent@university.edu")
        self.assertFalse(result)
    
    def test_modify_professor(self):
        self.professor_manager.add_new_professor(
            "prof1@university.edu",
            "Dr. Original Name",
            "prof1@university.edu",
            "Assistant Professor",
            "CS101"
        )
        
        result = self.professor_manager.modify_professor_details(
            "prof1@university.edu",
            Name="Dr. Updated Name",
            Rank="Associate Professor",
            course_id="CS102"
        )
        self.assertTrue(result)
        
        professor = next(p for p in self.professor_manager.professors 
                        if p.Professor_id == "prof1@university.edu")
        self.assertEqual(professor.Name, "Dr. Updated Name")
        self.assertEqual(professor.Rank, "Associate Professor")
        self.assertEqual(professor.course_id, "CS102")


class TestLargeDataset(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "test_large_students.csv"
        self.student_manager = StudentManager(self.test_csv)
        
        print("\ngenerating 1000 student records...")
        start_time = time.time()
        for i in range(1000):
            self.student_manager.add_new_student(
                f"student{i:04d}@university.edu",
                f"FirstName{i}",
                f"LastName{i}",
                f"CS{100 + (i % 10)}",
                self._get_grade(90 - (i % 50)),
                90 - (i % 50)
            )
        end_time = time.time()
        print(f"time to add 1000 records: {(end_time - start_time):.4f} seconds")
    
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def _get_grade(self, marks):
        if marks >= 90:
            return "A"
        elif marks >= 80:
            return "B"
        elif marks >= 70:
            return "C"
        elif marks >= 60:
            return "D"
        else:
            return "F"
    
    def test_load_large_dataset(self):
        self.student_manager.save_students()
        
        start_time = time.time()
        new_manager = StudentManager(self.test_csv)
        end_time = time.time()
        
        self.assertEqual(len(new_manager.students), 1000)
        load_time = end_time - start_time
        print(f"\ntime to load 1000 records from csv: {load_time:.6f} seconds")
    
    def test_search_large_dataset(self):
        start_time = time.time()
        results, search_time = self.student_manager.search_students("student0500", "email_address")
        end_time = time.time()
        
        self.assertEqual(len(results), 1)
        search_time_seconds = search_time / 1000
        print(f"\nsearch time for 1000 records (specific): {search_time_seconds:.6f} seconds")
        
        start_time = time.time()
        results, search_time = self.student_manager.search_students("FirstName5", "FirstName")
        end_time = time.time()
        
        self.assertGreater(len(results), 1)
        search_time_seconds = search_time / 1000
        print(f"search time for 1000 records (pattern): {search_time_seconds:.6f} seconds")
    
    def test_sort_large_dataset_by_marks(self):
        start_time = time.time()
        sorted_students = self.student_manager.sort_students_by_marks()
        end_time = time.time()
        
        self.assertEqual(len(sorted_students), 1000)
        self.assertGreaterEqual(sorted_students[0].marks, sorted_students[1].marks)
        
        sort_time = end_time - start_time
        print(f"time to sort 1000 records by marks (descending): {sort_time:.6f} seconds")
    
    def test_sort_ascending_by_email(self):
        start_time = time.time()
        sorted_students = sorted(self.student_manager.students, key=lambda x: x.email_address)
        end_time = time.time()
        
        self.assertEqual(len(sorted_students), 1000)
        self.assertLessEqual(sorted_students[0].email_address, sorted_students[1].email_address)
        
        sort_time = end_time - start_time
        print(f"time to sort 1000 records by email (ascending): {sort_time:.6f} seconds")
    
    def test_delete_from_large_dataset(self):
        initial_count = len(self.student_manager.students)
        
        start_time = time.time()
        result = self.student_manager.delete_new_student("student0500@university.edu")
        end_time = time.time()
        
        self.assertTrue(result)
        self.assertEqual(len(self.student_manager.students), initial_count - 1)
        
        delete_time = end_time - start_time
        print(f"\ntime to delete from 1000 records: {delete_time:.6f} seconds")
    
    def test_update_in_large_dataset(self):
        start_time = time.time()
        result = self.student_manager.update_student_record(
            "student0500@university.edu",
            Grades="A+",
            marks=98.5
        )
        end_time = time.time()
        
        self.assertTrue(result)
        student = next(s for s in self.student_manager.students 
                      if s.email_address == "student0500@university.edu")
        self.assertEqual(student.Grades, "A+")
        self.assertEqual(student.marks, 98.5)
        
        update_time = end_time - start_time
        print(f"time to update in 1000 records: {update_time:.6f} seconds")


class TestLoadFromPreviousRuns(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "persistent_students.csv"
    
    def test_load_and_search_from_previous_run(self):
        
        if not os.path.exists(self.test_csv):
            print(f"\ncreating {self.test_csv} with 1000 records for first run...")
            temp_manager = StudentManager(self.test_csv)
            for i in range(1000):
                temp_manager.add_new_student(
                    f"persistent{i:04d}@university.edu",
                    f"PersistentFirst{i}",
                    f"PersistentLast{i}",
                    f"CS{100 + (i % 10)}",
                    self._get_grade(90 - (i % 50)),
                    90 - (i % 50)
                )
            print(f"created and saved {len(temp_manager.students)} records")
        
        print(f"\nloading data from previous run ({self.test_csv})...")
        start_load = time.time()
        manager = StudentManager(self.test_csv)
        end_load = time.time()
        load_time = end_load - start_load
        
        print(f"  loaded {len(manager.students)} records from csv")
        print(f"  load time: {load_time:.6f} seconds")
        
        self.assertGreater(len(manager.students), 0, "No data loaded from previous run")

        search_results = []
        
        print("search by email (exact match):")
        results, search_time = manager.search_students("persistent0500", "email_address")
        search_time_seconds = search_time / 1000
        search_results.append(("email exact match", search_time_seconds))
        print(f"   found {len(results)} result(s) in {search_time_seconds:.6f} seconds")
        
        print("search by first name:")
        results, search_time = manager.search_students("PersistentFirst5", "FirstName")
        search_time_seconds = search_time / 1000
        search_results.append(("first name", search_time_seconds))
        print(f"   found {len(results)} result(s) in {search_time_seconds:.6f} seconds")
        
        print("search by last name:")
        results, search_time = manager.search_students("PersistentLast7", "LastName")
        search_time_seconds = search_time / 1000
        search_results.append(("last name", search_time_seconds))
        print(f"   found {len(results)} result(s) in {search_time_seconds:.6f} seconds")
        
        print("search by course id:")
        results, search_time = manager.search_students("CS101", "course_id")
        search_time_seconds = search_time / 1000
        search_results.append(("course id", search_time_seconds))
        print(f"   found {len(results)} result(s) in {search_time_seconds:.6f} seconds")
        
        self.assertGreater(len(search_results), 0)
        self.assertTrue(all(time > 0 for _, time in search_results))
    
    def _get_grade(self, marks):
        if marks >= 90:
            return "A"
        elif marks >= 80:
            return "B"
        elif marks >= 70:
            return "C"
        elif marks >= 60:
            return "D"
        else:
            return "F"


class TestLoginManager(unittest.TestCase):
    
    def setUp(self):
        self.test_csv = "test_login.csv"
        self.login_manager = LoginManager(self.test_csv)
    
    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
    
    def test_register_user(self):
        result = self.login_manager.register_user("test@example.com", "password123", "student")
        self.assertTrue(result)
        self.assertEqual(len(self.login_manager.users), 1)
    
    def test_login(self):
        self.login_manager.register_user("test@example.com", "password123", "student")
        
        user = self.login_manager.login("test@example.com", "password123")
        self.assertIsNotNone(user)
        
        user = self.login_manager.login("test@example.com", "wrongpassword")
        self.assertIsNone(user)
    
    def test_change_password(self):
        self.login_manager.register_user("test@example.com", "oldpassword", "student")
        
        result = self.login_manager.change_password("test@example.com", "oldpassword", "newpassword")
        self.assertTrue(result)
        
        user = self.login_manager.login("test@example.com", "newpassword")
        self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main(verbosity=2)

