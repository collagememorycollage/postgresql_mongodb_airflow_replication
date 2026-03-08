// Подключаемся к базе replica_db
db = db.getSiblingDB('replica_db');


// Подключаемся к базе replica_db
db = db.getSiblingDB('replica_db');

// 1. UserSessions
db.UserSessions.insertOne({
  "session_id": "sess_001",
  "user_id": "user_123",
  "start_time": "2024-01-10T09:00:00Z",
  "end_time": "2024-01-10T09:30:00Z",
  "pages_visited": ["/home", "/products", "/products/42", "/cart"],
  "device": {"type": "mobile"},
  "actions": ["login", "view_product", "add_to_cart", "logout"]
});

// 2. EventLogs
db.EventLogs.insertOne({
  "event_id": "evt_1001",
  "timestamp": "2024-01-10T09:05:20Z",
  "event_type": "click",
  "details": { "page": "/products/42" }
});

// 3. SupportTickets
db.SupportTickets.insertOne({
  "ticket_id": "ticket_789",
  "user_id": "user_123",
  "status": "open",
  "issue_type": "payment",
  "messages": [
    { "sender": "user", "message": "Не могу оплатить заказ.", "timestamp": "2024-01-09T12:00:00Z" },
    { "sender": "support", "message": "Пожалуйста, уточните способ оплаты.", "timestamp": "2024-01-09T13:00:00Z" }
  ],
  "created_at": "2024-01-09T11:55:00Z",
  "updated_at": "2024-01-09T13:00:00Z"
});

// 4. UserRecommendations
db.UserRecommendations.insertOne({
  "user_id": "user_123",
  "recommended_products": ["prod_101", "prod_205", "prod_333"],
  "last_updated": "2024-01-10T08:00:00Z"
});

// 5. ModerationQueue
db.ModerationQueue.insertOne({
  "review_id": "rev_555",
  "user_id": "user_123",
  "product_id": "prod_101",
  "review_text": "Отличный товар, работает как нужно!",
  "rating": 5,
  "moderation_status": "pending",
  "flags": ["contains_images"],
  "submitted_at": "2024-01-08T10:20:00Z"
});

print("✅ All collections have been created in replica_db!");
