#!/usr/bin/env python3
"""
Database seeding script for University Management System
Seeds the database with sample data including 3 different user roles: Student, Teacher, and Admin
"""

import os
import sys
from datetime import datetime, date
from werkzeug.security import generate_password_hash

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.auth import AuthUser
from app.models.profile import UserProfile, RoleEnum
from app.models.faculty import Faculty
from app.models.study_program import StudyProgram
from app.models.groups import Groups
from app.models.module import Module, SemesterEnum


def create_sample_users():
    """Create sample users with different roles"""
    
    print("Creating sample users...")
    
    # Sample users data
    users_data = [
        {
            'username': 'admin_user',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'Administrator',
            'email': 'admin@university.edu',
            'role': RoleEnum.Admin,
            'birth_date': date(1980, 5, 15),
            'age': 44
        },
        {
            'username': 'prof_smith',
            'password': 'teacher123',
            'first_name': 'John',
            'last_name': 'Smith',
            'email': 'j.smith@university.edu',
            'role': RoleEnum.Teacher,
            'birth_date': date(1975, 8, 22),
            'age': 49
        },
        {
            'username': 'student_doe',
            'password': 'student123',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@student.university.edu',
            'role': RoleEnum.Student,
            'birth_date': date(2002, 3, 10),
            'age': 22
        }
    ]
    
    created_users = []
    
    for user_data in users_data:
        # Check if user already exists
        existing_user = AuthUser.query.filter_by(username=user_data['username']).first()
        if existing_user:
            print(f"User {user_data['username']} already exists, skipping...")
            created_users.append(existing_user)
            continue
            
        # Create AuthUser
        auth_user = AuthUser(
            username=user_data['username']
        )
        auth_user.set_password(user_data['password'])
        
        db.session.add(auth_user)
        db.session.flush()  # Flush to get the ID
        
        # Create UserProfile
        user_profile = UserProfile(
            id=auth_user.id,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            role=user_data['role'],
            birth_date=user_data['birth_date'],
            age=user_data['age'],
            failed_logins=0,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            last_login=datetime.utcnow()
        )
        
        db.session.add(user_profile)
        created_users.append(auth_user)
        
        print(f"Created user: {user_data['username']} ({user_data['role'].value})")
    
    return created_users


def create_sample_faculty_and_programs():
    """Create sample faculty and study programs"""
    
    print("Creating sample faculties and study programs...")
    
    # Create Faculty
    faculty_data = [
        {'name': 'Faculty of Computer Science'},
        {'name': 'Faculty of Engineering'},
        {'name': 'Faculty of Mathematics'}
    ]
    
    faculties = []
    for faculty_info in faculty_data:
        existing_faculty = Faculty.query.filter_by(name=faculty_info['name']).first()
        if existing_faculty:
            print(f"Faculty {faculty_info['name']} already exists, skipping...")
            faculties.append(existing_faculty)
            continue
            
        faculty = Faculty(name=faculty_info['name'])
        db.session.add(faculty)
        faculties.append(faculty)
        print(f"Created faculty: {faculty_info['name']}")
    
    db.session.flush()
    
    # Create Study Programs
    programs_data = [
        {'name': 'Bachelor of Computer Science', 'faculty': faculties[0]},
        {'name': 'Master of Software Engineering', 'faculty': faculties[0]},
        {'name': 'Bachelor of Mechanical Engineering', 'faculty': faculties[1]},
        {'name': 'Bachelor of Mathematics', 'faculty': faculties[2]}
    ]
    
    study_programs = []
    for program_info in programs_data:
        existing_program = StudyProgram.query.filter_by(
            name=program_info['name'], 
            faculty_id=program_info['faculty'].id
        ).first()
        if existing_program:
            print(f"Study program {program_info['name']} already exists, skipping...")
            study_programs.append(existing_program)
            continue
            
        program = StudyProgram(
            name=program_info['name'],
            faculty_id=program_info['faculty'].id
        )
        db.session.add(program)
        study_programs.append(program)
        print(f"Created study program: {program_info['name']}")
    
    return faculties, study_programs


