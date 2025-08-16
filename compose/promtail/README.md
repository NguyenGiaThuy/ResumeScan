# Promtail Configuration

This folder contains the Promtail configuration files for log collection and forwarding.

## Files

- `promtail-config.yaml` - Main Promtail configuration file that defines:
  - Loki server connection details
  - Log file discovery and scraping rules
  - Docker container log collection
  - Label extraction and processing rules

## Purpose

Promtail serves as the log collection agent that:
- Monitors Docker container logs
- Collects system logs from /var/log
- Processes and labels log entries
- Forwards logs to Loki for storage and indexing

## Log Sources

- Docker container logs via Docker socket
- System logs from /var/log directory
- Application-specific log files
