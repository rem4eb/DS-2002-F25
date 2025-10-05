import csv
import json
import pandas as pd

#––TASK 1––
# Data records
survey_data = [
    {"student_id": 1001, "major": "Computer Science", "GPA": 3.0, "is_cs_major": "Yes", "credits_taken": "15.0"},
    {"student_id": 1002, "major": "Biology", "GPA": 3.5, "is_cs_major": "No", "credits_taken": "15.5"},
    {"student_id": 1003, "major": "Mathematics", "GPA": 4, "is_cs_major": "No", "credits_taken": "17.0"},
    {"student_id": 1004, "major": "Spanish", "GPA": 2.8, "is_cs_major": "No", "credits_taken": "16.0"},
    {"student_id": 1005, "major": "Economics", "GPA": 3, "is_cs_major": "No", "credits_taken": "14.0"},
    {"student_id": 1006, "major": "Biomedical Engineering", "GPA": 4, "is_cs_major": "No", "credits_taken": "18.0"},

]

# Write to CSV file
with open("raw_survey_data.csv", mode="w", newline="") as csvfile:
    fieldnames = ["student_id", "major", "GPA", "is_cs_major", "credits_taken"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in survey_data:
        writer.writerow(row)
print("raw_survey_data.csv created successfully")

#––TASK 2––
course_catalog = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "BME2220",
        "section": "001",
        "title": "Biomechanics",
        "level": 200,
        "instructors": [
            {"name": "Dr. Natasha D. Sheybani", "role": "Primary"},
            {"name": "Amanda Knizley", "role": "Graduate TA"},
            {"name": "Owen Brown", "role": "Undergraduate TA"},
            {"name": "Andrew Wittman", "role": "Undergraduate TA"},
            {"name": "Niharika Chandna", "role": "Undergraduate TA"}
        ]
            
    },
    {
        "course_id": "BME2000",
        "section": "001",
        "title": "Biomedical Engineering Design and Discovery",
        "level": 200,
        "instructors": [
            {"name": "Dr. William H. Guildford", "role": "Primary"},
            {"name": "Bethany Amanuel", "role": "TA"},
            {"name": "Sabrina Berry", "role": "TA"}
        ]
    },
    {
        "course_id": "BME2000",
        "section": "001",
        "title": "Biomedical Engineering Design and Discovery",
        "level": 200,
        "instructors": [
            {"name": "Dr. William H. Guildford", "role": "Primary"},
            {"name": "Bethany Amanuel", "role": "TA"},
            {"name": "Sabrina Berry", "role": "TA"}
        ]
    },
    {
        "course_id": "PHYS1655",
        "section": "001",
        "title": "Python for Scientists",
        "level": 100,
        "instructors": [
            {"name": "Prof. Craig Croup", "role": "Primary"},
            {"name": "Vincent Blackburn", "role": "TA"},
            {"name": "Alex Flamm", "role": "TA"},
            {"name": "Jackson Glass", "role": "TA"}
        ]
    },
    {
        "course_id": "BIOL4900",
        "section": "001",
        "title": "Independent Study in Biology",
        "level": 400,
        "instructors": [
            {"name": "Dr. Keith G. Kozminski", "role": "Primary"},
        ]
    }
]


# Write to JSON file
with open("raw_course_catalog.json", mode="w") as jsonfile:
    json.dump(course_catalog, jsonfile, indent=2)
print("raw_course_catalog.json created successfully")

#––TASK 3––
df = pd.read_csv("raw_survey_data.csv")

# Convert 'is_cs_major' to boolean
df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})

# Enforce numeric types as float
df = df.astype({
    "GPA": "float64",
    "credits_taken": "float64"
})

# Save cleaned DataFrame
df.to_csv("clean_survey_data.csv", index=False)
print("clean_survey_data.csv created successfully")

#––TASK 4––
with open("raw_course_catalog.json", "r") as jsonfile2:
    course_data = json.load(jsonfile2)

# flat nested DataFrame
df_courses = pd.json_normalize(
    course_data,
    record_path=["instructors"], # flatten instructors
    meta=["course_id", "title", "level", "section"],
)

# Save normalized DataFrame
df_courses.to_csv("clean_course_catalog.csv", index=False)
print("clean_course_catalog.csv created successfully")
