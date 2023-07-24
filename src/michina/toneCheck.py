from pydantic import BaseModel
from typing import Union, List

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from dotenv import load_dotenv
from os import environ as env
import xmltodict
from exceptions import InvalidTypeException, InvalidXMLException, LanguageModelException

load_dotenv()

class ToneCheckInput(BaseModel):
    message: str
    tone: str

class ToneCheckReponse(BaseModel):
    input: ToneCheckInput
    reasoning: str
    judgment: float

def toneCheck(message: str, tone: str) -> ToneCheckReponse:
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=env["OPENAI_API_KEY"],
    )

    template = """\
    INSTRUCTIONS:
    You are deciding whether the tone of a given message matches the tone provided. 

    Your goal is to give a point value to the tone match, where 1 is a perfect match, -1 is a perfect mismatch, and 0 is unsure or unrelated.
    How extreme your point value is determines how confident you are in your judgment.

    Think it through step-by-step, then write down your reasoning. Finally, give a point value to the tone match.

    Make sure the judgment is a float between -1 and 1, and the output is a valid XML document.

    INPUT FORMAT:
    <input>
        <message>The message to judge</message>
        <tone>The tone to judge.</tone>
    </input>

    OUTPUT FORMAT:
    <response>
        <input>
            <message>The message to judge</message>
            <tone>The tone to judge</tone>
        </input>
        <reasoning>The reasoning for the judgment</reasoning>
        <judgment>The judgment</judgment>
    </response>

    EXAMPLE INPUT:
    <input>
        <message>I am so happy to see you!</message>
        <tone>happy</tone>
    </input>

    EXAMPLE OUTPUT:
    <response>
        <input>
            <message>I am so happy to see you!</message>
            <tone>happy</tone>
        </input>
        <reasoning>The message contains the word "happy", so it is a perfect match.</reasoning>
        <judgment>1.0</judgment>
    </response>

    EXAMPLE INPUT:
    <input>
        <message>I am so happy to see you!</message>
        <tone>sad</tone>
    </input>
    
    EXAMPLE OUTPUT:
    <response>
        <input>
            <message>I am so happy to see you!</message>
            <tone>sad</tone>
        </input>
        <reasoning>The message contains the word "happy", so it is a perfect mismatch.</reasoning>
        <judgment>-1.0</judgment>
    </response>

    EXAMPLE INPUT:
    <input>
        <message>I am so happy to see you!</message>
        <tone>angry</tone>
    </input>
    
    EXAMPLE OUTPUT:
    <response>
        <input>
            <message>I am so happy to see you!</message>
            <tone>angry</tone>
        </input>
        <reasoning>The message contains the word "happy", so it is a mismatch.</reasoning>
        <judgment>-0.9</judgment>
    </response>
    
    TASK:
    <input>
        <message>{message}</message>
        <tone>{tone}</tone>
    </input>

    OUTPUT:
    """
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        string_response = chain.run(message=message, tone=tone)
    except Exception as e:
        raise LanguageModelException(e)
    
    try:
        response = xmltodict.parse(string_response)
    except Exception as e:
        raise InvalidXMLException(e)
    
    try: 
        response = ToneCheckReponse(**response['response'])
    except Exception as e:
        raise InvalidTypeException(e)
    
    return response