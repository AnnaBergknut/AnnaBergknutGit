create database Shooping;

drop table Produckts;
create table Produckts(
producktID int,
brand varchar(50),
mainType varchar(50),
subType varchar(50),
colour varchar(50),
gender varchar(50),
price int,
size varchar(50),
primary key (producktID));

drop table Customers;
create table Customers(
customerID int,
firstname varchar(50),
lastname varchar(50),
street varchar(50),
city varchar(50),
zipcode int,
primary key (customerID));
insert into Customers (CustomerID, firstname, lastname, street, city, zipcode) values
('1', 'Alice', 'Andersson', 'Testgatan 1', 'Ankeborg', '12312'),
('2', 'Oscar', 'Johansson', 'Testgatan 2', 'Ankeborg', '12312'),
('3', 'Nora', 'Hansen', 'Tramsgatan 1', 'Karlskrona', '32132'),
('4','William', 'Johansen', 'Tramsgatan 2', 'Karlskrona', '32132'),
('5', 'Lucia', 'Garcia', 'Bakgatan 1', 'Skogen', '23423'),
('6', 'Hugo', 'Fernandez', 'Bakgatan 2', 'Skogen', '23423'),
('7','Sofia', 'Rossi', 'Slumpgatan 1', 'Stockholm', '43243'),
('8', 'Francesco', 'Russo', 'Slumpgatan 2',  'Stockholm', '43243'),
('9', 'Olivia', 'Smith', 'Skogsgatan 1', 'Lund', '56776'),
('10', 'Oliver', 'Jones', 'Skogsgatan 2', 'Lund', '56776');
select * from customers;

drop table Orders;
create table Orders (
orderID int,
customerID int,
producktID int,
amount int,
primary key (orderID, producktID),
FOREIGN KEY (customerID) REFERENCES Customers(customerID));
alter table Orders
add FOREIGN KEY (producktID) REFERENCES Producks(producktID);