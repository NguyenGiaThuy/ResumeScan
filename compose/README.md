# Docker Compose Setup

## Start docker compose

```sh
docker compose up -d --build --remove-orphans
```

## Configuration Structure

The monitoring and logging configuration files are organized in separate folders:

- `prometheus/` - Prometheus metrics collection configuration
- `loki/` - Loki log aggregation configuration  
- `promtail/` - Promtail log collection configuration
- `grafana/` - Grafana dashboard and datasource configuration
- `otel-collector/` - OpenTelemetry Collector configuration

## Services

### Monitoring Stack
- **Prometheus** (port 9090) - Metrics collection and monitoring
- **Grafana** (port 3000) - Visualization and dashboards (admin/admin)
- **Loki** (port 3100) - Log aggregation
- **Promtail** - Log collection agent

### Application Services  
- **PostgreSQL** (port 5432) - Database
- **ChromaDB** (port 8000) - Vector database
- **Redis** (port 6379) - Cache
- **Chatbox** (port 8501) - Chat application
- **DB Integration** (port 8088) - Database integration service

### Management
- **Adminer** (port 8080) - Database management
- **Zipkin** (port 9411) - Distributed tracing
