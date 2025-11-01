def read_marks(filename):
    data = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("student_id"):
                    continue
                parts = line.split(',')
                if len(parts) != 4:
                    print(f"Skipping malformed line: {line}")
                    continue
                student_id, name, subject, marks = parts
                try:
                    marks = int(marks)
                except ValueError:
                    print(f"Invalid marks value in line: {line}")
                    continue
                if student_id not in data:
                    data[student_id] = {'name': name, 'subjects': {}}
                data[student_id]['subjects'][subject] = marks
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    return data
def generate_report(data):
    report = []
    for student_id, info in data.items():
        subjects = info['subjects']
        total_marks = sum(subjects.values())
        avg_marks = total_marks / len(subjects)
        highest_subject = max(subjects, key=subjects.get)
        lowest_subject = min(subjects, key=subjects.get)
        report.append({
            'student_id': student_id,
            'name': info['name'],
            'total': total_marks,
            'average': avg_marks,
            'highest_subject': highest_subject,
            'highest_marks': subjects[highest_subject],
            'lowest_subject': lowest_subject,
            'lowest_marks': subjects[lowest_subject]
        })
    report.sort(key=lambda x: x['average'], reverse=True)
    return report

def write_summary(report, filename):
    with open(filename, 'w') as file:
        for student in report:
            file.write(f"Student ID: {student['student_id']}\n")
            file.write(f"Name: {student['name']}\n")
            file.write(f"Total Marks: {student['total']}\n")
            file.write(f"Average Marks: {student['average']:.2f}\n")
            file.write(f"Highest Scored Subject: {student['highest_subject']} ({student['highest_marks']})\n")
            file.write(f"Lowest Scored Subject: {student['lowest_subject']} ({student['lowest_marks']})\n")
            file.write("\n")

def main():
    filename = 'marks.txt'
    data = read_marks(filename)
    if not data:
        print("No valid data found. Exiting.")
        return
    report = generate_report(data)
    write_summary(report, 'report.txt')
    print("Report generated successfully!")

if __name__ == "__main__":
    main()