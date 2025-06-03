## Relationships summary:
- auth_user 1:1 user_profile (via user_profile.id = auth_user.id)

faculty 1:N study_program

study_program 1:N groups

study_program 1:N module

study_program 1:N user_profile

groups 1:N user_profile

module 1:N module_requirement (as module_id)

module 1:N module_requirement (as required_module_id)

module 1:N assignment

module 1:N test

test 1:N test_question

test_question 1:N answer_option

user_profile 1:N attendance

module 1:N attendance

user_profile 1:N grade

module 1:N grade

module 1:N schedule_item
# Models Documentation

---

## AnswerOption

- **Table:** answer_option  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `question_id` (Integer, ForeignKey to `test_question.id`)  
  - `option_text` (Text, not nullable)  
  - `is_correct` (Boolean, default=False)  
- **Relationships:**  
  - `question`: relationship to `TestQuestion` (back_populates="answer_options")

---

## Assignment

- **Table:** assignment  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `title` (String(255))  
  - `due_date` (DateTime)  
- **Relationships:**  
  - `module`: relationship to `Module` (back_populates="assignments")

---

## Attendance

- **Table:** attendance  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `student_id` (Integer, ForeignKey to `user_profile.id`)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `date` (Date)  
  - `present` (Boolean)  
- **Relationships:**  
  - `student`: relationship to `UserProfile` (back_populates="attendances")  
  - `module`: relationship to `Module` (back_populates="attendances")

---

## AuthUser

- **Table:** auth_user  
- **Fields:**  
  - `id` (Integer, primary key)  
  - `username` (String(255), unique, not nullable)  
  - `password_hash` (String(255))  
- **Relationships:**  
  - `profile`: relationship to `UserProfile` (back_populates='user', one-to-one)  
- **Methods:**  
  - `set_password(password)`: hashes and sets password  
  - `check_password(password)`: verifies password  
- **Mixin:** `UserMixin` from Flask-Login

---

## Enums

### RoleEnum

- Student  
- Teacher  
- Admin

### SemesterEnum

- SPRING  
- SUMMER  
- FALL  
- WINTER

---

## Faculty

- **Table:** faculty  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `name` (String(255))  
- **Relationships:**  
  - `programs`: relationship to `StudyProgram` (back_populates="faculty")  
- **Methods:**  
  - `__repr__`: `<Faculty {id}: {name}>`

---

## Grade

- **Table:** grade  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `student_id` (Integer, ForeignKey to `user_profile.id`)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `grade` (Float)  
- **Relationships:**  
  - `student`: relationship to `UserProfile` (back_populates="grades")  
  - `module`: relationship to `Module` (back_populates="grades")

---

## Groups

- **Table:** groups  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `code` (String(255))  
  - `study_program_id` (Integer, ForeignKey to `study_program.id`)  
- **Relationships:**  
  - `study_program`: relationship to `StudyProgram` (back_populates="groups")  
  - `users`: relationship to `UserProfile` (back_populates="group")

---

## ModuleRequirement

- **Table:** module_requirement  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `required_module_id` (Integer, ForeignKey to `module.id`)  
- **Relationships:**  
  - `module`: relationship to `Module` (foreign_keys=[module_id], back_populates="requirements")  
  - `required_module`: relationship to `Module` (foreign_keys=[required_module_id], back_populates="required_for")

---

## Module

- **Table:** module  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `name` (String(255))  
  - `description` (Text)  
  - `credits` (Integer)  
  - `semester` (Enum: `SemesterEnum`)  
  - `study_program_id` (Integer, ForeignKey to `study_program.id`)  
  - `image_path` (String(255))  
- **Relationships:**  
  - `study_program`: relationship to `StudyProgram` (back_populates="modules")  
  - `requirements`: relationship to `ModuleRequirement` (foreign_keys='ModuleRequirement.module_id', back_populates="module")  
  - `required_for`: relationship to `ModuleRequirement` (foreign_keys='ModuleRequirement.required_module_id', back_populates="required_module")  
  - `assignments`: relationship to `Assignment` (back_populates="module")  
  - `tests`: relationship to `Test` (back_populates="module")  
  - `attendances`: relationship to `Attendance` (back_populates="module")  
  - `grades`: relationship to `Grade` (back_populates="module")  
  - `schedule_items`: relationship to `ScheduleItem` (back_populates="module")

---

## UserProfile

- **Table:** user_profile  
- **Fields:**  
  - `id` (Integer, ForeignKey to `auth_user.id`, primary key)  
  - `first_name` (String(64))  
  - `last_name` (String(64))  
  - `birth_date` (Date, nullable)  
  - `age` (Integer)  
  - `email` (String(35), unique, nullable)  
  - `failed_logins` (Integer)  
  - `profile_pic_path` (String(255))  
  - `is_active` (Boolean, default=True)  
  - `study_program_id` (Integer, ForeignKey to `study_program.id`)  
  - `group_id` (Integer, ForeignKey to `groups.id`)  
  - `role` (Enum: `RoleEnum`, default=Student, not nullable)  
  - `created_at` (DateTime, default current timestamp, not nullable)  
  - `updated_at` (DateTime, default current timestamp, auto-updated)  
  - `last_login` (DateTime, default current timestamp, auto-updated)  
- **Relationships:**  
  - `user`: relationship to `AuthUser` (back_populates='profile')  
  - `study_program`: relationship to `StudyProgram` (back_populates="users")  
  - `group`: relationship to `Groups` (back_populates="users")  
  - `attendances`: relationship to `Attendance` (back_populates="student")  
  - `grades`: relationship to `Grade` (back_populates="student")  
- **Methods:**  
  - `__repr__`: `UserProfile('{id}', '{created_at}')`  
  - `full_name` (property): returns concatenated first and last name or username fallback

---

## ScheduleItem

- **Table:** schedule_item  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `type` (String(255)) — e.g., 'Lecture', 'Exam'  
  - `date` (DateTime)  
- **Relationships:**  
  - `module`: relationship to `Module` (back_populates="schedule_items")

---

## StudyProgram

- **Table:** study_program  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `name` (String(255))  
  - `faculty_id` (Integer, ForeignKey to `faculty.id`)  
- **Relationships:**  
  - `faculty`: relationship to `Faculty` (back_populates="programs")  
  - `groups`: relationship to `Groups` (back_populates="study_program")  
  - `modules`: relationship to `Module` (back_populates="study_program")  
  - `users`: relationship to `UserProfile` (back_populates="study_program")  
- **Methods:**  
  - `__repr__`: `Study Program('{name}', Study Program ID: {id})`

---

## TestQuestion

- **Table:** test_question  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `test_id` (Integer, ForeignKey to `test.id`)  
  - `question_text` (Text, not nullable)  
- **Relationships:**  
  - `test`: relationship to `Test` (back_populates="questions")  
  - `answer_options`: relationship to `AnswerOption` (back_populates="question", cascade="all, delete-orphan")

---

## Test

- **Table:** test  
- **Fields:**  
  - `id` (Integer, primary key, autoincrement)  
  - `module_id` (Integer, ForeignKey to `module.id`)  
  - `name` (String(255))  
- **Relationships:**  
  - `module`: relationship to `Module` (back_populates="tests")  
  - `questions`: relationship to `TestQuestion` (back_populates="test", cascade="all, delete-orphan")

---
