from fastapi import FastAPI
from pydantic import BaseModel
import openai 
import dotenv


api_config = dotenv.dotenv_values('.env')
openai.api_key = api_config['open_api_key']

app = FastAPI()

function_description = [
            {
                "name": "code_snippet_creator",
                "description": "extract corresponding information from given information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "the name of the product name, e.g. Alibaba",
                        },
                        "image": {
                            "type": "string",
                            "description": "the specific link for the image, e.g. http://zylker.com/store/Cliq-wireless-headphones-34433.png",
                        },
                        "url": {
                            "type": "string",
                            "description": "the URL for the product, e.g. http://zylker.com/store/Cliq-wireless-headphones/34452//know-more",
                        },
                        "description": {
                            "type": "string",
                            "description": "the description for the product, e.g. High Peformance Wheat Germ Extract that has been contained an abundance of the translation factors that are required for protein synthesis.",
                        },
                    },
                    "required": ["text","image","url","description"],
                },
            }
        ]

query = """
type: "links",
text: "$Wheat Germ Extract WEPRO7240",
image: "https://resource.amerigoscientific.com/p-img/WEPRO7240.png",
description:"High Peformance Wheat Germ Extract that has been contained an abundance of the translation factors that are required for protein synthesis."
url: "https://www.amerigoscientific.org/wheat-germ-extract-wepro7240-item-237474.html",
text: "Click here to buy"
"""
prompt = f'please extract the information for given context {query}'

response = openai.ChatCompletion.create(
        model = 'gpt-4-0613',
        messages = [{'role':'user','content':prompt}],
        functions=function_description,
        function_call="auto"
    )
# ['message']['function_call']['arguments']
print(response['choices'][0]['message']['function_call']['arguments'])

@app.get('/')
def index():
    return {'hello world'}


class Email(BaseModel):
    content:str


@app.post('/')
def analyze_email(email:Email):
    content = email.content
    prompt = f'please extract the information for given context {content}'

    response = openai.ChatCompletion.create(
        model = 'gpt-4-0613',
        messages = [{'role':'user','content':prompt}],
        functions=function_description,
        function_call="auto"
    )

    val = response.choices[0]['message']['function_call']['arguments']
    textContent = eval(val).get('text')
    imageContent = eval(val).get('image')
    urlContent = eval(val).get('url')
    desContent = eval(val).get('description')

    return {
        "text":textContent,
        "image":imageContent,
        "url":urlContent,
         "description":desContent
    }
