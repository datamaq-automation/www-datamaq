from dataclasses import asdict
import json
import os
from typing import Any, Dict

from src.domain.entities.lead import Lead
from src.domain.repositories.lead_repository import LeadRepository
import logging

logger = logging.getLogger(__name__)


DATA_DIR = "data/leads"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def _lead_to_dict(lead: Lead) -> Dict[str, Any]:
    """Serializa un Lead a un dict compatible con JSON."""
    data = asdict(lead)
    data["id"] = str(lead.id)
    return data


class LeadRepositoryJson(LeadRepository):
    """Implementación de LeadRepository que persiste leads como archivos JSON."""

    async def save(self, lead: Lead) -> None:
        submission_id = str(lead.id)
        lead_path = os.path.join(DATA_DIR, f"{submission_id}.json")

        logger.debug("[LeadRepositoryJson] Guardando lead %s en %s", submission_id, lead_path)

        try:
            with open(lead_path, "w", encoding="utf-8") as f:
                json.dump(_lead_to_dict(lead), f, indent=2, ensure_ascii=False)
            logger.info("[LeadRepositoryJson] Lead %s guardado en %s", submission_id, lead_path)
        except Exception as e:
            logger.error("[LeadRepositoryJson] Fallo al guardar lead %s: %s", submission_id, e)
            raise
