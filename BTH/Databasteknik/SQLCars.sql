drop database RentalBeanServic;
create database RentalBeanServic;

drop table BeanCars;
create table BeanCars ( 
carNumber int, 
brand varchar(50), 
model varchar(50),
colour varchar(50), 
pricePerDay int,
primary key (carNumber));
insert into BeanCars (carNumber, brand, model, colour, pricePerDay) values 
(1, 'Peugeot', '208', 'Blue', 800),
(2, 'Peugeot', '3008', 'Green', 700),
(3, 'Volkswagen', 'Polo', 'Red', 600),
(4, 'Volvo', 'V70', 'Silver', 1200),
(5, 'Tesla', 'X', 'Black', 2000),
(6, 'SAAB', '9-5', 'Green', 850),
(7, 'Volvo', 'V40', 'Red', 900),
(8, 'Fiat', '500', 'Black', 1050),
(9, 'Volvo', 'V40', 'Green', 850),
(10, 'Fiat', '500', 'Red', 950),
(11, 'Volkswagen', 'Polo', 'Blue', 700),
(12, 'BMW', 'M3', 'Black', 1599),
(13, 'Volkswagen', 'Golf', 'Red', 1500 );
select * from BeanCars;

drop table CustomerBean;
create table CustomerBean (
customerNumber int,
fullname varchar(50),
birthDate varchar(50),
primary key (customerNumber));
insert into CustomerBean (customerNumber, fullname, birthDate) values 
(1, 'Alice Andersson', '1990-05-05'),
(2, 'Oscar Johansson', '1975-08-10'),
(3, 'Nora Hansen', '1981-10-27'),
(4, 'William Johansen', '2000-01-17'),
(5, 'LucÃ-a GarcÃ-a', '1987-12-13'),
(6, 'Hugo FernÃ¡ndez', '1950-03-16'),
(7, 'Sofia Rossi', '1995-08-04'),
(8, 'Francesco Russo', '2000-02-26'),
(9, 'Olivia Smith', '1972-05-23'),
(10, 'Oliver Jones', '1964-05-08'),
(11, 'Shaimaa Elhawary', '1999-12-23'),
(12, 'Mohamed Elshabrawy', '1997-11-07'),
(13, 'Jing Wong', '1947-07-15'),
(14, 'Wei Lee', '1962-09-29'),
(15, 'Aadya Singh', '1973-01-01'),
(16, 'Aarav Kumar', '1986-06-28'),
(17, 'Louise Martin', '1994-04-22'),
(18, 'Gabriel Bernard', '1969-12-01'),
(19, 'Emma Smith', '1971-03-18'),
(20, 'Noah Johnson', '1800-12-16'),
(21, 'Alice Silva', '1988-12-04'),
(22, 'Miguel Santos', '1939-12-29');
select * from CustomerBean;

drop table BeanBookings;
create table BeanBookings(
bookingNumber int, 
customerNumber int, 
carNumber int,
startDate varchar(50),
endDate varchar(50),
primary Key (bookingNumber),
FOREIGN KEY (customerNumber) REFERENCES CustomerBean(customerNumber));
Alter table BeanBookings
add FOREIGN KEY (carNumber) REFERENCES BeanCars(carNumber);
insert into BeanBookings (bookingNumber, customerNumber, carNumber, startDate, endDate) values
(1, 1, 6, '2018-01-02', '2018-01-15'),
(2, 2, 1, '2018-01-03', '2018-01-05'),
(3, 4, 3, '2018-01-03', '2018-01-04'),
(4, 5, 8, '2018-01-04', '2018-01-30'),
(5, 6, 10, '2018-01-10', '2018-01-13'),
(6, 1, 1, '2018-01-20', '2018-01-25'),
(7, 2, 13, '2018-01-21', '2018-01-30'),
(8, 3, 6, '2018-01-22', '2018-01-30'),
(9, 1, 2, '2018-01-29', '2018-02-01'),
(10, 2, 5, '2018-02-02', '2018-02-06'),
(11, 6, 1, '2018-02-20', '2018-02-25'),
(12, 7, 6, '2018-02-21', '2018-02-24'),
(13, 8, 3, '2018-02-21', '2018-02-28'),
(14, 10, 3, '2018-02-22', '2018-02-26'),
(15, 9, 12, '2018-02-22', '2018-02-28'),
(16, 10, 13, '2018-03-01', '2018-03-10'),
(17, 11, 1, '2018-03-04', '2018-03-09'),
(18, 10, 3, '2018-03-11', '2018-03-14'),
(19, 8, 6, '2018-03-14', '2018-03-17'),
(20, 9, 5, '2018-03-14', '2018-03-30'),
(21, 7, 12, '2018-03-18', '2018-03-20'),
(22, 6, 8, '2018-03-18', '2018-04-02');
select * from BeanBookings;

-- stuff i got stuck on
-- Show all bookings that are longer than 6 days.
select * from BeanBookings where datediff(endDate, startDate) > 6;
-- Show all customers whose first name starts with an O. 
select fullname from CustomerBean where fullname like 'O%';



