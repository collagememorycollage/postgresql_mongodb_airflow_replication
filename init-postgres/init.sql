CREATE TABLE IF NOT EXISTS UserSessions (
	session_id TEXT PRIMATY KEY,
	user_id TEXT NOT NULL,
	start_time TIMESTAMPTZ NOT NULL,
	end_time TIMESTAMPTZ NOT NULL
	pages_visited JSONB NOT NULL,
	actions TEXT[] NOT NULL,
	device JSONB NOT NULL
);


CREATE TABLE IF NOT EXISTS EventLogs (
	event_id TEXT PRIMATY KEY,
	timestamp TIMESTAMPTZ NOT NULL,
	event_type TEXT NOT NULL,
	details JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS SupportTickets (
	
);

CREATE TABLE IF NOT EXISTS UserRecommendations (
	user_id TEXT PRIMARY KEY,
	last_updated TIMESTAMPTZ,
	recommended_products TEXT[] NOT NULL
);

CREATE TABLE IF NOT EXISTS ModerationQueue (
	review_id TEXT PRIMARY KEY,
	user_id TEXT NOT NULL,
	product_id TEXT NOT NULL,
	review_text TEXT NOT NULL,
	rating INT NOT NULL,
	moderation_status NOT NULL,
	submitted_at NOT NULL,
	flags NOT NULL
);


1. UserSessions (Сессии)
Таблица: user_sessions
Колонки:
session_id (TEXT, PK), user_id (TEXT), start_time, end_time (TIMESTAMP).
pages_visited (TEXT[] или JSONB) — так как это простой список строк.
actions (TEXT[]) — список действий.
device (JSONB) — так как в Mongo это объект (даже если там одно поле).
2. EventLogs (Логи)
Таблица: event_logs
Колонки:
event_id (TEXT, PK), timestamp (TIMESTAMP), event_type (TEXT).
details (JSONB) — идеальное поле для неструктурированных деталей события.
3. SupportTickets (Тикеты) — Самая сложная структура
Вариант А (Простой): Таблица support_tickets, где поле messages — это JSONB. Это сохранит иерархию переписки в одной строке.
Вариант Б (Аналитический): Две таблицы.
tickets (основная инфо).
ticket_messages (отдельные строки для каждого сообщения с ticket_id), если нужно считать среднее время ответа оператора.
4. UserRecommendations (Рекомендации)
Таблица: user_recommendations
Колонки:
user_id (TEXT, PK), last_updated (TIMESTAMP).
recommended_products (TEXT[]) — массив ID товаров.
5. ModerationQueue (Модерация)
Таблица: moderation_queue
Колонки:
review_id (PK), user_id, product_id, review_text (TEXT), rating (INT), moderation_status, submitted_at.
flags (TEXT[]) — массив тегов типа ["contains_images"].
