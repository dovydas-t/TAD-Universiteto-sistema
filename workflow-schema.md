[User Registration]
    |
    v
[Select User Type: Student / Teacher / Admin]
    |
    v
[Fill Registration Form with Validation]
    |
    v
[Store User + Profile Picture]
    |
    v
[Login]
    |
    v
[Role-Based Dashboard]
    |                   |                     |
    v                   v                     v
[Student Dashboard]  [Teacher Dashboard]  [Admin Dashboard]

Student Dashboard:
    - View assigned modules
    - View academic info & schedule
    - Select courses (with prereq & schedule check)

Teacher Dashboard:
    - Create/Edit/Delete modules
    - Set schedules, assignments, prerequisites
    - Track student attendance & grades
    - Create/Assign tests (bonus)

Admin Dashboard:
    - Manage users (roles, groups, deactivate)
    - Manage modules & study programs
    - View system stats & errors

-------------------------------------------------------
Database Operations + Validation + Error Handling
-------------------------------------------------------
All CRUD operations wrapped in try-except with logging.

-------------------------------------------------------
File Upload
-------------------------------------------------------
Profile pictures and module images uploaded -> validated -> stored -> DB stores file paths.

-------------------------------------------------------
Database Migration
-------------------------------------------------------
Schema updates managed via Flask_Migrate.