-- Show all customers with all their information.
select * from CustomerBean;
-- Show all customers, but only with their name and birthdate. 
select fullname, birthDate from  CustomerBean;
-- Show all cars that cost more than 1000:- per day.
select * from BeanCars where priceperday > 1000;
-- Show all Volvo cars, only with their brand name and their model.
select * from BeanCars where brand = 'Volovo';
-- Show all customers, only with their names, in a sorted fashion based on their name. Both in ascending and descending order.
select fullname from CustomerBean order by fullname Asc;
select fullname from CustomerBean order by fullname desc;
-- Show all customers, only with their names, that were born in 1990 or later in a sorted fashion based on their birthdate.
select fullname from CustomerBean where birthDate >= 1990-01-01;
-- Show all cars that are red and cost less than 1500.
select * from BeanCars where colour = 'Red' and preicePerDay < 1500;
-- Show all customers, only with their names, that were born between 1970-1990.
select fullname, birthDate from CustomerBean where birthDate <= 1990-01-01 and birthDate >=1970-01-01;
-- Show all bookings that overlap with the interval 2018-02-01 - 2018-02-25.
select * from BeanBookings where startDate or endDate between 2018-02-01 and 2018-02-25;

-- Show the average price per day for the cars.
select avg(pricePerDay) from BeanCars;
-- Show the total price per day for the cars.
select sum(pricePerDay) from BeanCars;
-- Show the average price for red cars.
select avg(pricePerDay) from BeanCars where colour = 'Red';
-- Show the total price for all cars grouped by the different colors.
select sum(pricePerDay) from BeanCars group by colour; 
-- Show how many cars are of red color.
select count(colour) from BeanCars where colour = 'Red';
-- Show how many cars exists of each color.
select count(colour) from BeanCars group by colour;
-- Show the car that is the most expensive to rent. (Do not hard code this with the most expensive price, instead use ORDER and LIMIT.)
select * from BeanCars order by pricePerDay limit 1;

-- Show the Cartesian product between Cars and Bookings.
SELECT * FROM BeanCars
LEFT JOIN BeanBookings ON BeanCars.carNumber = BeanBookings.carNumber
UNION
SELECT * FROM BeanCars
RIGHT JOIN BeanBookings ON BeanCars.carNumber = BeanBookings.carNumber;
-- Show the Cartesian product between Customers and Bookings.
SELECT * FROM CustomerBean
LEFT JOIN BeanBookings ON CustomerBean.customerNumber = BeanBookings.customerNumber
UNION
SELECT * FROM CustomerBean
RIGHT JOIN BeanBookings ON CustomerBean.customerNumber = BeanBookings.customerNumber;
-- Show the results of converting the previous two joins to inner joins.
SELECT * FROM BeanCars INNER JOIN BeanBookings
ON BeanCars.carNumber = BeanBookings.carNumber;
-- Show the names of all the customers that has made a booking.
select CustomerBean.fullname from CustomerBean inner join BeanBookings on CustomerBean.customerNumber = BeanBookings.customerNumber;
-- Same as the previous but without all the duplicates.
select CustomerBean.fullname from CustomerBean inner join BeanBookings on CustomerBean.customerNumber = BeanBookings.customerNumber where ;
-- Show all the Volkswagen cars that has been booked at least once.
-- Show all the customers that has rented a Volkswagen.
-- Show all cars that has been booked at least once.
-- Show all cars that has never been booked.
-- Show all the black cars that has been booked at least once.

-- Show all the cars that cost more than the average.
-- Show the car with the lowest cost with black color.
-- Show the car which has the lowest cost.
-- Show all the black cars that has been booked at least once by using a sub query.

-- Show all cars that has the cost 700, 800, and 850.
-- Show all the customers that born in 1990, 1995, and 2000. (Hint: YEAR function).
-- Show all the bookings that start on 2018-01-03, 2018-02-22, or 2018-03-18.

-- Show all cars whose price is in the range 600 - 1000.
-- Show all the customers who are born between 1960 - 1980.
-- Show all bookings that last between 2 - 4 days.

-- Show all the cars that are eligible for booking between 2018-01-10 - 2018-01-20.
-- Show the car that has been booked the most.
-- Show all the customers who are born in January or February and has booked at least one car.

-- There is a customer born in 1800 according to the records, this is obviously not possible so delete that customer.
-- The Tesla X car that is available for renting needs to have its price increased by 200:-.
-- All the Peugeot cars also needs to be increased in price, in this case by 20%.
-- Now we fast forward into the future and Sweden has changed its currency to Euros (€). Fix both the data itself (assume the conversion rate is 10SEK == 1 EUR) and the table so it can handle the new prices.
-- Can we construct a PK in the Bookings table without adding a new column? If yes, do that. If not, add another column that allows you to uniquely identify each booking.

-- Create a view, that shows all the information about black cars.
-- Create a view that shows all information about black cars and the addition of the weekly price as a column.
-- Try and insert a car into both views created. What happens? Why? What's the difference between the views?
-- Create a view that shows all the cars available for booking at this current time.
-- Alter the previous view, with the condition that the cars have to be available for at least 3 days of renting.

-- Drop the table Cars.
-- Why didn't it work? Fix so that you can drop the table.
-- Delete all the rows of table Customers.
-- What's the difference between DROP TABLE and DELETE?