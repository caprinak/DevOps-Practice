#!/bin/bash
# Microservices E2E Test Script (Bash)
# This script automates the Customer -> Product -> Order flow via the API Gateway.

GATEWAY_URL="http://localhost:8222/api/v1"

echo "--- Step 1: Creating Customer ---"
CUSTOMER_ID=$(curl -s -X POST "$GATEWAY_URL/customers" \
  -H "Content-Type: application/json" \
  -d '{
    "firstname": "Bash",
    "lastname": "Tester",
    "email": "bash.test@example.com",
    "address": {
      "street": "Shell Blvd",
      "houseNumber": "202",
      "zipCode": "88888"
    }
  }')

echo "Success! Customer ID: $CUSTOMER_ID"

echo -e "\n--- Step 2: Creating Product ---"
PRODUCT_ID=$(curl -s -X POST "$GATEWAY_URL/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Shell Gadget",
    "description": "A product created by bash script",
    "availableQuantity": 50,
    "price": 49.99,
    "categoryId": 1
  }')

echo "Success! Product ID: $PRODUCT_ID"

echo -e "\n--- Step 3: Placing Order ---"
ORDER_ID=$(curl -s -X POST "$GATEWAY_URL/orders" \
  -H "Content-Type: application/json" \
  -d "{
    \"reference\": \"BASH_ORD_$(date +%H%M)\",
    \"amount\": 49.99,
    \"paymentMethod\": \"PAYPAL\",
    \"customerId\": \"$CUSTOMER_ID\",
    \"products\": [
      {
        \"productId\": $PRODUCT_ID,
        \"quantity\": 1
      }
    ]
  }")

echo "Success! Order ID: $ORDER_ID"

echo -e "\n=========================================="
echo "E2E Integration Test Completed Successfully!"
echo "Check Zipkin: http://localhost:9411"
echo "Check MailDev: http://localhost:1080"
echo "=========================================="
