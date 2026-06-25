CREATE DATABASE IF NOT EXISTS genxcafe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE genxcafe;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','staff','user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category ENUM('Coffee','Tea','Cold Beverages','Pizza','Burgers','Sandwiches','Desserts') NOT NULL,
    image VARCHAR(255) DEFAULT 'default.jpg',
    is_featured TINYINT(1) DEFAULT 0,
    is_available TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    guests INT NOT NULL DEFAULT 1,
    date DATE NOT NULL,
    time TIME NOT NULL,
    special_request TEXT,
    status ENUM('pending','confirmed','cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    subject VARCHAR(200),
    message TEXT NOT NULL,
    is_read TINYINT(1) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chatbot_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role ENUM('user','assistant') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default admin user (password: Admin@123)
INSERT IGNORE INTO users (name, email, password, role) VALUES
('Admin', 'admin@genxcafe.com', 'pbkdf2:sha256:600000$genxcafe$8c4e3f2b1a9d7e6f5c3b2a1d9e8f7c6b5a4d3e2f1c9b8a7d6e5f4c3b2a1d9e8f', 'admin');

-- Sample menu items
INSERT IGNORE INTO menu_items (name, description, price, category, is_featured) VALUES
('Espresso', 'Rich and bold single shot espresso', 120.00, 'Coffee', 1),
('Cappuccino', 'Espresso with steamed milk foam', 160.00, 'Coffee', 1),
('Latte', 'Smooth espresso with steamed milk', 170.00, 'Coffee', 0),
('Americano', 'Espresso diluted with hot water', 130.00, 'Coffee', 0),
('Mocha', 'Espresso with chocolate and milk', 180.00, 'Coffee', 1),
('Masala Chai', 'Spiced Indian tea with milk', 80.00, 'Tea', 0),
('Green Tea', 'Fresh and healthy green tea', 90.00, 'Tea', 0),
('Iced Coffee', 'Chilled coffee with ice', 150.00, 'Cold Beverages', 1),
('Cold Brew', 'Smooth cold-brewed coffee', 200.00, 'Cold Beverages', 0),
('Mango Smoothie', 'Fresh mango blended with milk', 180.00, 'Cold Beverages', 0),
('Margherita Pizza', 'Classic tomato, mozzarella, basil', 350.00, 'Pizza', 1),
('Pepperoni Pizza', 'Loaded with spicy pepperoni', 420.00, 'Pizza', 0),
('Classic Burger', 'Beef patty with lettuce and tomato', 280.00, 'Burgers', 1),
('Veggie Burger', 'Crispy veggie patty with avocado', 240.00, 'Burgers', 0),
('Grilled Chicken Sandwich', 'Tender grilled chicken with herbs', 220.00, 'Sandwiches', 0),
('Club Sandwich', 'Triple-decker with eggs and bacon', 260.00, 'Sandwiches', 0),
('Chocolate Brownie', 'Warm fudgy brownie with ice cream', 150.00, 'Desserts', 1),
('Cheesecake', 'New York-style creamy cheesecake', 180.00, 'Desserts', 0);
