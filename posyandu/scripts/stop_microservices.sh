#!/bin/bash

echo "🛑 Stopping Posyandu + Microservices..."

# Stop all services
docker-compose down

echo "✅ All services have been stopped!"

# Optional: Remove volumes (uncomment if you want to reset database)
# echo "🗑️  Removing volumes..."
# docker-compose down -v

echo "📊 To view logs:"
echo "  docker-compose logs [service-name]"
echo ""
echo "🚀 To start services again:"
echo "  ./run_microservices.sh"
