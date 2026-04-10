

from file_handler import read_file, write_file, append_file

class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

    def update_profile(self, new_name):
        users = read_file("users.txt")
        for i in range(len(users)):
            parts = users[i].split(",")
            if parts[0] == self.user_id:
                parts[1] = new_name
                users[i] = ",".join(parts)
                write_file("users.txt", users)
                self.name = new_name
                break

class Student(User):
    def view_grades(self):
        grades = read_file("grades.txt")
        for g in grades:
            parts = g.split(",")
            if parts[0] == self.user_id:
                return list(map(int, parts[1:]))
        return []

    def view_eca(self):
        eca = read_file("eca.txt")
        for e in eca:
            parts = e.split(",")
            if parts[0] == self.user_id:
                return parts[1:]
        return []

class Admin(User):
    def add_user(self, user_id, name, role, password):
        append_file("users.txt", f"{user_id},{name},{role}")
        append_file("passwords.txt", f"{user_id},{password}")
        append_file("grades.txt", f"{user_id},0,0,0,0,0")
        append_file("eca.txt", f"{user_id},None")

    def delete_user(self, user_id):
        for fname in ["users.txt", "passwords.txt", "grades.txt", "eca.txt"]:
            lines = read_file(fname)
            lines = [line for line in lines if not line.startswith(user_id + ",")]
            write_file(fname, lines)

    def update_grades(self, user_id, new_grades):
        grades = read_file("grades.txt")
        for i in range(len(grades)):
            parts = grades[i].split(",")
            if parts[0] == user_id:
                grades[i] = f"{user_id}," + ",".join(map(str, new_grades))
                break
        write_file("grades.txt", grades)

    def update_eca(self, user_id, activities):
        eca = read_file("eca.txt")
        for i in range(len(eca)):
            parts = eca[i].split(",")
            if parts[0] == user_id:
                eca[i] = f"{user_id}," + ",".join(activities)
                break
        write_file("eca.txt", eca)
