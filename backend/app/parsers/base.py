from abc import ABC, abstractmethod
from typing import List, Any
from app.models.schemas import ActionNode

class BaseParser(ABC):
    @abstractmethod
    def parse(self, source_code: str) -> List[ActionNode]:
        """Parse source code and return a list of sequential action nodes."""
        pass
