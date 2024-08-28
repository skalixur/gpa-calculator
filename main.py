import sys

# GPA Calculator

def grade_point_to_letter_mark(grade_point):
  # use a hash map to map the values:
  """
  4.10 or higher A+
  3.75 or higher A
  3.25 or higher A-
  2.75 or higher B
  2.25 or higher B-
  1.75 or higher C
  1.25 or higher D
  0.75 or higher F
  0.00 or higher FF
  """
  
  conversion_table = {
    4.10: 'A+',
    3.75: 'A',
    3.25: 'A-',
    2.75: 'B',
    2.25: 'B-',
    1.75: 'C',
    1.25: 'D',
    0.75: 'F',
    0: 'FF'
  }

  for key in conversion_table:
    if grade_point >= key:
      return conversion_table[key]

def letter_mark_to_grade_point(letter_mark):
  # use a hash map to map the values:
  """
  Letter Mark to Grade Point Table  \n  
  A+    4.2\n
  A    4\n
  A-    3.5\n
  B    3\n
  B-    2.5\n
  C    2\n
  D    1.5\n
  F    1\n
  FF    0\n
  """

  conversion_table = {
    'A+': 4.2,
    'A': 4,
    'A-': 3.5,
    'B': 3,
    'B-': 2.5,
    'C': 2,
    'D': 1.5,
    'F': 1,
    'FF': 0
  }

  return conversion_table[letter_mark]

class Assessment:
  def __init__(self, number, letter_mark):
    self.number = number
    self.letter_mark = letter_mark

class MeasurementTopic:
  def __init__(self, name, weight):
    self.name = name
    self.weight = weight
    self.assessments = {}

  def evaluate_letter_grade(self, subject_holistic):
    if self.assessments.values() == []:
      print("No assessments to evaluate! :c")
      return

    if subject_holistic:
      average_grade_point = sum(letter_mark_to_grade_point(assessment.letter_mark) for assessment in self.assessments.values()) / len(self.assessments)
      average_letter_mark = grade_point_to_letter_mark(average_grade_point)
      return average_letter_mark
    else:
      highest_letter_mark = grade_point_to_letter_mark(max(letter_mark_to_grade_point(assessment.letter_mark) for assessment in self.assessments.values()))
      return highest_letter_mark
  
  def add_assessment(self, number, letter_mark):
    assessment = Assessment(number, letter_mark)
    self.assessments[number] = assessment

class Subject:
  def __init__(self, name, units, is_holistic, num_measurement_topics):
    self.name = name
    self.units = units
    self.holistic = is_holistic
    self.measurement_topics = []
    
    for i in range(num_measurement_topics):
      topic_name = input(f"Enter the name of measurement topic {i+1}: ")
      topic_weight = float(input(f"Enter the weight of measurement topic {i+1}: "))
      
      topic = MeasurementTopic(topic_name, topic_weight)
      self.measurement_topics.append(topic)
  
  def evaluate_letter_grade(self):
    total_grade_point = 0
    total_weight = 0
    for topic in self.measurement_topics:
        topic_grade_point = letter_mark_to_grade_point(topic.evaluate_letter_grade(self.holistic))
        total_grade_point += topic_grade_point * topic.weight
        total_weight += topic.weight

    if total_weight == 0:
        return None  # or handle the case where there are no weights

    weighted_average = total_grade_point / total_weight
    return grade_point_to_letter_mark(weighted_average)

subjects = []

