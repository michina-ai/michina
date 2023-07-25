from michina.checks.base_check import BaseCheck
from michina.checks.tone.prompt import TONE_CHECK_TEMPLATE
from michina.exceptions.exceptions import (
    InvalidTypeException,
    InvalidXMLException,
    LanguageModelException,
)
from pydantic import BaseModel

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from dotenv import load_dotenv
from os import environ as env
import xmltodict

load_dotenv()


class ToneCheckInput(BaseModel):
    message: str
    tone: str


class ToneCheckReponse(BaseModel):
    input: ToneCheckInput
    reasoning: str
    judgment: float


class ToneCheck(BaseCheck):
    description: str = (
        "Checks whether the tone of a given message matches the tone provided."
    )

    def check(message: str, tone: str) -> ToneCheckReponse:
        llm = ChatOpenAI(
            temperature=0,
            model="gpt-3.5-turbo",
            openai_api_key=env["OPENAI_API_KEY"],
        )

        prompt = PromptTemplate.from_template(TONE_CHECK_TEMPLATE)
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
            response = ToneCheckReponse(**response["response"])
        except Exception as e:
            raise InvalidTypeException(e)

        return response
