import json
import re
import os
'''
# @author  : Shiqiding
# @description: This script is used within the CI to convert checked markdown into data available for fine-tuning.
# @version : V1.0
'''
def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pattern = r'#Eg\n(## Q\n.*?\n## A\n.*?\n)'
    matches = re.findall(pattern, content, re.DOTALL)

    data = []

    for match in matches:
        conversation = {
            "conversation": []
        }

        qa_pair = re.findall(r'## Q\n(.*?)\n## A\n(.*?)\n', match, re.DOTALL)
        for question, answer in qa_pair:
            conversation["conversation"].append({"input": question.strip(), "output": answer.strip()})

        data.append(conversation)

    return data


source_folder = 'fine-tuning-commit'
target_folder = 'fine-tuning-data'

# Create the destination folder (if it does not exist)
os.makedirs(target_folder, exist_ok=True)

# Traverse all .md files in the source folder and its subfolders
for root, dirs, files in os.walk(source_folder):
    for filename in files:
        if filename.endswith('.md'):
            # Build the source and target file paths
            source_path = os.path.join(root, filename)
            relative_path = os.path.relpath(source_path, source_folder)
            target_path = os.path.join(target_folder, relative_path[:-3] + '.json')

            # Create the destination folder (if it does not exist)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            # Extract data and write to JSON file (overwrite mode)
            extracted_data = extract_content(source_path)
            with open(target_path, 'w', encoding='utf-8') as output_file:
                json.dump(extracted_data, output_file, indent=2, ensure_ascii=False)

            print(f"JSON data has been written {target_path}")
