class LanguageModelException(Exception):
    "The LMM model failed to generate a response."
    pass


class InvalidXMLException(Exception):
    "The LMM model generated an invalid XML response."
    pass


class InvalidTypeException(Exception):
    "The LMM model generated an invalid response type."
    pass