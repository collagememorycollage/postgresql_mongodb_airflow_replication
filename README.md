# Работа с MongoDB (mongosh)

### Установка и подключение


**Linux**
```
sudo curl -O https://www.mongodb.com && sudo dpkg -i mongodb-mongosh_2.7.0_amd64.deb
```

**Mac**
```
sudo curl -O https://downloads.mongodb.com/compass/mongosh-2.7.0-darwin-arm64.zip 
```

**Подключение**
```
mongosh "mongodb://admin:secret@localhost:27017/?authSource=admin"
```

**Базовые команды**
```
use replica_db
show collections
```


##### База данных создается из файла /init-mongo/init.js

#### 1. UserSessions, сессии пользователей:
- **session_id** — уникальный идентификатор сессии;
- **user_id** — идентификатор пользователя;
- **start_time** — время начала сессии;
- **end_time** — время завершения сессии;
- **pages_visited** — массив посещённых страниц;
- **device** — информация об устройстве;
- **actions** — массив действий пользователя.
```
{
    "session_id": "sess_001",
    "user_id": "user_123",
    "start_time": "2024-01-10T09:00:00Z",
    "end_time": "2024-01-10T09:30:00Z",
    "pages_visited": ["/home", "/products", "/products/42", "/cart"],
    "device": {"mobile"},
    "actions": ["login", "view_product", "add_to_cart", "logout"]
}
```

#### 2. EventLogs, логи событий:
- **event_id** — уникальный идентификатор события;
- **timestamp** — время события;
- **event_type** — тип события;
- **details** — подробности.

```
{
    "event_id": "evt_1001",
    "timestamp": "2024-01-10T09:05:20Z",
    "event_type": "click",
    "details": {"/products/42"}
}
```

#### 3. SupportTickets, обращения в поддержку:
- **ticket_id** — уникальный идентификатор тикета;
- **user_id** — идентификатор пользователя;
- **status** — статус тикета;
- **issue_type** — тип проблемы;
- **messages** — массив сообщений;
- **created_at** — время создания тикета;
- **updated_at** — время последнего обновления.

```
{
    "ticket_id": "ticket_789",
    "user_id": "user_123",
    "status": "open",
    "issue_type": "payment",
    "messages": [
        {
            "sender": "user",
            "message": "Не могу оплатить заказ.",
            "timestamp": "2024-01-09T12:00:00Z"
        },
        {
            "sender": "support",
            "message": "Пожалуйста, уточните способ оплаты.",
            "timestamp": "2024-01-09T13:00:00Z"
        }
    ],
    "created_at": "2024-01-09T11:55:00Z",
    "updated_at": "2024-01-09T13:00:00Z"
}
```

#### 4. UserRecommendations, рекомендации пользователям:
- **user_id** — идентификатор пользователя;
- **recommended_products** — массив рекомендованных товаров;
- **last_updated** — время последнего обновления рекомендаций.

```
{
    "user_id": "user_123",
    "recommended_products": ["prod_101", "prod_205", "prod_333"],
    "last_updated": "2024-01-10T08:00:00Z"
}
```

#### 5. ModerationQueue, очередь модерации отзывов:
- **review_id** — идентификатор отзыва;
- **user_id** — идентификатор пользователя;
- **product_id** — идентификатор товара;
- **review_text** — текст отзыва;
- **rating** — оценка;
- **moderation_status** — статус модерации;
- **flags** — массив флагов;
- **submitted_at** — время, когда был оставлен отзыв.

```
{
    "review_id": "rev_555",
    "user_id": "user_123",
    "product_id": "prod_101",
    "review_text": "Отличный товар, работает как нужно!",
    "rating": 5,
    "moderation_status": "pending",
    "flags": ["contains_images"],
    "submitted_at": "2024-01-08T10:20:00Z"
}
```


