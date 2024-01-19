CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL
            );

CREATE TABLE IF NOT EXISTS "product" (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(50) NOT NULL,
                price decimal NOT NULL
            );

CREATE TABLE IF NOT EXISTS "sales" (
                id SERIAL PRIMARY KEY,
                product_id integer NOT NULL REFERENCES "product"(id) ,
                user_id integer NOT NULL REFERENCES "user"(id)
            );