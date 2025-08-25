CREATE TABLE history (
    id SERIAL PRIMARY KEY,
    session_id TEXT NOT NULL,
    film TEXT NOT NULL,
    recommendation TEXT NOT NULL
)