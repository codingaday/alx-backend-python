{
  "info": {
    "name": "Messaging App API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Obtain JWT Token",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "url": {
          "raw": "{{base_url}}/api/token/",
          "host": ["{{base_url}}"],
          "path": ["api", "token"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"your_username\",\n  \"password\": \"your_password\"\n}"
        }
      }
    },
    {
      "name": "Refresh JWT Token",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "url": {
          "raw": "{{base_url}}/api/token/refresh/",
          "host": ["{{base_url}}"],
          "path": ["api", "token", "refresh"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"refresh\": \"{{refresh_token}}\"\n}"
        }
      }
    },
    {
      "name": "Create Conversation",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/conversations/",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"participants\": [\"other_username\"]\n}"
        }
      }
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/conversations/{{conversation_id}}/messages/",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations", "{{conversation_id}}", "messages"]
        },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"content\": \"Hello!\"\n}"
        }
      }
    },
    {
      "name": "Fetch Conversations",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/conversations/",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations"]
        }
      }
    },
    {
      "name": "Fetch Messages (Paginated & Filtered)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/conversations/{{conversation_id}}/messages/?page=1&sender=other_username&sent_after=2024-01-01T00:00:00",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations", "{{conversation_id}}", "messages"],
          "query": [
            { "key": "page", "value": "1" },
            { "key": "sender", "value": "other_username" },
            { "key": "sent_after", "value": "2024-01-01T00:00:00" }
          ]
        }
      }
    },
    {
      "name": "Unauthorized Access Test",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/api/conversations/",
          "host": ["{{base_url}}"],
          "path": ["api", "conversations"]
        }
      }
    }
  ]
}
