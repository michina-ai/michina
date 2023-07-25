"""
This is a module for the Michina test suite.
"""
from michina.checks.base_check import BaseCheck
from michina.exceptions.exceptions import InvalidTypeException, InvalidXMLException, LanguageModelException
from michina.checks.consistency.prompt import CONSISTENCY_CHECK_TEMPLATE
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from dotenv import load_dotenv
from os import environ as env
import xmltodict
from pydantic import BaseModel

load_dotenv()

class IsConsistentInput(BaseModel):
    message: str
    statement: str


class IsConsistentResponse(BaseModel):
    input: IsConsistentInput
    reasoning: str
    judgment: float

class ConsistencyCheck(BaseCheck):
    def check(message: str, statement: str) -> IsConsistentResponse:
        llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=env["OPENAI_API_KEY"],
        )

        prompt = PromptTemplate.from_template(CONSISTENCY_CHECK_TEMPLATE)
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
