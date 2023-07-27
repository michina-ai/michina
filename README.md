# Michina
From the quechua word for "pasture".

Unit testing and integration testing for LLMs.

## Features
- [openai] Can run in a Github Actions for workflow

## Todo
- Add monitoring

## Versions

### v0.1.1 -> v0.2.0
This change allows you to configure the OpenAI model version to use.

The API was like this
```python
from src.prompts import check_for_political_content, respond_to_customer
from michina.checks import ToneCheck, ConsistencyCheck

"""
This is a consistency check. It tests whether your prompt's output 
is consistent with the goal of the test itself.
"""
def test_check_for_political_content_consistent():
    message = "I want to buy a campaign poster for Obama."
    statement = check_for_political_content(message)
    response = ConsistencyCheck.check(message, statement)
    assert response.judgment > 0.5
```
and now it's like this
```python
from src.prompts import check_for_political_content, respond_to_customer
from michina.checks import ToneCheck, ConsistencyCheck
from os import environ as env

michina_config = {
    'model': 'gpt-3.5-turbo',
    'temperature': 0,
    'openai_api_key': env["OPENAI_API_KEY"],
}

consistency = ConsistencyCheck(**michina_config)

def test_check_for_political_content_consistent():
    message = "I want to buy a campaign poster for Obama."
    statement = check_for_political_content(message)
    response = consistency.check(message, statement)
    assert response.judgment > 0.5
```