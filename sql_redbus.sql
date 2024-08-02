DROP DATABASE redbus_1;
CREATE DATABASE redbus_1;
USE redbus_1;

CREATE TABLE bus_routes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_name TEXT,
    route_link TEXT,
    busname TEXT,
    bustype TEXT,
    departing_time TIME,
    duration TEXT,
    reaching_time TIME,
    star_rating FLOAT,
    price DECIMAL(10, 2),
    seats_available INT
);

SELECT * FROM bus_routes;



