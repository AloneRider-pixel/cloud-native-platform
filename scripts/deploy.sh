#!/bin/bash
# Deploy application to Kubernetes
set -euo pipefail

ENVIRONMENT=${1:-production}
IMAGE_TAG=${2:-latest}
NAMESPACE=$ENVIRONMENT

echo "🚀 Deploying to $ENVIRONMENT (image: $IMAGE_TAG)"

# Update kubeconfig
aws eks update-kubeconfig --name "cloud-native-app-$ENVIRONMENT" --region ap-south-1

# Apply base manifests
kubectl apply -f kubernetes/base/namespace.yaml
kubectl apply -f kubernetes/base/secret.yaml
kubectl apply -f kubernetes/base/configmap.yaml

# Deploy with Helm
helm upgrade --install cloud-native-app ./helm/app \
  --namespace "$NAMESPACE" \
  --create-namespace \
  --set image.tag="$IMAGE_TAG" \
  --values "helm/app/values-${ENVIRONMENT}.yaml" \
  --wait \
  --timeout 300s

# Verify
echo "✅ Deployment complete. Verifying..."
kubectl rollout status deployment/cloud-native-app -n "$NAMESPACE" --timeout=300s
kubectl get pods -n "$NAMESPACE" -l app=cloud-native-app

echo "🎉 Deployed successfully!"