def create_sample_groups(study_programs):
    """Create sample groups"""
    
    print("Creating sample groups...")
    
    groups_data = [
        {'code': 'CS-2024-A', 'study_program': study_programs[0]},
        {'code': 'CS-2024-B', 'study_program': study_programs[0]},
        {'code': 'SE-2024-A', 'study_program': study_programs[1]},
        {'code': 'ME-2024-A', 'study_program': study_programs[2]}
    ]
    
    groups = []
    for group_info in groups_data:
        existing_group = Groups.query.filter_by(code=group_info['code']).first()
        if existing_group:
            print(f"Group {group_info['code']} already exists, skipping...")
            groups.append(existing_group)
            continue
            
        group = Groups(
            code=group_info['code'],
            study_program_id=group_info['study_program'].id
        )
        db.session.add(group)
        groups.append(group)
        print(f"Created group: {group_info['code']}")
    
    return groups


def create_sample_modules(study_programs):
    """Create sample modules"""
    
    print("Creating sample modules...")
    
    modules_data = [
        {
            'name': 'Introduction to Programming',
            'description': 'Basic programming concepts using Python',
            'credits': 6,
            'semester': SemesterEnum.FALL,
            'study_program': study_programs[0]
        },
        {
            'name': 'Data Structures and Algorithms',
            'description': 'Advanced data structures and algorithm design',
            'credits': 8,
            'semester': SemesterEnum.SPRING,
            'study_program': study_programs[0]
        },
        {
            'name': 'Software Engineering Principles',
            'description': 'Principles of software development and project management',
            'credits': 6,
            'semester': SemesterEnum.FALL,
            'study_program': study_programs[1]
        }
    ]
    
    modules = []
    for module_info in modules_data:
        existing_module = Module.query.filter_by(
            name=module_info['name'],
            study_program_id=module_info['study_program'].id
        ).first()
        if existing_module:
            print(f"Module {module_info['name']} already exists, skipping...")
            modules.append(existing_module)
            continue
            
        module = Module(
            name=module_info['name'],
            description=module_info['description'],
            credits=module_info['credits'],
            semester=module_info['semester'],
            study_program_id=module_info['study_program'].id
        )
        db.session.add(module)
        modules.append(module)
        print(f"Created module: {module_info['name']}")
    
    return modules


def assign_student_to_program_and_group(users, study_programs, groups):
    """Assign the student user to a study program and group"""
    
    print("Assigning student to program and group...")
    
    # Find the student user
    student_profile = None
    for user in users:
        if user.profile and user.profile.role == RoleEnum.Student:
            student_profile = user.profile
            break
    
    if student_profile and study_programs and groups:
        student_profile.study_program_id = study_programs[0].id  # Assign to CS program
        student_profile.group_id = groups[0].id  # Assign to CS-2024-A group
        print(f"Assigned student {student_profile.full_name} to {study_programs[0].name} and group {groups[0].code}")


def seed_database():
    """Main seeding function"""
    
    print("Starting database seeding...")
    print("=" * 50)
    
    try:
        # Create users with different roles
        users = create_sample_users()
        
        # Create faculties and study programs
        faculties, study_programs = create_sample_faculty_and_programs()
        
        # Create groups
        groups = create_sample_groups(study_programs)
        
        # Create modules
        modules = create_sample_modules(study_programs)
        
        # Assign student to program and group
        assign_student_to_program_and_group(users, study_programs, groups)
        
        # Commit all changes
        db.session.commit()
        
        print("=" * 50)
        print("Database seeding completed successfully!")
        print("\nCreated users:")
        print("- admin_user (Admin) - Password: admin123")
        print("- prof_smith (Teacher) - Password: teacher123") 
        print("- student_doe (Student) - Password: student123")
        print("\nYou can use these credentials to test different user roles.")
        
    except Exception as e:
        print(f"Error during seeding: {str(e)}")
        db.session.rollback()
        raise


def clear_database():
    """Clear all data from database (use with caution!)"""
    
    print("WARNING: This will clear all data from the database!")
    confirm = input("Are you sure you want to continue? (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            # Drop all tables and recreate them
            db.drop_all()
            db.create_all()
            print("Database cleared successfully!")
        except Exception as e:
            print(f"Error clearing database: {str(e)}")
            raise
    else:
        print("Database clearing cancelled.")


if __name__ == '__main__':
    # Create Flask app and setup database context
    app = create_app()
    
    with app.app_context():
        # # Check command line arguments
        # if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        #     clear_database()
        
        # # Create tables if they don't exist
        # db.create_all()
        
        # Seed the database
        seed_database()