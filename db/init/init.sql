-- enum for users
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_role') THEN
    CREATE TYPE user_role AS ENUM ('customer', 'manager', 'admin');
  END IF;
END
$$;

CREATE TABLE IF NOT EXISTS users (
  user_id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email          VARCHAR(255)  NOT NULL UNIQUE,
  password_hash  TEXT NOT NULL,
  name           VARCHAR(50)  NOT NULL,
  role           user_role NOT NULL DEFAULT 'customer',
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE IF NOT EXISTS coffee_shops (
  shop_id      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name         VARCHAR(128)  NOT NULL, 
  address      VARCHAR(256) NOT NULL,
  manager_id   INTEGER UNIQUE REFERENCES users(user_id) ON DELETE SET NULL 
);


CREATE TABLE IF NOT EXISTS products (
  product_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name        VARCHAR(128) NOT NULL, 
  description TEXT,
  image_url   TEXT,
  price       INTEGER NOT NULL CHECK (price >= 0) 
);


CREATE TABLE IF NOT EXISTS shop_menu (
  shop_menu_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  shop_id      INTEGER NOT NULL REFERENCES coffee_shops(shop_id) ON DELETE CASCADE,
  product_id   INTEGER NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
  is_available BOOLEAN NOT NULL DEFAULT TRUE,
  UNIQUE (shop_id, product_id)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id      INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
  shop_id      INTEGER NOT NULL REFERENCES coffee_shops(shop_id) ON DELETE RESTRICT,
  total_amount INTEGER NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_id      INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
  product_id    INTEGER NOT NULL REFERENCES products(product_id) ON DELETE RESTRICT,
  unit_price    INTEGER NOT NULL CHECK (unit_price >= 0),
  quantity      INTEGER NOT NULL CHECK (quantity >= 1)
);

CREATE INDEX IF NOT EXISTS idx_orders_user_created ON orders(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_shop_menu_shop_available ON shop_menu(shop_id, is_available);