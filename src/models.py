"""Data Contracts and Specification Models for EnerlyAPP Platform."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ServiceStatus(str, Enum):
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    FALLBACK = "FALLBACK"
    OFFLINE = "OFFLINE"


class TariffBand(str, Enum):
    F1_PEAK = "F1"
    F2_MID = "F2"
    F3_OFF_PEAK = "F3"


@dataclass
class MicroserviceHealth:
    """Represents the operational health of an isolated domain microservice."""
    service_name: str
    port: int
    pid: int
    status: ServiceStatus
    uptime_seconds: float
    memory_rss_mb: float


@dataclass
class BillOcrExtract:
    """Sanitized, zero-knowledge energy bill extraction data contract."""
    extract_id: str
    provider_name: str
    billing_period: str
    total_consumption_kwh: float
    band_consumption_kwh: Dict[TariffBand, float]
    committed_power_kw: float
    total_net_amount_eur: float
    pii_sanitized: bool = True
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EnergySimulationForecast:
    """Tri-temporal analytical projection calculated by the Energy Synthesizer."""
    system_capacity_kwp: float
    annual_generation_kwh: float
    self_consumption_rate_percent: float
    annual_grid_export_kwh: float
    projected_annual_savings_eur: float
    estimated_amortization_years: float
    regulatory_compliance: str = "CEI 0-21 / GSE SSP"
    calculation_latency_ms: float = 18.5


@dataclass
class AiModuleTask:
    """Request contract dispatched to iaStudio and AI Gateway."""
    task_id: str
    module_name: str
    prompt_template: str
    sanitized_variables: Dict[str, str]
    model_preference: str = "gemini-pro"
    max_tokens: int = 2048
