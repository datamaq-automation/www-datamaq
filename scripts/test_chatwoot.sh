#!/bin/bash
# Script de diagnóstico para probar la integración con Chatwoot Application API.
# Lee las variables desde .env en la raíz del proyecto.

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ -f "$ENV_FILE" ]; then
    # shellcheck source=/dev/null
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

BASE_URL="${CHATWOOT_BASE_URL:-https://app.chatwoot.com}"
ACCOUNT_ID="${CHATWOOT_ACCOUNT_ID}"
API_TOKEN="${CHATWOOT_API_TOKEN}"

if [ -z "$ACCOUNT_ID" ] || [ -z "$API_TOKEN" ]; then
    echo "❌ CHATWOOT_ACCOUNT_ID o CHATWOOT_API_TOKEN no están configurados en $ENV_FILE"
    exit 1
fi

URL="$BASE_URL/api/v1/accounts/$ACCOUNT_ID/contacts"

echo "🔍 Probando Chatwoot Application API"
echo "   API_TOKEN: $API_TOKEN"
echo "   URL:       $URL"
echo "   Cuenta:    $ACCOUNT_ID"

UNIQUE_SUFFIX=$(date +%s)
TEST_EMAIL="test${UNIQUE_SUFFIX}@datamaq.com"
TEST_PHONE="+549${UNIQUE_SUFFIX}"

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$URL" \
    -H "api_access_token: $API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"name\":\"Test User\",\"phone_number\":\"$TEST_PHONE\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo ""
echo "Status: $HTTP_CODE"
echo "Body:   $BODY"
echo ""

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 300 ]; then
    echo "✅ Chatwoot respondió correctamente"
else
    echo "❌ Chatwoot respondió con error $HTTP_CODE"
    exit 1
fi
