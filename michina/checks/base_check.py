from abc import abstractmethod
from pydantic import BaseModel

class BaseCheck(BaseModel):
    description: str
    
    @abstractmethod
    def check(self, *args, **kwargs):
        """Checks the input and returns a response.
        """