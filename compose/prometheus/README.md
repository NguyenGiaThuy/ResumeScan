# Prometheus Configuration

This folder contains the Prometheus configuration files for the AI Elevate monitoring stack.

## Files

- `prometheus.yaml` - Main Prometheus configuration file that defines:
  - Scrape intervals and evaluation rules
  - Target endpoints for metrics collection
  - Service discovery configuration
  - Job configurations for all monitored services

## Services Monitored

- Prometheus itself (self-monitoring)
- OpenTelemetry Collector
- Grafana
- Redis
- ChromaDB
- Chatbox application
- DB Integration service

## Access

Prometheus web UI is available at: http://localhost:9090
