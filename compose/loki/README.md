# Loki Configuration

This folder contains the Loki configuration files for centralized log aggregation.

## Files

- `loki-config.yaml` - Main Loki configuration file that defines:
  - Server settings
  - Storage configuration
  - Limits and retention policies
  - Log ingestion rules

## Purpose

Loki serves as the centralized log aggregation system that:
- Receives logs from Promtail
- Stores logs efficiently with indexing
- Provides query interface for Grafana
- Manages log retention and cleanup

## Access

Loki API is available at: http://localhost:3100
