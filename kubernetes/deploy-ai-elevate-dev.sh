#!/bin/bash

# AI Elevate Deployment Script for DEV env

set -e

# Namespace
NAMESPACE="ai-elevate-dev"

# Configurations
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Utility functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

main() {
    log_info "Updating Rancher..."

    # Deploy rancher
    log_info "Deploying rancher..."
    helm -n cattle-system upgrade --install rancher rancher/ \
        -f rancher/values.yaml \
        -f rancher/values-custom.yaml
    
    log_info "Starting AI Elevate development deployment..."
    
    # Create namespace
    log_info "Checking if namespace ${NAMESPACE} exists..."
    if kubectl get namespace ${NAMESPACE} &> /dev/null; then
        log_info "Namespace ${NAMESPACE} already exists, skipping creation"
    else
        log_info "Creating namespace ${NAMESPACE}..."
        kubectl create namespace ${NAMESPACE}
        log_info "Namespace ${NAMESPACE} created successfully"
    fi

    # Deploy ecr-token-renew
    log_info "Deploying ecr-token-renew..."
    helm -n ${NAMESPACE} upgrade --install ecr-token-renew ecr-token-renew/ \
        -f ecr-token-renew/values.yaml \
        -f ecr-token-renew/values-${NAMESPACE}.yaml

    # Deploy Chromadb
    log_info "Deploying Chromadb..."
    helm -n ${NAMESPACE} upgrade --install chromadb chromadb/ \
        -f chromadb/values.yaml \
        -f chromadb/values-${NAMESPACE}.yaml

    # Deploy Postgres (CNPG)
    if ! kubectl get deployment cnpg-controller-manager -n cnpg-system &> /dev/null; then
        log_info "CNPG operator not found, installing..."
        kubectl apply --server-side -f ./postgres/postgres-operator/
    else
        log_info "CNPG operator already exists, skipping installation"
    fi
    log_info "Deploying Postgres..."
    helm -n ${NAMESPACE} upgrade --install postgres postgres/ \
        -f postgres/values.yaml \
        -f postgres/values-${NAMESPACE}.yaml
    
    # Deploy db-integration
    log_info "Deploying db-integration..."
    helm -n ${NAMESPACE} upgrade --install db-integration db-integration/ \
        -f db-integration/values.yaml \
        -f db-integration/values-${NAMESPACE}.yaml
    
    # Deploy minio
    log_info "Deploying minio..."
    helm -n ${NAMESPACE} upgrade --install minio minio/ \
        -f minio/values.yaml \
        -f minio/values-${NAMESPACE}.yaml

    # Deploy graph
    log_info "Deploying graph..."
    helm -n ${NAMESPACE} upgrade --install graph graph/ \
        -f graph/values.yaml \
        -f graph/values-${NAMESPACE}.yaml

    # Deploy ingress-nginx
    log_info "Deploying ingress-nginx..."
    helm -n ${NAMESPACE} upgrade --install ingress-nginx ingress-nginx/ \
        -f ingress-nginx/values.yaml \
        -f ingress-nginx/values-${NAMESPACE}.yaml

    # Deploy loki
    log_info "Deploying loki..."
    helm -n ${NAMESPACE} upgrade --install loki loki/ \
        -f loki/values.yaml \
        -f loki/values-${NAMESPACE}.yaml

    # Deploy matching
    log_info "Deploying matching..."
    helm -n ${NAMESPACE} upgrade --install matching matching/ \
        -f matching/values.yaml \
        -f matching/values-${NAMESPACE}.yaml

    # Deploy chatbox
    log_info "Deploying chatbox..."
    helm -n ${NAMESPACE} upgrade --install chatbox chatbox/ \
        -f chatbox/values.yaml \
        -f chatbox/values-${NAMESPACE}.yaml

    log_info "Deployment process completed successfully!"
}

# Entry
main "$@"
