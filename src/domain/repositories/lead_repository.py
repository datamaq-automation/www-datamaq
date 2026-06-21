from abc import ABC, abstractmethod

from src.domain.entities.lead import Lead


class LeadRepository(ABC):
    """Puerto de persistencia para leads."""

    @abstractmethod
    async def save(self, lead: Lead) -> None:
        """Persiste un lead."""
        raise NotImplementedError
