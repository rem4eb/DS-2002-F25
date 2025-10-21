#!/bin/bash

read -p "Enter TCG Card Set ID (e.g., base1, base4): " SET_ID

if [ -z "$SET_ID" ]; then
    echo "Error: Set ID cannot be empty." >&2
    exit 1
fi

echo "Fetching card data for set: $SET_ID"

curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" -o "card_set_lookup/${SET_ID}.json"

# Check if curl was successful
if [ $? -eq 0 ]; then
    echo "Successfully saved card data to card_set_lookup/${SET_ID}.json"
else
    echo "Error: Failed to fetch data from API." >&2
    exit 1
fi