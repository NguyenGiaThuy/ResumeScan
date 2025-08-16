# README

## Installation

Install operator & validate

```sh
kubectl apply --server-side -f ./postgres-operator/
kubectl -n cnpg-system get deployment cnpg-controller-manager
```

Create Postgres Cluster

```sh
kubectl -n ai-elevate-dev apply -f ./postgres-cluster/
```

## Post-Installation

Get Postgres Cluster credentials (username, password and connection string):

```sh
./scripts/get-postgres-creds.sh
```

Login to postgres via username and password:

```sh
psql -h localhost -U app -d app
```
