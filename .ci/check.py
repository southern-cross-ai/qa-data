import re
import os
import sys
'''
# @author  : Shiqiding
# @description: This script is used to check that the submitted markdown file conforms to the template's requirements
# @version : V1.0
'''

def check_prompt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Check for the presence of the # Prompt tag
    prompt_match = re.search(r'#\s*Prompt', content)

    if prompt_match:

        # Check for the presence of the #Eg tag
        eg_matches = re.finditer(r'#\s*Eg', content)

        # Eg Counter initialised to 0
        valid_eg_count = 0

        for eg_match in eg_matches:

            # Looking for the next #Eg tag or end of file
            next_eg_match = re.search(r'#\s*Eg', content[eg_match.end():])
            end_of_file = len(content) if not next_eg_match else next_eg_match.start() + eg_match.end()

            # Intercepting content between two #Eg tags
            eg_content = content[eg_match.end():end_of_file]

            # Check that each #Eg is followed by only one ## Q and one ## A
            q_a_matches = re.findall(r'##\s*(Q|A)', eg_content)

            if len(q_a_matches) == 2 and q_a_matches[0] != q_a_matches[1]:
                # If the format is correct, the counter adds 1
                valid_eg_count += 1
            else:
                print(f"Invalid question and answer format. A pair of ## Q ## A tags was not found in the {valid_eg_count+1}th #Eg tag.")
                return False

        print(f"\n Total of {valid_eg_count} valid #Eg examples found.")

    else:
        print("Invalid prompt format. The # Prompt tag was not found.")
        return False



def check_all_prompts(folder_path='fine-tuning-commit'):
    # Get a list of all .md files in the specified folder
    md_files = [file for file in os.listdir(folder_path) if file.endswith('.md')]

    # Loop through each .md file and check the prompt
    for md_file in md_files:
        file_path = os.path.join(folder_path, md_file)
        if check_prompt(file_path)==False:
            print(f"The error is in the {md_file}")
            sys.exit(1)
    print("All files are formatted correctly")
# Call the function with the specified folder path
check_all_prompts()


