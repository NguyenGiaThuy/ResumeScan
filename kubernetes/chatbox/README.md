# Chatbox Helm Chart

This Helm chart deploys the AI Elevate Chatbox service, which is a Streamlit-based interview system frontend.

## Overview

The Chatbox service provides an interactive user interface for the AI Elevate interview system. It's built using Streamlit and runs on port 8501.

## Configuration

### Image Configuration

- **Repository**: `058264469194.dkr.ecr.ap-southeast-1.amazonaws.com`
- **Image Name**: `ai-elevate/chatbox`
- **Default Tag**: `0.0.1`

### Service Configuration

- **Type**: ClusterIP
- **Port**: 8501
- **Target Port**: 8501

### Health Checks

The chart includes health checks using Streamlit's built-in health endpoint:
- **Path**: `/_stcore/health`
- **Initial Delay**: 30 seconds
- **Period**: 10 seconds

### Resources

Default resource limits and requests:
- **Limits**: 500m CPU, 1Gi Memory
- **Requests**: 250m CPU, 512Mi Memory

## Installation

### Development Environment

```bash
helm install chatbox ./chatbox \
  -f chatbox/values.yaml \
  -f chatbox/values-ai-elevate-dev.yaml \
  -n ai-elevate-dev
```

### Upgrade

```bash
helm upgrade chatbox ./chatbox \
  -f chatbox/values.yaml \
  -f chatbox/values-ai-elevate-dev.yaml \
  -n ai-elevate-dev
```

## Customization

### Environment Variables

Add environment variables in the values file:

```yaml
env:
  CUSTOM_VAR: "custom_value"
```

### Secrets

Mount secrets by configuring the secrets array:

```yaml
secrets:
  - name: "chatbox-secret"
    mountPath: "/secrets"
```

### ConfigMaps

Mount configuration files:

```yaml
configs:
  - name: "chatbox-config"
    mountPath: "/configs"
```

## Dependencies

This service may require:
- Access to other AI Elevate services (graph, db-integration)
- Proper network policies for inter-service communication
- ECR registry access for image pulling
