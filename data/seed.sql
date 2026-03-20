DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS employees;

-- DEPARTMENTS
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget REAL
);
INSERT INTO departments VALUES
    (1, 'Engineering', 500000),
    (2, 'Marketing', 200000),
    (3, 'Sales', 300000),
    (4, 'HR', 150000),
    (5, 'Finance', 250000),
    (6, 'Legal', 100000);

-- EMPLOYEES (some have dept_id that doesn't exist, some have NULL)
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dept_id INTEGER,
    salary REAL,
    hire_date TEXT,
    manager_id INTEGER
);
INSERT INTO employees VALUES
    (1,  'Alice',    1, 95000,  '2021-03-15', NULL),
    (2,  'Bob',      1, 87000,  '2022-01-10', 1),
    (3,  'Charlie',  1, 78000,  '2023-06-01', 1),
    (4,  'Diana',    2, 72000,  '2022-04-20', NULL),
    (5,  'Eve',      2, 65000,  '2023-09-01', 4),
    (6,  'Frank',    3, 82000,  '2021-07-01', NULL),
    (7,  'Grace',    3, 82000,  '2022-11-15', 6),
    (8,  'Hank',     3, 68000,  '2023-02-01', 6),
    (9,  'Ivy',      3, 68000,  '2024-01-10', 6),
    (10, 'Jack',     4, 55000,  '2023-05-01', NULL),
    (11, 'Karen',    NULL, 70000, '2023-08-01', NULL),
    (12, 'Leo',      NULL, 62000, '2024-02-15', NULL),
    (13, 'Mona',     99, 58000, '2024-03-01', NULL),
    (14, 'Nick',     1, 92000,  '2021-06-01', 1),
    (15, 'Olivia',   5, 88000,  '2022-03-01', NULL);

-- CUSTOMERS
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    segment TEXT
);
INSERT INTO customers VALUES
    (1,  'Acme Corp',       'Warsaw',    'Enterprise'),
    (2,  'Beta Ltd',        'Krakow',    'SMB'),
    (3,  'Gamma Inc',       'Gdansk',    'Enterprise'),
    (4,  'Delta SA',        'Wroclaw',   'Startup'),
    (5,  'Epsilon Sp',      'Poznan',    'SMB'),
    (6,  'Zeta Group',      'Warsaw',    'Enterprise'),
    (7,  'Eta Solutions',   'Krakow',    'Startup'),
    (8,  'Theta Corp',      'Lodz',      'SMB'),
    (9,  'Iota Tech',       'Warsaw',    'Enterprise'),
    (10, 'Kappa Digital',   'Gdansk',    'Startup');

-- PRODUCTS
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    price REAL
);
INSERT INTO products VALUES
    (1, 'Cloud Basic',      'Cloud',      99.99),
    (2, 'Cloud Pro',        'Cloud',      299.99),
    (3, 'Cloud Enterprise', 'Cloud',      999.99),
    (4, 'Analytics Lite',   'Analytics',  149.99),
    (5, 'Analytics Pro',    'Analytics',  449.99),
    (6, 'Security Suite',   'Security',   599.99),
    (7, 'Dev Tools',        'DevOps',     199.99),
    (8, 'CI/CD Pipeline',   'DevOps',     349.99);

-- ORDERS
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    status TEXT
);
INSERT INTO orders VALUES
    (1,  1,  '2024-01-05', 'completed'),
    (2,  1,  '2024-01-20', 'completed'),
    (3,  2,  '2024-01-15', 'completed'),
    (4,  3,  '2024-02-01', 'completed'),
    (5,  3,  '2024-02-10', 'cancelled'),
    (6,  1,  '2024-02-15', 'completed'),
    (7,  4,  '2024-03-01', 'completed'),
    (8,  5,  '2024-03-10', 'completed'),
    (9,  5,  '2024-03-15', 'pending'),
    (10, 6,  '2024-04-01', 'completed'),
    (11, 1,  '2024-04-10', 'completed'),
    (12, 7,  '2024-04-20', 'completed'),
    (13, 3,  '2024-05-01', 'completed'),
    (14, 8,  '2024-05-15', 'completed'),
    (15, 2,  '2024-06-01', 'pending'),
    (16, 9,  '2024-06-10', 'completed'),
    (17, 1,  '2024-07-01', 'completed'),
    (18, 6,  '2024-07-15', 'cancelled'),
    (19, 3,  '2024-08-01', 'completed'),
    (20, 4,  '2024-08-20', 'completed');

-- ORDER ITEMS
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);
INSERT INTO order_items VALUES
    (1,  1,  1, 5),
    (2,  1,  4, 2),
    (3,  2,  2, 3),
    (4,  3,  1, 10),
    (5,  3,  7, 1),
    (6,  4,  3, 2),
    (7,  5,  5, 1),
    (8,  6,  2, 5),
    (9,  7,  6, 3),
    (10, 8,  1, 8),
    (11, 8,  4, 4),
    (12, 9,  7, 2),
    (13, 10, 3, 1),
    (14, 11, 2, 2),
    (15, 12, 1, 15),
    (16, 13, 5, 3),
    (17, 14, 6, 1),
    (18, 15, 8, 2),
    (19, 16, 3, 4),
    (20, 17, 2, 1),
    (21, 18, 4, 6),
    (22, 19, 1, 20),
    (23, 19, 3, 1),
    (24, 20, 7, 5);
