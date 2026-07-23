"""
Reason for the base class:
- without base class all the collectors behaves differently.
- With baseclass everything is consistent.

"""

from abc import ABC, abstractmethod
from state.models import Article

class BaseCollector(ABC):
    """ Base class for all collectors. 
        Every collector must implement the collect() method.
    """

    @abstractmethod
    def collect(self) -> list[Article]:
        """ 
        Fetch articles from the source.

        Returns:
          list[Article] 
        
        """
        pass