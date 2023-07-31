import openai

openai.api_key = "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"

def get_model_response(prompt):
    responses = []
    for _ in range(1):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful coding assistant.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        responses.append(response)
    
    print(f"Obtained {len(responses)} responses from GPT-3.5")
    return responses

def clean_responses(responses):
    cleaned = []
    for res in responses:
        response_text = res['choices'][0]['message']['content']
        start = response_text.find("```")
        end = response_text.rfind("```")
        code = response_text[start+3:end].strip() if start != -1 and end != -1 else ""
        
        # Replace "python" and "Python" with empty string
        code = code.replace('python', '')
        code = code.replace('Python', '')
        
        cleaned.append(code)
    
    print(f"Cleaned {len(cleaned)} responses")
    return cleaned

def write_files(cleaned_response, i):
    test_code = '''

assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
assert has_close_elements([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
assert has_close_elements([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
assert has_close_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
assert has_close_elements([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False
'''  # your test code goes here
    with open(f'Number{i+1}.py', 'w') as f:
        f.write(cleaned_response + test_code)

    print(f"Wrote file Number{i+1}.py")
    return None

import subprocess
import csv

import os

def run_files():
    results = []
    for i in range(1, 201):
        result = os.system(f"python3 Number{i}.py")  # a non-zero exit code indicates an error
        status = "Passed" if result == 0 else "Failed"
        results.append((f"Number{i}.py", status))

    with open('results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    print("CSV file with results created.")
    return None

def count_pass():
    with open('results.csv', 'r') as f:
        reader = csv.reader(f)
        passed_count = sum(1 for row in reader if row[1] == "Passed")
    return passed_count

def main():
    request = """from typing import List def has_close_elements(numbers: List[float], threshold: float) -> bool: "" Check if in given list of numbers, are any two numbers closer to each other than given threshold. >>> has_close_elements([1.0, 2.0, 3.0], 0.5) False >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) True "". Please solve this request with one block of code delimited by triple back-ticks."""
    
    for i in range(200):      
        responses = get_model_response(request)  # gets one response at a time
        cleaned_response = clean_responses(responses)[0]  # takes the first and only cleaned response
        write_files(cleaned_response, i)  # write file with the current index
    
    run_files()  # after creating all files, run them and create the csv 

    print(f"Number of passed: {count_pass()}")
        
if __name__ == "__main__":
    main()