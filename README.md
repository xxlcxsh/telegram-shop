DATABASE STRUCTURE:
table users
    id SERIAL PRIMARY KEY,
    t_id BIGINT UNIQUE NOT NULL,
    balance INT DEFAULT 0,
    spent INT DEFAULT 0,
    created TIMESTAMP DEFAULT NOW(),
    is_admin BOOLEAN DEFAULT FALSE
table goods:
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    amount INT,
    price INT NOT NULL,
    category VARCHAR(50) NOT NULL
table orders:
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    good_id INT REFERENCES goods(id),
    created TIMESTAMP DEFAULT NOW()
table categories:
    id SERIAL PRIMARY KEY,
table accounts:
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES good(id) ON DELETE CASCADE,
    data TEXT NOT NULL
    
