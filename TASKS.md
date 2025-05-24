🟢 **Progress Legend**:
- `[x]` = Complete
- `[ ]` = To Do


# DONE: Finished tasks
- `[x]` = Set up login functionality
- `[x]` = Implement user registration
# FIXME: Need fixes
# TODO: Tasks need to be done

# ✅ University Management System – Task Checklist

## 🔐 User Authentication & Registration
- [ ] Create user roles: Student, Teacher, Admin
- [ ] Hardcode initial Admin user
- [ ] Implement user registration with program selection
- [ ] Assign study group based on program (e.g., IFIN-18-A)
- [ ] Validate email and password
- [ ] Add profile picture upload with size/type validation
- [ ] Store picture path in DB, save files in `/uploads/profile_pictures/`
- [ ] Lock account after 3 failed login attempts (temporary)
- [ ] Admin-only page for registering new admins

## 📚 Module (Course) Management
- [ ] Create module model (name, description, credits, semester, etc.)
- [ ] Implement module CRUD (Create, Edit, View, Delete with confirmation)
- [ ] Allow students to choose modules based on program
- [ ] Check for schedule conflicts during module selection
- [ ] Enforce module prerequisites for students
- [ ] Teachers can set/edit schedules, requirements, and deadlines
- [ ] Link teachers to modules and track assignments

## 👩‍🏫 Role Permissions
- [ ] Students: View modules, schedule, grades
- [ ] Teachers: Manage modules, track progress and attendance
- [ ] Admins: Full control over users, modules, programs, groups

## 🧪 Bonus: Tests and Assignments
- [ ] Teachers can create tests for modules
- [ ] Students complete tests, results affect grades
- [ ] Handle validation and security during test processing
- [ ] Implement module assignment management (dates, descriptions)

## 🛠 Admin Panel
- [ ] Dashboard with stats: users, modules, groups
- [ ] Error tracking with try-except and readable messages
- [ ] Manage users: roles, programs, group assignment
- [ ] Deactivate/delete user accounts with cascading updates
- [ ] Full module edit capabilities for admin

## 🗂 Database & Migrations
- [ ] Define models: User, Module, Group, Assignment, Test
- [ ] Setup Flask-Migrate
- [ ] Wrap all DB operations with try-except blocks

## 🖼 Image Upload & Storage
- [ ] Upload user profile photos with validation
- [ ] (Bonus) Upload module illustrations
- [ ] Save file paths in DB, images in `/uploads/`

## 🏛 Academic Structure (Bonus)
- [ ] Faculties contain programs and modules
- [ ] Enrollment based on semester, program, schedule
- [ ] Multi-level prerequisite enforcement

## 🧪 Validation & Error Handling
- [ ] Validate schedules (no conflict overlap)
- [ ] Validate credits (no negative or excessive numbers)
- [ ] Wrap critical logic in try-except with clear error messages

## 🧱 Project Structure
- [ ] Separate folders: static, templates, controllers, services, models
- [ ] Separate files for each CRUD operation and form
- [ ] Prepare deployment-ready project structure

## 🔀 Git & Project Management
- [ ] Setup GitHub with `main`, `dev`, and `feature/*` branches
- [ ] Use Pull Requests for all merges
- [ ] Reach 10+ meaningful commits
- [ ] Track tasks using JIRA or similar platform

---
