#!/usr/bin/env python3
"""EnerlyAPP Architectural Showcase - Standalone Simulation Demo.

Demonstrates:
1. Ingress API Gateway initialization and microservices routing.
2. Local-first Zero-Knowledge OCR parsing of energy bills.
3. Tri-temporal Energy Synthesizer calculation under Italian CEI 0-21 / GSE model.
4. Model Context Protocol (MCP) inspection tool call by an AI Agent.
"""

import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add package root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.stubs import IngressApiGatewayStub, ZeroKnowledgeOcrParserStub, EnergySynthesizerStub
from src.mcp_spec import EnerlyAppMcpProvider


def run_simulation():
    print("=" * 70)
    print("  ENERLYAPP (ENERGYLIFE) ARCHITECTURAL SHOWCASE -- SIMULATION DEMO")
    print("  Author: Alessandro Caliciotti (@RedScorpio83)")
    print("=" * 70)

    # 1. Initialize Ingress Gateway & Core Stubs
    print("\n[1/4] Initializing Ingress API Gateway (Port 3001) & 6 Domain Microservices...")
    gateway = IngressApiGatewayStub()
    ocr_parser = ZeroKnowledgeOcrParserStub()
    synthesizer = EnergySynthesizerStub()
    mcp_provider = EnerlyAppMcpProvider(gateway)
    print("      [OK] Ingress Gateway up on port 3001 with in-process failover fallback.")

    # 2. Simulate Local-First Zero-Knowledge OCR parsing
    print("\n[2/4] Parsing Energy Bill via Zero-Knowledge OCR In-Memory Pipeline...")
    bill = ocr_parser.parse_document_stream(b"%PDF-1.4...", "bolletta_luglio_agosto.pdf")
    print(f"      • Provider:           {bill.provider_name}")
    print(f"      • Total Consumption:  {bill.total_consumption_kwh:.1f} kWh ({bill.billing_period})")
    print(f"      • Peak Power Meter:   {bill.committed_power_kw} kW")
    print(f"      • Net Expenditure:    € {bill.total_net_amount_eur:.2f}")
    print(f"      • Privacy Guard:      PII Sanitized = {bill.pii_sanitized} (Zero PII forwarded to LLM)")

    # 3. Simulate Tri-Temporal Energy Synthesizer Calculation
    print("\n[3/4] Executing Tri-Temporal Energy Synthesizer (Italian Regulatory CEI 0-21 Model)...")
    sim = synthesizer.synthesize_scenario(
        historical_consumption_kwh=bill.total_consumption_kwh * 6,  # Annualized (~2520 kWh)
        system_capacity_kwp=6.0,  # 6 kWp photovoltaic setup
        storage_capacity_kwh=10.0, # 10 kWh battery storage
    )
    print(f"      • Planned Capacity:   {sim.system_capacity_kwp} kWp (Storage: 10 kWh)")
    print(f"      • Estimated Yield:    {sim.annual_generation_kwh} kWh/year")
    print(f"      • Self-Consumption:   {sim.self_consumption_rate_percent}%")
    print(f"      • Annual Net Savings: € {sim.projected_annual_savings_eur:.2f} / year")
    print(f"      • Estimated Payback:  {sim.estimated_amortization_years} years")
    print(f"      • Engine Latency:     {sim.calculation_latency_ms} ms (Deterministic 0-AI fallback)")

    # 4. Model Context Protocol Tool Execution by AI Agent
    print("\n[4/4] Model Context Protocol (MCP) Execution by AI Agent...")
    print("      Agent calls tool: 'energylife_cluster_health'")
    health_resp = mcp_provider.handle_tool_call("energylife_cluster_health", {})
    print(f"      Cluster Status: {health_resp['overall_status']} ({health_resp['total_services']} services online on CT 116)")

    print("\n      Agent calls tool: 'energylife_architecture_schema'")
    schema_resp = mcp_provider.handle_tool_call("energylife_architecture_schema", {})
    print(f"      Deployment Target: {schema_resp['deployment']}")
    print(f"      Gateway Config:    {schema_resp['gateway']}")

    print("\n" + "=" * 70)
    print("  SIMULATION COMPLETED WITH SUCCESS!")
    print("=" * 70)


if __name__ == "__main__":
    run_simulation()
