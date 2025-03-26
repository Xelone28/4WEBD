-- -----------------------------------------------------
-- Table: users
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Indexes for users
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- -----------------------------------------------------
-- Table: events
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    location VARCHAR(255),
    date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    total_tickets INTEGER NOT NULL,
    available_tickets INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);

-- Indexes for events
CREATE INDEX IF NOT EXISTS idx_events_name ON events (name);
CREATE INDEX IF NOT EXISTS idx_events_date ON events (date);

-- -----------------------------------------------------
-- Table: tickets
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    purchase_date TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Indexes for tickets
CREATE INDEX IF NOT EXISTS idx_tickets_ticket_number ON tickets (ticket_number);
CREATE INDEX IF NOT EXISTS idx_tickets_event_id ON tickets (event_id);
CREATE INDEX IF NOT EXISTS idx_tickets_user_id ON tickets (user_id);

-- -----------------------------------------------------
-- Optional: Additional Constraints and Triggers
-- -----------------------------------------------------

-- Automatically update the 'updated_at' column on row update
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for users table
CREATE TRIGGER trigger_update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for events table
CREATE TRIGGER trigger_update_events_updated_at
BEFORE UPDATE ON events
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

-- Trigger for tickets table
CREATE TRIGGER trigger_update_tickets_updated_at
BEFORE UPDATE ON tickets
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();

INSERT INTO public.users
(email, hashed_password, first_name, last_name)
VALUES('lougautr@gmail.com', 'password', 'Lou-Anne', 'Gautherie');

INSERT INTO public.events
(name, description, location, date, total_tickets, available_tickets)
VALUES('Chambre 140 Tour PLK ', 'La tournée Chambre 140 Tour 2025 de PLK passe à Paris à L Accor Arena à Paris ', 'Accor Arena - Paris', '2025-11-15 20:00:00', 1000, 200);

INSERT INTO public.tickets
(ticket_number, event_id, user_id, purchase_date)
VALUES('1203', 1, 1, '2025-03-20 10:14:56');
