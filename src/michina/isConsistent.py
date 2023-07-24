"""
This is a module for the Michina test suite.
"""
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from dotenv import load_dotenv
from os import environ as env
import xmltodict

from exceptions import InvalidTypeException, InvalidXMLException, LanguageModelException

load_dotenv()

from pydantic import BaseModel

class IsConsistentInput(BaseModel):
    message: str
    statement: str


class IsConsistentResponse(BaseModel):
    input: IsConsistentInput
    reasoning: str
    judgment: float


def isConsistent(message: str, statement: str) -> IsConsistentResponse:
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
        openai_api_key=env["OPENAI_API_KEY"],
    )

    template = """\
    INSTRUCTIONS:
    You are judging whether a statement about a message is consistent or inconsistent.

    Your goal is to give a point value to the statement, where 1 is very consistent, -1 is very contradictory, and 0 is unsure or unrelated. 
    How extreme your point value is determines how confident you are in your judgment.

    Think through it step-by-step, then write down your reasoning. Finally, give a point value to the statement.

    Make sure the judgment is a float between -1 and 1, and the output is a valid XML document.

    INPUT FORMAT:
    <input>
        <message>The message to judge</message>
        <statement>The statement to judge.</statement>
    </input>

    OUTPUT FORMAT:
    <response>
        <input>
            <message>The message to judge</message>
            <statement>The statement to judge</statement>
        </input>
        <reasoning>The reasoning for the judgment</reasoning>
        <judgment>The judgment to give the statement</judgment>
    </response>

    EXAMPLES:
    <response>
        <input>
            <message>I like dogs.</message>
            <statement>The speaker likes dogs.</statement>
        </input>
        <reasoning>Because the message and the statement both assert the speaker likes dogs, the statement is very consistent with the message, so the score is 1.</reasoning>
        <judgment>1.0</judgment>
    </response>
    
    <response>
        <input>
            <message>I like dogs.</message>
            <statement>The doesn't likes dogs.</statement>
        </input>
        <reasoning>Because the statement directly contradicts the message, the statement is very inconsistent, so the score should be -1.</reasoning>
        <judgment>-1.0</judgment>
    </response>
    
    <response>
        <input>
            <message>I like dogs.</message>
            <statement>The speaker likes cats.</statement>
        </input>
        <reasoning>It's not clear whether the speaker does or does not like cats based on the message, so the statement is unrelated, so the score is 0.</reasoning>
        <judgment>0.0</judgment>
    </response>

    Make sure the judgment is a float between -1 and 1, and the output is a valid XML document.

    TASK:
    <input>
        <message>{message}</message>
        <statement>{statement}</statement>
    <input>

    OUTPUT:
"""
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        string_response = chain.run(message=message, statement=statement)
    except Exception as e:
        raise LanguageModelException(e)

    def postprocessor(path, key, value):
        if key == "judgment":
            return key, float(value)
        else:
            return key, value

    try:
        dict_response = xmltodict.parse(string_response, postprocessor=postprocessor)
    except Exception as e:
        raise InvalidXMLException(e)

    try:
        response = IsConsistentResponse(**dict_response["response"])
    except Exception as e:
        raise InvalidTypeException(e)

    return response
