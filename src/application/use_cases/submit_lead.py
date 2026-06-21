from dataclasses import asdict
from typing import Any, Dict
from fastapi import BackgroundTasks
from src.domain.models import ContactSubmitPayload
from src.domain.entities.lead import Lead, LeadId
from src.domain.value_objects.contact_info import ContactInfo
import json
import os
import uuid

DATA_DIR = "data/leads"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def _lead_to_dict(lead: Lead) -> Dict[str, Any]:
    """Serializa un Lead a un dict compatible con JSON."""
    data = asdict(lead)
    data["id"] = str(lead.id)
    return data


async def persist_lead_task(lead: Lead, submission_id: str) -> None:
    """Persiste el lead como archivo JSON en disco."""
    lead_path = os.path.join(DATA_DIR, f"{submission_id}.json")
    with open(lead_path, "w", encoding="utf-8") as f:
        json.dump(_lead_to_dict(lead), f, indent=2, ensure_ascii=False)


def _map_payload_to_lead(payload: ContactSubmitPayload) -> Lead:
    """Traduce el payload de entrada en una entidad de dominio Lead."""
    return Lead(
        id=LeadId(),
        contact=ContactInfo(
            name=payload.name,
            first_name=payload.firstName,
            last_name=payload.lastName,
            email=payload.email,
            phone=payload.phone,
            company=payload.company,
        ),
        comment=payload.comment,
        preferred_contact_channel=payload.preferredContactChannel,
        page_location=payload.pageLocation,
        traffic_source=payload.trafficSource,
        user_agent=payload.userAgent,
        geographic_location=payload.geographicLocation,
        created_at=payload.createdAt,
        captcha_token=payload.captchaToken,
    )


class SubmitLeadUseCase:
    """Caso de uso que orquesta la recepción y persistencia de un lead."""

    def execute(self, payload: ContactSubmitPayload, background_tasks: BackgroundTasks) -> Dict[str, Any]:
        lead = _map_payload_to_lead(payload)
        submission_id = str(lead.id)
        request_id = f"req_{uuid.uuid4().hex[:8]}"

        background_tasks.add_task(persist_lead_task, lead, submission_id)

        return {
            "requestId": request_id,
            "submissionId": submission_id,
            "submitStatus": "success"
        }
