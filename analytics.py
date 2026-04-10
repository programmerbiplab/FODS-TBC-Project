# analytics.py

from file_handler import read_file
import numpy as np

def get_analytics_data():
    grades_data = read_file("grades.txt")
    eca_data = read_file("eca.txt")

    student_ids = []
    all_grades = []

    for g in grades_data:
        parts = g.strip().split(",")
        student_ids.append(parts[0])
        all_grades.append(list(map(int, parts[1:])))

    all_grades_np = np.array(all_grades)
    avg_grades = np.mean(all_grades_np, axis=0)  # avg per subject
    averages = np.mean(all_grades_np, axis=1)    # avg per student

    eca_count = []
    eca_dict = dict()
    for e in eca_data:
        parts = e.strip().split(",")
        eca_dict[parts[0]] = parts[1:] if len(parts) > 1 else []
    for sid in student_ids:
        eca_count.append(len(eca_dict.get(sid, [])))

    return avg_grades, eca_count, averages, student_ids
