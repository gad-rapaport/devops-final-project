-- Create test database for CI pipeline
CREATE DATABASE IF NOT EXISTS smartrecipe_test;
GRANT ALL PRIVILEGES ON smartrecipe_test.* TO 'smartrecipe'@'%';
FLUSH PRIVILEGES;
