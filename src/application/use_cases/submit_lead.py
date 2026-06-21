from typing import Any, Dict
from fastapi import BackgroundTasks
from src.domain.models import ContactSubmitPayload
import json
import os
import uuid

DATA_DIR = "data/leads"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


async def persist_lead_task(payload: ContactSubmitPayload, submission_id: str) -> None:
    """Persiste el lead como archivo JSON en disco."""
    lead_path = os.path.join(DATA_DIR, f"{submission_id}.json")
    with open(lead_path, "w", encoding="utf-8") as f:
        json.dump(payload.model_dump(), f, indent=2, ensure_ascii=False)


class SubmitLeadUseCase:
    """Caso de uso que orquesta la recepción y persistencia de un lead."""

    def execute(self, payload: ContactSubmitPayload, background_tasks: BackgroundTasks) -> Dict[str, Any]:
        submission_id = f"lead_{uuid.uuid4().hex[:8]}"
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        background_tasks.add_task(persist_lead_task, payload, submission_id)

        return {
            "requestId": request_id,
            "submissionId": submission_id,
            "submitStatus": "success"
        }
