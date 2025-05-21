CREATE TABLE IF NOT EXISTS bookings (
    id TEXT PRIMARY KEY,             -- Unique booking ID, e.g. 'cloudbeds_1234'
    source TEXT NOT NULL,            -- Booking source: 'Cloudbeds' or 'Lodgify'
    guest_name TEXT NOT NULL,        -- Full guest name
    check_in DATE NOT NULL,          -- Check-in date
    check_out DATE NOT NULL,         -- Check-out date
    total_price REAL NOT NULL,       -- Total price of the booking
    created_at TEXT NOT NULL         -- Timestamp when booking was created
);
CREATE TABLE bookings (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    guest_name TEXT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price REAL NOT NULL,
    created_at TIMESTAMP NOT NULL,
    country TEXT NOT NULL
);

INSERT INTO bookings (
    id, source, guest_name, check_in, check_out, total_price, created_at
) VALUES
    ('cloudbeds_1001', 'Cloudbeds', 'Alice Smith', '2025-06-01', '2025-06-05', 420.50, '2025-05-21T08:00:00Z'),
    ('lodgify_2002', 'Lodgify', 'Bob Johnson', '2025-06-10', '2025-06-12', 310.00, '2025-05-21T09:30:00Z');
SELECT * FROM bookings;
SELECT * FROM bookings
WHERE DATE(created_at) = DATE('now');  -- works in SQLite
