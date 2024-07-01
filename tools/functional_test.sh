#!/bin/bash

set -ex

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Install the CaaS operator from the chart we are about to ship
# Make sure to use the images that we just built
helm upgrade coral-credits ./charts \
  --dependency-update \
  --namespace coral-credits \
  --create-namespace \
  --install \
  --wait \
  --timeout 10m \
  --set-string image.tag=${GITHUB_SHA::7}

# Wait for rollout
kubectl rollout status deployment/coral-credits -n coral-credits --timeout=300s -w
# temporary, for some reason rollout doesn't wait long enough.
sleep 20
# Port forward in the background
kubectl port-forward -n coral-credits svc/coral-credits 8080:8080 &

# Check we get a 204 from the status endpoint
if [ "$(curl -s http://0.0.0.0:8080/_status/ -w "%{http_code}")" -eq 204 ]; then
    echo "Success: HTTP status code is 204."
else
    echo "Error: Expected HTTP status code 204, but got $(curl -s -o /dev/null -w "%{http_code}" http://0.0.0.0:8080/_status/)"
    exit 1
fi

#TODO(tylerchristie) check more things