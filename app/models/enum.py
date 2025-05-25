import enum

class RoleEnum(enum.Enum):
    Student = "Student"
    Teacher = "Teacher"
    Admin = "Admin"

class SemesterEnum(enum.Enum):
    SPRING = "Spring"
    SUMMER = "Summer"
    FALL = "Fall"
    WINTER = "Winter"
