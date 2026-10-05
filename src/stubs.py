"""Encapsulated Service Stubs and Specification Implementations for EnerlyAPP.

Note: Certified GSE economic constants, Italian grid code lookup tables (CEI 0-21),
and production server credentials are encapsulated in the private production binary.
These stubs demonstrate architectural routing, data contracts, and failover mechanics.
"""

from datetime import datetime
from typing import Dict, List, Optional
from .interfaces import (
    IIngressApiGateway,
    IZeroKnowledgeOcrParser,
    IEnergySynthesizer,
    IAiGatewayOrchestrator,
    IMcpSupervisor,
)
from .models import (
    MicroserviceHealth,
    ServiceStatus,
    BillOcrExtract,
    TariffBand,
    EnergySimulationForecast,
    AiModuleTask,
)


class IngressApiGatewayStub(IIngressApiGateway):
    """Central Gateway coordinating routing to decoupled Node.js microservices."""

    def __init__(self):
        self.registered_services = {
            "securityService": 3010,
            "usersData": 3011,
            "usersLive": 3012,
            "iaStudio": 3013,
            "usersGuide": 3014,
            "adminService": 3015,
        }

    def route_request(self, path: str, method: str, payload: Optional[Dict] = None) -> Dict:
        """Emulates path matching and downstream dispatching with fallback handling."""
        if path.startswith("/api/scan/bill"):
            return {"status": "dispatched", "target": "usersData:3011", "endpoint": "parse_ocr"}
        elif path.startswith("/api/stream/live"):
            return {"status": "dispatched", "target": "usersLive:3012", "endpoint": "sse_telemetry"}
        elif path.startswith("/api/ai/synthesize"):
            return {"status": "dispatched", "target": "iaStudio:3013", "endpoint": "prompt_exec"}
        return {"status": "ok", "message": f"Routed {method} {path} via Ingress Gateway"}

    def get_cluster_health(self) -> List[MicroserviceHealth]:
        """Returns health diagnostics for all monitored microservices."""
        return [
            MicroserviceHealth("securityService", 3010, 10241, ServiceStatus.ONLINE, 86400.0, 48.2),
            MicroserviceHealth("usersData", 3011, 10242, ServiceStatus.ONLINE, 86400.0, 62.4),
            MicroserviceHealth("usersLive", 3012, 10243, ServiceStatus.ONLINE, 86400.0, 54.1),
            MicroserviceHealth("iaStudio", 3013, 10244, ServiceStatus.ONLINE, 86400.0, 78.5),
            MicroserviceHealth("usersGuide", 3014, 10245, ServiceStatus.ONLINE, 86400.0, 32.0),
            MicroserviceHealth("adminService", 3015, 10246, ServiceStatus.ONLINE, 86400.0, 39.7),
        ]


class ZeroKnowledgeOcrParserStub(IZeroKnowledgeOcrParser):
    """Parses energy bill data in memory, purging PII before returning numeric fields."""

    def parse_document_stream(self, document_bytes: bytes, filename: str) -> BillOcrExtract:
        # In production, this executes client-side memory tokenizers and regex sanitization.
        return BillOcrExtract(
            extract_id="OCR_SANITIZED_202610_01",
            provider_name="Enel Energia S.p.A.",
            billing_period="Bimestre Luglio - Agosto",
            total_consumption_kwh=420.0,
            band_consumption_kwh={
                TariffBand.F1_PEAK: 140.0,
                TariffBand.F2_MID: 160.0,
                TariffBand.F3_OFF_PEAK: 120.0,
            },
            committed_power_kw=4.5,
            total_net_amount_eur=126.80,
            pii_sanitized=True,
        )


class EnergySynthesizerStub(IEnergySynthesizer):
    """Tri-temporal analytical engine calculating solar yield and ROI according to CEI 0-21."""

    def synthesize_scenario(
        self,
        historical_consumption_kwh: float,
        system_capacity_kwp: float,
        storage_capacity_kwh: float,
    ) -> EnergySimulationForecast:
        # Deterministic formula simulating Italian irradiation & self-consumption
        annual_yield = system_capacity_kwp * 1350.0  # ~1350 kWh/kWp Central/Southern Italy average
        self_consumption_ratio = min(0.85, (storage_capacity_kwh * 0.05) + 0.55)
        self_consumed_kwh = annual_yield * self_consumption_ratio
        grid_export_kwh = annual_yield - self_consumed_kwh

        annual_savings = (self_consumed_kwh * 0.28) + (grid_export_kwh * 0.10)
        system_cost = (system_capacity_kwp * 1100.0) + (storage_capacity_kwh * 450.0)
        payback_years = system_cost / annual_savings if annual_savings > 0 else 99.0

        return EnergySimulationForecast(
            system_capacity_kwp=system_capacity_kwp,
            annual_generation_kwh=round(annual_yield, 1),
            self_consumption_rate_percent=round(self_consumption_ratio * 100, 1),
            annual_grid_export_kwh=round(grid_export_kwh, 1),
            projected_annual_savings_eur=round(annual_savings, 2),
            estimated_amortization_years=round(payback_years, 1),
            regulatory_compliance="CEI 0-21 / GSE Scambio sul Posto",
            calculation_latency_ms=16.8,
        )
