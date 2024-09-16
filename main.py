import json
import atexit

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
  def __init__(self, name, units, holistic, measurement_topics):
    self.name = name
    self.units = units
    self.holistic = holistic
    self.measurement_topics = measurement_topics

  def evaluate_letter_grade(self):
    if self.measurement_topics == []:
      print("No measurement topics to evaluate! :c")
      return

    # return weighted average of measurement topic grades
    total_weighted_grade_point = 0
    total_weight = 0
    for topic in self.measurement_topics:
      topic_grade_point = letter_mark_to_grade_point(topic.evaluate_letter_grade(self.holistic))
      total_weighted_grade_point += topic_grade_point * topic.weight
      total_weight += topic.weight
    
    average_grade_point = total_weighted_grade_point / total_weight
    average_letter_mark = grade_point_to_letter_mark(average_grade_point)
    return average_letter_mark
    
subjects = []
# Read Subjects from data.json
with open('data.json', 'r') as file:
  subjects_data = json.load(file)
  subjects = []
  for subject_data in subjects_data['subjects']:
    name = subject_data['name']
    units = subject_data['units']
    holistic = subject_data['holistic']
    measurement_topics = []
    subject = Subject(name, units, holistic, measurement_topics)
    
    for topic_data in subject_data['measurement_topics']:
      topic_name = topic_data['name']
      topic_weight = topic_data['weight']
      
      topic = MeasurementTopic(topic_name, topic_weight)
      # print(topic_data['assessments']['1']['letter_mark'])
      
      # Add assessments to the topic
      for number, assessment_data in topic_data['assessments'].items():
        letter_mark = assessment_data['letter_mark']

        
        topic.add_assessment(number, letter_mark)
       
      subject.measurement_topics.append(topic)
    
    subjects.append(subject)

# Custom JSON encoder class
class SubjectEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Subject):
      return obj.__dict__
    elif isinstance(obj, MeasurementTopic):
      return obj.__dict__
    elif isinstance(obj, Assessment):
      return obj.__dict__
    return super().default(obj)

# atexit, save subjects to data.json
def save_subjects_data():
  subjects_data = {'subjects': subjects}
  with open('data.json', 'w') as file:
    file.write(json.dumps(subjects_data, cls=SubjectEncoder))

atexit.register(save_subjects_data)

while True:
  print("Please select an option:\n"
    "1. Help\n"
    "2. New subject\n"
    "3. New assessment\n"
    "4. Calculate Grade\n"
    # "5. Modify subject\n"
    # "6. Modify assessment\n"
    # "7. Delete subject\n"
    # "8. Delete assessment\n"
    "9. Exit\n"
    )

  choice = input("Please enter your choice: ")

  if choice == "1":
    # Help
    print("This is a GPA calculator program.")
    print("""To use this program, please create a subject.
          A subject is a course or a module that you are taking, and you must enter: its name, the number of units it is worth, whether it is holistic or not, and the number of measurement topics it has.
          
          A measurement topic is a category of assessment within a subject, and you must enter: its name and its weight for measurement topic within the subject.
          
          An assessment is a graded piece of work within a measurement topic, and you must enter: the number of the assessment and the letter mark you received for the assessment.
          
          You can calculate the grade for a measurement topic, a subject, or your GPA after entering your subjects and assessments.
          
          In summary,
          - Create a subject
            - Enter the name of the subject
            - Enter the number of units the subject is worth
            - Enter whether the subject is holistic or not
            - Enter the number of measurement topics the subject has
              - For each measurement topic, enter the name of the measurement topic and the weight of the measurement topic
          
          - Create an assessment
            - Select the subject
            - Select the measurement topic
            - Enter the number of the assessment
            - Enter the letter mark of the assessment
          
          - Calculate Grade (AFTER entering subjects and assessments)
            - Calculate measurement topic grade
              - Select the subject
              - Select the measurement topic
            - Calculate subject grade
              - Select the subject
            - Calculate GPA
              - No selection required
          """)
  elif choice == "2":
    # Code for creating a new subject
    name = input("Enter the name of the subject: ")
    units = float(input("Enter the number of units for the subject: "))
    holistic = input("Is the subject holistic? (yes/no): ")
    num_measurement_topics = int(input("Enter the number of measurement topics for the subject: "))

    measurement_topics = []
    for i in range(num_measurement_topics):
      topic_name = f"MT{i+1}"
      topic_weight = float(input(f"Enter the weight of measurement topic {i+1}: "))
      topic = MeasurementTopic(topic_name, topic_weight)
      measurement_topics.append(topic)

    subject = Subject(name, units, holistic.lower() == "yes", measurement_topics)
    subjects.append(subject)
    print("Subject created successfully.")
  elif choice == "3":
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
  elif choice == "4":
    calculation_choice = input("Please select an option:\n"
                   "0. Calculate measurement topic grade\n"
                   "1. Calculate subject grade\n"
                   "2. Calculate GPA\n"
                   "Enter your choice: ")

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
        subject_holistic = subject.holistic
        subject_grade_point = letter_mark_to_grade_point(subject.evaluate_letter_grade())
        total_grade_points += subject_grade_point * subject.units
        total_units += subject.units

      gpa = total_grade_points / total_units

      print(f"GPA: {gpa}")

    else:
      print("Invalid choice. Please try again.")
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
    exit()
    break
  else:
    print("Invalid choice. Please try again.")
