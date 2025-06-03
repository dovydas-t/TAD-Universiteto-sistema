"""
Comprehensive Database seeding script for University Management System
Seeds ALL tables with realistic, interconnected data for full system testing
"""

import os
import sys
import random
from datetime import datetime, date, timedelta
from app.extensions import bcrypt

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.auth import AuthUser
from app.models.profile import UserProfile, RoleEnum
from app.models.faculty import Faculty
from app.models.study_program import StudyProgram
from app.models.groups import Groups
from app.models.module import Module, SemesterEnum
from app.models.module_requirement import ModuleRequirement
from app.models.assignment import Assignment
from app.models.schedule_item import ScheduleItem
from app.models.attendance import Attendance
from app.models.grade import Grade
from app.models.test import Test
from app.models.test_question import TestQuestion
from app.models.answer_option import AnswerOption


class DatabaseSeeder:
    def __init__(self):
        self.app = create_app()
        self.app.app_context().push()
    
    def run(self):
        print("Starting database seeding...")
        self.seed_faculties()
        self.seed_study_programs()
        self.seed_users()
        self.seed_groups()
        self.seed_modules()
        self.seed_module_requirements()
        self.seed_assignments()
        self.seed_schedule()
        self.seed_attendance()
        self.seed_tests()
        self.seed_grades()
        db.session.commit()
        print("Database seeding completed.")

    def seed_faculties(self):
        print("Seeding faculties...")
        faculties = [
            Faculty(name="Faculty of Engineering"),
            Faculty(name="Faculty of Arts"),
            Faculty(name="Faculty of Science")
        ]
        db.session.bulk_save_objects(faculties)
        db.session.commit()
        self.faculties = Faculty.query.all()

    def seed_study_programs(self):
        print("Seeding study programs...")
        programs = [
            StudyProgram(name="Computer Engineering", faculty_id=self.faculties[0].id),
            StudyProgram(name="Mechanical Engineering", faculty_id=self.faculties[0].id),
            StudyProgram(name="English Literature", faculty_id=self.faculties[1].id),
            StudyProgram(name="Physics", faculty_id=self.faculties[2].id),
        ]
        db.session.bulk_save_objects(programs)
        db.session.commit()
        self.study_programs = StudyProgram.query.all()

    def seed_users(self):
        print("Seeding users with roles...")
        # Create admin user
        admin_auth = AuthUser(
            username="admin",
            password_hash = bcrypt.generate_password_hash("adminpass")
        )
        db.session.add(admin_auth)
        db.session.flush()  # To get id

        admin_profile = UserProfile(
            id=admin_auth.id,
            first_name="Admin",
            last_name="User",
            role=RoleEnum.Admin
        )
        db.session.add(admin_profile)

        # Create teacher users
        teacher_auths = []
        teacher_profiles = []
        for i in range(3):
            auth = AuthUser(
                username=f"teacher{i+1}",
                password_hash = bcrypt.generate_password_hash(f"teacher{i+1}pass")
            )
            db.session.add(auth)
            db.session.flush()
            profile = UserProfile(
                id=auth.id,
                first_name="Teacher",
                last_name=f"{i+1}",
                role=RoleEnum.Teacher
            )
            db.session.add(profile)
            teacher_auths.append(auth)
            teacher_profiles.append(profile)

        # Create student users
        student_auths = []
        student_profiles = []
        for i in range(10):
            auth = AuthUser(
                username=f"student{i+1}",
                password_hash = bcrypt.generate_password_hash(f"student{i+1}pass")
            )
            db.session.add(auth)
            db.session.flush()
            profile = UserProfile(
                id=auth.id,
                first_name ="Student",
                last_name=f"{i+1}",
                role=RoleEnum.Student
            )
            db.session.add(profile)
            student_auths.append(auth)
            student_profiles.append(profile)

        db.session.commit()
        self.admin = admin_profile
        self.teachers = teacher_profiles
        self.students = student_profiles

    def seed_groups(self):
        print("Seeding groups...")
        groups = []
        # Let's create groups per study program, each with some students
        for i, program in enumerate(self.study_programs):
            group = Groups(
                code=f"Group {i+1} - {program.name}",
                study_program_id=program.id
            )
            groups.append(group)
            db.session.add(group)
        db.session.commit()
        self.groups = Groups.query.all()

        # Assign students to groups roughly equally
        for i, student in enumerate(self.students):
            group = self.groups[i % len(self.groups)]
            group.users.append(student)
        db.session.commit()

    def seed_modules(self):
        print("Seeding modules...")

        if len(self.study_programs) < 4:
            raise ValueError("Expected at least 4 study programs to seed modules.")

        modules = [
            Module(
                name="Introduction to Programming",
                description="Basics of programming using Python. Covers variables, control flow, functions, and basic data structures.",
                credits=6,
                semester=SemesterEnum.FALL,
                study_program_id=self.study_programs[0].id,
                faculty_id=self.study_programs[0].faculty_id,
                image_path="images/modules/intro_programming.png"
            ),
            Module(
                name="Data Structures",
                description="Covers arrays, lists, stacks, queues, trees, graphs, and algorithmic applications.",
                credits=6,
                semester=SemesterEnum.SPRING,
                study_program_id=self.study_programs[0].id,
                faculty_id=self.study_programs[0].faculty_id,
                image_path="images/modules/data_structures.png"
            ),
            Module(
                name="Thermodynamics",
                description="Explores the laws of thermodynamics, heat transfer, and applications in engineering.",
                credits=5,
                semester=SemesterEnum.FALL,
                study_program_id=self.study_programs[1].id,
                faculty_id=self.study_programs[1].faculty_id,
                image_path="images/modules/thermodynamics.png"
            ),
            Module(
                name="English Poetry",
                description="Analyzes major poetic movements, forms, and authors in English literature.",
                credits=4,
                semester=SemesterEnum.SPRING,
                study_program_id=self.study_programs[2].id,
                faculty_id=self.study_programs[2].faculty_id,
                image_path="images/modules/english_poetry.png"
            ),
            Module(
                name="Quantum Mechanics",
                description="Fundamentals of quantum theory including wave functions, uncertainty, and operators.",
                credits=6,
                semester=SemesterEnum.FALL,
                study_program_id=self.study_programs[3].id,
                faculty_id=self.study_programs[3].faculty_id,
                image_path="images/modules/quantum_mechanics.png"
            )
        ]

        db.session.bulk_save_objects(modules)
        db.session.commit()
        self.modules = Module.query.all()

    def seed_module_requirements(self):
        print("Seeding module requirements (pre-requisites)...")
        # Example: Data Structures requires Introduction to Programming
        intro_prog = next((m for m in self.modules if m.name == "Introduction to Programming"), None)
        data_struct = next((m for m in self.modules if m.name == "Data Structures"), None)

        if intro_prog and data_struct:
            req = ModuleRequirement(module_id=data_struct.id, required_module_id=intro_prog.id)
            db.session.add(req)
            db.session.commit()

    def seed_assignments(self):
        print("Seeding assignments...")
        assignments = []
        for module in self.modules:
            assignment = Assignment(
                title=f"Assignment 1 for {module.name}",
                description=f"This is the first assignment for {module.name}.",
                module_id=module.id,
                due_date=datetime.utcnow() + timedelta(days=30)
            )
            assignments.append(assignment)
            db.session.add(assignment)
        db.session.commit()
        self.assignments = assignments

    def seed_schedule(self):
        print("Seeding schedule items...")
        schedule_items = []
        # Create some schedule entries per group and module
        for group in self.groups:
            for module in self.modules:
                schedule_item = ScheduleItem(
                    group_id=group.id,
                    module_id=module.id,
                    start_time=datetime.utcnow() + timedelta(days=random.randint(1, 60)),
                    end_time=datetime.utcnow() + timedelta(days=random.randint(61, 120)),
                    location=f"Room {random.randint(100, 500)}"
                )
                schedule_items.append(schedule_item)
                db.session.add(schedule_item)
        db.session.commit()
        self.schedule_items = schedule_items

    def seed_attendance(self):
        print("Seeding attendance records...")
        # For each schedule item, randomly mark attendance for students in group
        for schedule in self.schedule_items:
            group = Groups.query.get(schedule.group_id)
            for student in group.students:
                attended = random.choice([True, False])
                attendance = Attendance(
                    student_id=student.id,
                    schedule_item_id=schedule.id,
                    date=schedule.start_time.date(),
                    status="present" if attended else "absent"
                )
                db.session.add(attendance)
        db.session.commit()

    def seed_tests(self):
        print("Seeding tests, questions, and answer options...")
        for module in self.modules:
            test = Test(
                title=f"Midterm Test for {module.name}",
                module_id=module.id,
                date=datetime.utcnow() + timedelta(days=45)
            )
            db.session.add(test)
            db.session.flush()

            # Add 3 questions per test
            for q_num in range(1, 4):
                question = TestQuestion(
                    test_id=test.id,
                    text=f"Question {q_num} for {module.name}?"
                )
                db.session.add(question)
                db.session.flush()

                # Add 4 answer options per question, with one correct
                correct_index = random.randint(0, 3)
                for option_num in range(4):
                    option = AnswerOption(
                        test_question_id=question.id,
                        text=f"Option {option_num + 1} for question {q_num}",
                        is_correct=(option_num == correct_index)
                    )
                    db.session.add(option)
        db.session.commit()

    def seed_grades(self):
        print("Seeding grades for students...")
        for student in self.students:
            for assignment in self.assignments:
                grade_value = random.randint(50, 100)
                grade = Grade(
                    student_id=student.id,
                    assignment_id=assignment.id,
                    value=grade_value,
                    graded_on=datetime.utcnow()
                )
                db.session.add(grade)
        db.session.commit()

    def clear_database(self):
        print("Clearing database...")
        # Delete in order respecting FK constraints
        # Adjust this based on your actual FK constraints and tables
        models = [
            Grade, Attendance, ScheduleItem, Assignment, ModuleRequirement,
            Module, Groups, UserProfile, AuthUser, StudyProgram, Faculty,
            Test, TestQuestion, AnswerOption
        ]
        for model in models:
            db.session.query(model).delete()
        db.session.commit()
        print("Database cleared.")

    def create_three_users(self):
        print("Creating 3 users with different roles...")
        # Clear existing users first
        db.session.query(UserProfile).delete()
        db.session.query(AuthUser).delete()
        db.session.commit()

        # Admin user
        admin_auth = AuthUser(
            username="admin_user",
            password_hash=bcrypt.generate_password_hash("adminpass")
        )
        db.session.add(admin_auth)
        db.session.flush()
        admin_profile = UserProfile(
            id=admin_auth.id,
            first_name="Admin",
            last_name="User",
            role=RoleEnum.Admin
        )
        db.session.add(admin_profile)

        # Teacher user
        teacher_auth = AuthUser(
            username="teacher_user",
            password_hash=bcrypt.generate_password_hash("teacherpass")
        )
        db.session.add(teacher_auth)
        db.session.flush()
        teacher_profile = UserProfile(
            id=teacher_auth.id,
            first_name="Teacher",
            last_name="User",
            role=RoleEnum.Teacher
        )
        db.session.add(teacher_profile)

        # Student user
        student_auth = AuthUser(
            username="student_user",
            password_hash=bcrypt.generate_password_hash("studentpass")
        )
        db.session.add(student_auth)
        db.session.flush()
        student_profile = UserProfile(
            id=student_auth.id,
            first_name="Student",
            last_name="User",
            role=RoleEnum.Student
        )
        db.session.add(student_profile)

        db.session.commit()
        print("3 users created: Admin, Teacher, Student.")

if __name__ == "__main__":
    seeder = DatabaseSeeder()

    def menu():
        print("\nUniversity Management System Seeder")
        print("1. Create 3 users with different roles")
        print("2. Seed entire database with random entries")
        print("3. Clear the database")
        print("0. Exit")
        return input("Choose an option: ").strip()

    while True:
        choice = menu()
        if choice == "1":
            seeder.create_three_users()
        elif choice == "2":
            seeder.run()
        elif choice == "3":
            seeder.clear_database()
        elif choice == "0":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select again.")

# if __name__ == "__main__":
#     seeder = DatabaseSeeder()
#     seeder.run()
