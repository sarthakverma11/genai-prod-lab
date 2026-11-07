
#!/usr/bin/env bash
set -euo pipefail

docker network create genai-net

# Deploy both versions
docker run -d --name app-a \
  --network genai-net -p 8001:8000 \
  genai-app:tag-a

docker run -d --name app-b \
  --network genai-net -p 8002:8000 \
  genai-app:tag-b

# Check both containers
for port in 8001 8002; do
  for i in {1..20}; do
    if curl -fsS "http://localhost:$port/health"; then
      break
    fi
    sleep 1
  done
  curl -fsS "http://localhost:$port/health"
done

# Start a temporary traffic gateway
docker run -d --name gateway \
  --network genai-net -p 8080:80 nginx:alpine

route_to() {
  target="$1"

  cat > nginx.conf <<EOF
events {}
http {
  server {
    listen 80;
    location / {
      proxy_pass http://${target}:8000;
    }
  }
}
EOF

  docker cp nginx.conf gateway:/etc/nginx/nginx.conf
  docker exec gateway nginx -t
  docker exec gateway nginx -s reload
}

# Initially route to Version A
route_to app-a
curl -fsS http://localhost:8080/health \
  | grep -q '"version":"A"'
echo "Version A active"

# Switch traffic to Version B
route_to app-b
curl -fsS http://localhost:8080/health \
  | grep -q '"version":"B"'
echo "Version B active"

# Rollback to Version A
start=$(date +%s)

route_to app-a
curl -fsS http://localhost:8080/health \
  | grep -q '"version":"A"'

elapsed=$(( $(date +%s) - start ))
echo "Rollback successful in ${elapsed} seconds"

test "$elapsed" -lt 120
