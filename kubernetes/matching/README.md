# Matching Service Helm Chart

This Helm chart deploys the Matching Service, which provides AI-powered Job Description and Resume matching capabilities.

## Description

The Matching Service is a FastAPI-based microservice that analyzes and scores the compatibility between job descriptions and resumes using AI embeddings and language models.

## Prerequisites

- Kubernetes cluster
- Helm 3.x
- ECR access for pulling Docker images
- AWS credentials configured for accessing AI services

## Installation

### Development Environment

```bash
helm install matching . \
  -f values.yaml \
  -f values-ai-elevate-dev.yaml \
  --namespace ai-elevate-dev \
  --create-namespace
```

### Production Environment

```bash
helm install matching . \
  -f values.yaml \
  -f values-production.yaml \
  --namespace ai-elevate-prod \
  --create-namespace
```

## Configuration

### Main Configuration (values.yaml)

- `replicaCount`: Number of pod replicas
- `image.repository`: ECR repository URL
- `image.name`: Docker image name
- `image.tag`: Image tag to deploy
- `service.port`: Service port (default: 8001)
- `service.targetPort`: Container port (default: 8001)
- `resources`: CPU and memory limits/requests
- `healthCheck`: Health check configuration

### Environment-specific Configuration

Environment-specific values are defined in separate files:
- `values-ai-elevate-dev.yaml`: Development environment
- `values-ai-elevate-prod.yaml`: Production environment (to be created)

## Service Endpoints

The matching service exposes the following endpoints:

- `GET /`: Service information and available endpoints
- `GET /health`: Health check endpoint
- `POST /match`: Main matching endpoint for JD-Resume analysis

## Dependencies

The service requires AWS credentials to access:
- Embeddings services (for text vectorization)
- Language models (for analysis and scoring)

## Monitoring

Health checks are configured to monitor:
- Liveness probe: `/health` endpoint
- Readiness probe: `/health` endpoint

## Troubleshooting

### Common Issues

1. **Pod fails to start**: Check AWS credentials and ECR access
2. **Health check failures**: Verify the service is responding on port 8001
3. **Memory issues**: Adjust resource limits based on workload

### Logs

```bash
# View pod logs
kubectl logs -f deployment/matching -n ai-elevate-dev

# View service status
kubectl get svc matching -n ai-elevate-dev
```

## Upgrading

```bash
helm upgrade matching . \
  -f values.yaml \
  -f values-ai-elevate-dev.yaml \
  --namespace ai-elevate-dev
```
