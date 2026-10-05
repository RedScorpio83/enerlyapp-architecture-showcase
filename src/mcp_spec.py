"""Model Context Protocol (MCP) Interface Specification for EnerlyAPP Platform.

Provides audited architectural inspection and deployment telemetry to AI Agents.
"""

from typing import Dict, List
from .stubs import IngressApiGatewayStub


class EnerlyAppMcpProvider:
    """Exposes high-level platform status and architectural metadata to AI models."""

    def __init__(self, gateway: IngressApiGatewayStub):
        self.gateway = gateway

    def get_available_tools(self) -> List[Dict]:
        return [
            {
                "name": "energylife_architecture_schema",
                "description": "Returns full microservice topology, port maps, and gateway routes for EnerlyAPP.",
                "parameters": {"type": "object", "properties": {}},
            },
            {
                "name": "energylife_cluster_health",
                "description": "Polls real-time operational state of all 6 decoupled microservices on Proxmox CT 116.",
                "parameters": {"type": "object", "properties": {}},
            },
        ]

    def handle_tool_call(self, tool_name: str, arguments: Dict) -> Dict:
        if tool_name == "energylife_architecture_schema":
            return {
                "platform": "EnerlyAPP (EnergyLife)",
                "deployment": "Proxmox LXC Container CT 116 (192.168.10.101)",
                "gateway": "Ingress API Gateway on Port 3001 (ingress.cjs)",
                "microservices_count": 6,
                "services": [
                    {"name": "securityService", "port": 3010, "scope": "Auth / OAuth / JWT"},
                    {"name": "usersData", "port": 3011, "scope": "Profiles / Inverters / Bill OCR"},
                    {"name": "usersLive", "port": 3012, "scope": "SSE Telemetry Feeds"},
                    {"name": "iaStudio", "port": 3013, "scope": "AI Orchestration"},
                    {"name": "usersGuide", "port": 3014, "scope": "Documentation & Wiki"},
                    {"name": "adminService", "port": 3015, "scope": "Isolated Administration"},
                ],
                "database": "PostgreSQL 16 Alpine in Docker (Port 5432)",
            }
        elif tool_name == "energylife_cluster_health":
            health = self.gateway.get_cluster_health()
            return {
                "overall_status": "HEALTHY",
                "total_services": len(health),
                "services": [
                    {
                        "name": s.service_name,
                        "port": s.port,
                        "status": s.status.value,
                        "memory_rss_mb": s.memory_rss_mb,
                    }
                    for s in health
                ],
            }
        raise ValueError(f"Unknown MCP Tool: {tool_name}")
