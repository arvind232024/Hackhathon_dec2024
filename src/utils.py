import time
import json
from dotenv import load_dotenv
from pypdf import PdfReader
import yaml
from importlib.resources import files
from src.schema import ModelInput,ModelOutput
import os
import openai
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key)


def load_yaml_config(config_file: str):
    # print(config_file)
    config_file = files('config').joinpath(config_file)
    # print(config_file)
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise Exception(f"Configuration file '{config_file}' not found.")
    except yaml.YAMLError as e:
        raise Exception(f"Error parsing the YAML file: {e}")
    


def read_document(file_path)->dict:
    """ Read all the pages of document 
    return a dict of text with page number as keys"""
    doc_content=""
    reader = PdfReader(file_path)

    # Get the total number of pages
    num_pages = len(reader.pages)
    # print(f"Total Pages: {num_pages}")

    doc_content = dict()
    # Loop through all pages and extract text
    for page_num in range(num_pages):
        page = reader.pages[page_num]  # Get a specific page
        text = page.extract_text()    # Extract text from the page
        doc_content[f"page_{page_num}"] = text
        # print(f"{page_num} \n {text}")

        # print(e)    
    return {"error":"","data":doc_content}


def extract_all_functionalies_testcases(application_input):
    doc_path=application_input.doc_path
    application_url = application_input.application_url
    document_content = read_document(doc_path)

    # load prompts
    prompt_file = "prompt_config.yaml"

    prompts = load_yaml_config(prompt_file)
    output_format = """ {
    "modules": [
        {
            "id": "ATC-1",
            "name": "Module 1 - User 1"
        },
        {
            "id": "ATC-2",
            "name": "Module 1 - User 2"
        },
        {
            "id": "ATC-3",
            "name": "Module 1 - User 3"
        },
        {
            "id": "ATC-4",
            "name": "Module 2 - User 1"
        },
        {
            "id": "ATC-5",
            "name": "Module 2 - User 2"
        },
        {
            "id": "ATC-6",
            "name": "Module 2 - User 3"
        }
    ]
}
"""
    extract_module_prompt = prompts["module_extraction"]
    system_prompt = extract_module_prompt["system_prompt"]
    user_prompt = extract_module_prompt["user_prompt"].format(document_content=document_content,output_format=output_format)

    result = extract_all_modules(system_prompt=extract_module_prompt["system_prompt"],user_prompt=extract_module_prompt["user_prompt"].format(document_content=document_content,output_format=output_format))

    print("---result----")

    print(result)

    final_list = json.loads(result)

    return {"error":"","data":final_list}


def extract_all_modules(user_prompt:str, system_prompt:str):
    # print(user_prompt)
    # response = openai.chat.completions.create({
    #             model: "gpt-4o",
    #             messages: [
    #                 { role: "system", content: system_prompt},
    #                 {
    #                     role: "user",
    #                     content: user_prompt,
    #                 },
    #             ],
    #         })
    
    # response=openai.chat.completions.create(model="gpt-4",
    #                                         messages= [
    #                 { "role": "system", "content": system_prompt},
    #                 {
    #                     "role": "user",
    #                     "content": user_prompt,
    #                 },
    #             ], response_format=ModelOutput)
    response = openai.beta.chat.completions.parse(model="gpt-4o-2024-08-06",
                                            messages= [
                    { "role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ], response_format=ModelOutput)

    # response=openai.chat.completions.create(model="gpt-4",
    #                                         messages= [
    #                 { "role": "system", "content": system_prompt},
    #                 {
    #                     "role": "user",
    #                     "content": user_prompt,
    #                 },
    #             ], response_format=ModelOutput)

# Output the result
    # print("---response----")
    # print(response)
    result = response.choices[0].message.content
    # print(type(result))
    # print(result["input"])

# Extract and return the response from the model
    # result =  response['choices'][0]['message']['content']
   
    return result

