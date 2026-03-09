CREATE TABLE UserSessions (
	session_id TEXT PRIMARY KEY,
	user_id TEXT NOT NULL,
	start_time TIMESTAMPTZ NOT NULL,
	end_time TIMESTAMPTZ NOT NULL,
	pages_visited JSONB NOT NULL,
	device JSONB NOT NULL,
	actions TEXT[] NOT NULL
);


CREATE TABLE EventLogs (
	event_id TEXT PRIMARY KEY,
	timestamp TIMESTAMPTZ NOT NULL,
	event_type TEXT NOT NULL,
	details JSONB
);

CREATE TABLE SupportTickets (
	ticket_id TEXT PRIMARY KEY,
	user_id TEXT NOT NULL,
	status TEXT NOT NULL,
	issue_type TEXT,
	message JSONB,
	cerated_at TIMESTAMPTZ NOT NULL,
	updated_ad TIMESTAMPTZ
);

CREATE TABLE UserRecommendations (
	user_id TEXT PRIMARY KEY,
	last_updated TIMESTAMPTZ,
	recommended_products TEXT[] NOT NULL
);

CREATE TABLE ModerationQueue (
	review_id TEXT PRIMARY KEY,
	user_id TEXT NOT NULL,
	product_id TEXT NOT NULL,
	review_text TEXT NOT NULL,
	rating INT CHECK (rating BETWEEN 1 AND 5),
	moderation_status TEXT,
	flags TEXT[],
	submitted_at TIMESTAMPTZ
);


