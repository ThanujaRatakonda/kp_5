#!/bin/bash

echo "Stopping old port-forward processes..."

# Kill old port-forward processes
for port in 5000 4000 5433; do
    pid=$(lsof -t -i:$port || true)
    if [ ! -z "$pid" ]; then
        kill -9 $pid
        echo "Killed process on port $port"
    fi
done

echo "Starting port-forwarding in fully detached background..."

# Ensure correct kubeconfig
export KUBECONFIG=/var/lib/jenkins/.kube/config

# Start port-forwarding fully detached
setsid nohup /usr/local/bin/kubectl port-forward svc/backend 5000:5000 --address 0.0.0.0 > /tmp/backend.log 2>&1 &
setsid nohup /usr/local/bin/kubectl port-forward svc/frontend 4000:3000 --address 0.0.0.0 > /tmp/frontend.log 2>&1 &
setsid nohup /usr/local/bin/kubectl port-forward statefulset/database 5433:5432 --address 0.0.0.0 > /tmp/database.log 2>&1 &

echo "Port forwarding started in detached mode. Logs: /tmp/backend.log /tmp/frontend.log /tmp/database.log"

