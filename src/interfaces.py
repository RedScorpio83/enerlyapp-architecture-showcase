"""Abstract Architectural Interfaces and Protocols for EnerlyAPP Platform."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from .models import (
    MicroserviceHealth,
    BillOcrExtract,
    EnergySimulationForecast,
    AiModuleTask,
)


class IIngressApiGateway(ABC):
    """Abstract contract for the Central Ingress Gateway (Port 3001)."""

    @abstractmethod
    def route_request(self, path: str, method: str, payload: Optional[Dict] = None) -> Dict:
        """Dispatches incoming request to target microservice with in-process failover fallback."""
        pass

    @abstractmethod
    def get_cluster_health(self) -> List[MicroserviceHealth]:
        """Polls health probes across all active microservices."""
        pass


class IZeroKnowledgeOcrParser(ABC):
    """Local-first parser stripping PII before emitting energy bill metrics."""

    @abstractmethod
    def parse_document_stream(self, document_bytes: bytes, filename: str) -> BillOcrExtract:
        """Extracts strictly technical & numerical consumption data, purging personal info."""
        pass


class IEnergySynthesizer(ABC):
    """Tri-temporal deterministic computation engine (Past, Present, Future)."""

    @abstractmethod
    def synthesize_scenario(
        self,
        historical_consumption_kwh: float,
        system_capacity_kwp: float,
        storage_capacity_kwh: float,
    ) -> EnergySimulationForecast:
        """Executes zero-latency CEI 0-21 / GSE financial and yield simulations."""
        pass


class IAiGatewayOrchestrator(ABC):
    """Multi-provider LLM gateway orchestrating prompts, rate limits, and task pipelines."""

    @abstractmethod
    def execute_prompt_task(self, task: AiModuleTask) -> Dict:
        """Routes prompt to appropriate AI model with context compression."""
        pass


class IMcpSupervisor(ABC):
    """Model Context Protocol interface exposing platform introspection to AI Agents."""

    @abstractmethod
    def get_architecture_schema(self) -> Dict:
        """Returns topological schema of the platform and service mapping."""
        pass

    @abstractmethod
    def query_proxmox_lxc_state(self) -> Dict:
        """Inspects status of the host container CT 116."""
        pass
