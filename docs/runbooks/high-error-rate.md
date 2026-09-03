# Runbook: High Error Rate

## Alert
- **Name:** HighErrorRate
- **Severity:** Critical
- **Condition:** Error rate > 5% for 5 minutes

## Immediate Actions

1. **Check the dashboard**
   ```bash
   kubectl port-forward svc/grafana -n monitoring 3000:80
   # Open http://localhost:3000 → Application Dashboard
   ```

2. **Check pod status**
   ```bash
   kubectl get pods -n production -l app=cloud-native-app
   kubectl logs -n production -l app=cloud-native-app --tail=100
   ```

3. **Check recent deployments**
   ```bash
   kubectl rollout history deployment/cloud-native-app -n production
   ```

## If Caused by Recent Deployment
```bash
./scripts/rollback.sh production
```

## If Database Issues
```bash
# Check DB connections
kubectl exec -n production deploy/cloud-native-app -- python -c "
import psycopg2
conn = psycopg2.connect(host='DB_HOST', dbname='appdb', user='app_admin')
print('DB OK')
"
```

## If Redis Issues
```bash
kubectl exec -n production deploy/cloud-native-app -- python -c "
import redis
r = redis.Redis(host='REDIS_HOST', port=6379)
print(r.ping())
"
```

## Escalation
- If not resolved in 15 minutes → Page on-call engineer
- If affecting customers > 30 minutes → Incident commander
