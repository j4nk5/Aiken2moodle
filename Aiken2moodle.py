import os
import glob
import html
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom


folder_path = os.path.dirname(os.path.abspath(__file__))

def parse_aiken(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    i = 0
    while i < len(lines):
        question_text = lines[i]
        i += 1
        choices = {}
        feedback = ""

        while i < len(lines) and re.match(r'^[A-Z]\.', lines[i]):
            label, text = lines[i].split('.', 1)
            choices[label.strip()] = text.strip()
            i += 1

        if i < len(lines) and lines[i].startswith("ANSWER:"):
            correct = lines[i].split("ANSWER:")[1].strip()
            i += 1
        else:
            raise ValueError(f"Missing ANSWER line after question: {question_text}")

        if i < len(lines) and lines[i].startswith("FEEDBACK:"):
            feedback = lines[i].split("FEEDBACK:")[1].strip()
            i += 1

        questions.append((question_text, choices, correct, feedback))
    
    print(f"Parsed {len(questions)} questions.")
    return questions


def to_moodle_xml(questions, grade_per_question):
    quiz = ET.Element('quiz')
    
    for qtext, choices, correct, feedback in questions:
        question = ET.SubElement(quiz, 'question', type='multichoice')

        name = ET.SubElement(question, 'name')
        text = ET.SubElement(name, 'text')
        text.text = html.escape(qtext[:50])

        questiontext = ET.SubElement(question, 'questiontext', format='html')
        qtext_el = ET.SubElement(questiontext, 'text')
        qtext_el.text = html.escape(qtext)

        # Add general feedback from parsed text
        generalfeedback = ET.SubElement(question, 'generalfeedback', format='html')
        feedback_text = ET.SubElement(generalfeedback, 'text')
        feedback_text.text = html.escape(feedback)

        ET.SubElement(question, 'defaultgrade').text = f"{float(grade_per_question):.7f}"
        ET.SubElement(question, 'single').text = 'true'
        ET.SubElement(question, 'shuffleanswers').text = 'false'
        ET.SubElement(question, 'answernumbering').text = 'ABCD'

        for key, answer in choices.items():
            answer_el = ET.SubElement(
                question, 'answer',
                fraction="100" if key == correct else "0"
            )
            answer_text = ET.SubElement(answer_el, 'text')
            answer_text.text = html.escape(answer)

            feedback_el = ET.SubElement(answer_el, 'feedback')
            ftext = ET.SubElement(feedback_el, 'text')
            ftext.text = ''

    rough_string = ET.tostring(quiz, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def quizbreaker(folder_path):
    import os

    files = []
    for root, dirs, filenames in os.walk(folder_path):
        # Skip folders named "ready" and artaiken
        if 'ready' in root.lower().split(os.sep):
            continue
        if 'artaiken' in root.lower().split(os.sep):
            continue

        for filename in filenames:
            if (
                filename.lower().startswith('quiz') or
                filename.lower().startswith('kouiz')
            ) and filename.lower().endswith('.txt'):
                files.append(os.path.join(root, filename))

    if not files:
        print("No matching quiz files found.")
        return

    for file in files:
        print(f"\n📄 File: {file}")
        while True:
            grade_input = input("👉 Enter the default grade for this file: ")
            try:
                grade = float(grade_input)
                break
            except ValueError:
                print("❌ Please enter a valid number.")

        questions = parse_aiken(file)
        xml_data = to_moodle_xml(questions, grade)

        output_file = os.path.splitext(file)[0] + ".xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_data)

        print(f"✅ XML saved to: {output_file}")


# Call function on the folder with quiz files
quizbreaker(os.path.dirname(os.path.abspath(__file__)))