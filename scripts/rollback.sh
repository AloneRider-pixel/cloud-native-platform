#!/bin/bash
# Rollback deployment to previous version
set -euo pipefail

ENVIRONMENT=${1:-production}
NAMESPACE=$ENVIRONMENT

echo "🔄 Rolling back $ENVIRONMENT deployment..."

aws eks update-kubeconfig --name "cloud-native-app-$ENVIRONMENT" --region ap-south-1

# Check current rollout history
echo "📋 Current rollout history:"
kubectl rollout history deployment/cloud-native-app -n "$NAMESPACE"

# Undo to previous revision
kubectl rollout undo deployment/cloud-native-app -n "$NAMESPACE"

# Wait for rollout
kubectl rollout status deployment/cloud-native-app -n "$NAMESPACE" --timeout=300s

echo "✅ Rollback complete!"
kubectl get pods -n "$NAMESPACE" -l app=cloud-native-app