while True:
  print("Please select an option:\n"
  "0. Calculate grades\n"
  "1. New subject\n"
  "2. New assessment\n"
  "3. Exit"
  ) # Never gonna give you up never gonna let you down never gonna run around and deser you never gonna make you cry never gonna sax you goodbye never gonna tell a lie and hurt you            
  # "3. Modify subject\n"
  # "4. Modify measurement topic\n"
  # "5. Modify assessment\n"
  # "6. Delete subject\n"
  # "7. Delete measurement topic\n"
  # "8. Delete assessment\n"

  choice = input("Please enter your choice: ")

  if choice == "0":
    print("Please select an option:\n",
          "0. Calculate measurement topic grade\n",
          "1. Calculate subject grade\n",
          "2. Calculate GPA\n",)
    
    calculation_choice = input("Enter your choice: ")
    if calculation_choice == "0":
      # Code for calculating measurement topic grade
      subject_index = 0
      for i, subject in enumerate(subjects):
        print(f"{i+1}. {subject.name}")
      subject_choice = int(input("Please enter the number of the subject: "))

      if subject_choice < 1 or subject_choice > len(subjects):
        print("Invalid subject choice. Please try again.")
      else:
        subject = subjects[subject_choice - 1]

        for i, topic in enumerate(subject.measurement_topics):
          print(f"{i+1}. {topic.name}")

        topic_number = int(input("Enter the number of the measurement topic: "))

        topic_index = topic_number - 1
        topic = subject.measurement_topics[topic_index]

        topic_grade = topic.evaluate_letter_grade(subject.holistic)
        topic_grade_point = letter_mark_to_grade_point(topic_grade)

        print(f"Measurement topic grade: {topic_grade}")
        print(f"Measurement topic grade point: {topic_grade_point}")

    elif calculation_choice == "1":
      # Code for calculating subject grade
      subject_index = 0
      for i, subject in enumerate(subjects):
        print(f"{i+1}. {subject.name}")
      subject_choice = int(input("Please enter the number of the subject: "))

      if subject_choice < 1 or subject_choice > len(subjects):
        print("Invalid subject choice. Please try again.")
      else:
        subject = subjects[subject_choice - 1]

        subject_grade = subject.evaluate_letter_grade()
        subject_grade_point = letter_mark_to_grade_point(subject_grade)

        print(f"Subject grade: {subject_grade}")
        print(f"Subject grade point: {subject_grade_point}")

    elif calculation_choice == "2":
      # Code for calculating GPA
      total_grade_points = 0
      total_units = 0

      for subject in subjects:
        subject_grade_point = letter_mark_to_grade_point(subject.evaluate_letter_grade())
        total_grade_points += subject_grade_point * subject.units
        total_units += subject.units

      gpa = total_grade_points / total_units

      print(f"GPA: {gpa}")

    else:
      print("Invalid choice. Please try again.")
    pass
  elif choice == "1":
    # Code for creating a new subject
    name = input("Enter the name of the subject: ")
    units = int(input("Enter the number of units for the subject: "))
    holistic = input("Is the subject holistic? (y/n): ")
    num_measurement_topics = int(input("Enter the number of measurement topics for the subject: "))

    subject = Subject(name, units, holistic.lower() == "y", num_measurement_topics)
    subjects.append(subject)
    print("Subject created successfully.")
  elif choice == "2":
    # Code for creating a new assessment
    subject_index = 0
    for i, subject in enumerate(subjects):
      print(f"{i+1}. {subject.name}")
    subject_choice = int(input("Please enter the number of the subject: "))

    if subject_choice < 1 or subject_choice > len(subjects):
      print("Invalid subject choice. Please try again.")
    else:
      subject = subjects[subject_choice - 1]

      for i, topic in enumerate(subject.measurement_topics):
        print(f"{i+1}. {topic.name}")
        
      topic_number = int(input("Enter the number of the measurement topic: "))
      
      topic_index = topic_number - 1
      topic = subject.measurement_topics[topic_index]

      for number, assessment in topic.assessments.items():
        print(f"Assessment {number}: {assessment.letter_mark}")

      number = str(len(topic.assessments) + 1)
      letter_mark = input("Enter the letter mark: ")
      topic.add_assessment(number, letter_mark)
      print("Assessment added successfully.")
  elif choice == "3":
    print("Exiting...")
    pass
  elif choice == "4":
    # Code for modifying an existing measurement topic
    pass
  elif choice == "5":
    # Code for modifying an existing assessment
    pass
  elif choice == "6":
    # Code for deleting an existing subject
    pass
  elif choice == "7":
    # Code for deleting an existing measurement topic
    pass
  elif choice == "8":
    # Code for deleting an existing assessment
    pass
  elif choice == "9":
    # Exit the program
    break
  else:
    print("Invalid choice. Please try again.")
