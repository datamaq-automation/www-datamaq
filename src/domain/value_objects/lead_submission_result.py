from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LeadSubmissionResult:
    """Resultado de la operación de submit de un lead."""
    request_id: str
    submission_id: str
    lead_saved: bool
    notification_sent: bool
    error_message: Optional[str] = None

    @property
    def submit_status(self) -> str:
        if self.lead_saved and self.notification_sent:
            return "success"
        if self.lead_saved and not self.notification_sent:
            return "partial_success"
        return "failed"
