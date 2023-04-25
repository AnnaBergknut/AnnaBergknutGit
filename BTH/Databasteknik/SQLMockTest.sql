create Database Mocktest;
create table Student (
stNum varchar(50), 
Fname varchar(50), 
Lname varchar(50), 
Age int, 
Telephone varchar(50), 
Email varchar(50), 
Address varchar(50),
primary key(stNum));

INSERT INTO Student (stNum, Fname, Lname, Age, Telephone, Email, Address) VALUES
('DA2G93D','Lars','Andersson',26,'07-71793336','kivaba3175@ineedsa.com','Stackekärr 121, Dyltabruk'),
('K88ZP8O','Anna','Nilsson',25,'07-79156016','veter22@aosdeag.com','Mogata Sjöhagen 60, Bullaren'),
('W6T5WZG','Anders','Johansson',29,'07-72240308','slabody@iaintel.com','Fuglie 80, Umeå'),
('PTQY0BQ','Maria','Karlsson',27,'07-77038419','anzhelagrechka@distraplo.com','Orrspelsv 130, Lycksele'),
('F62FDT84','Mikael','Mountain',26,'07-74215021','marusiam85@epubd.site','Sandviken 57, Dyltabruk');


create table Book(
ISBN varchar(50),
Title varchar(50), 
Author varchar(50), 
shelfNum varchar(50), 
numOfCopies varchar(50),
primary key(ISBN));

INSERT INTO Book (ISBN, Title, Author, shelfNum, numOfCopies) VALUES
('F-0055-G', 'De kommer att drunkna i sina mödrars tårar', 'Johannes Anyuru','PER-5',4),
('A-0080-Z', 'Folk med ångest', 'Fredrik Backman','PER-5',4),
('H-0037-M','Välkommen till Amerika', 'Linda Boström Knausgård','SEM-1',4),
('A-0030-B','Silvervägen', 'Stina Jackson','PIN-4',5),
('C-0050-K','Drömfakulteten', 'Sara Stridsberg','PAS-3',4),
('H-0082-M','Inlandet', 'Elin Willows','NAM-8',5);


create table BookLease (
leaseNumber varchar(50),
ISBN varchar(50),
stNum varchar(50) ,
startDate varchar(50),
leaseInDays varchar(50),
dateReturned varchar(50),
primary key (leaseNumber),
FOREIGN KEY (stNum) REFERENCES Student(stNum),
FOREIGN KEY (ISBN) REFERENCES Book(ISBN));

INSERT INTO BookLease(leaseNumber,ISBN,stNum,startDate,leaseInDays,dateReturned) VALUES
(1,'F-0055-G','PTQY0BQ','2020-06-10',10,'2020-06-20'),
(2,'C-0050-K','K88ZP8O','2020-06-10',8,'2020-06-18'),
(3,'A-0080-Z','DA2G93D','2020-11-10',25,'2020-12-10'),
(4,'F-0055-G','DA2G93D','2020-11-10',25,'2020-12-10'),
(5,'A-0030-B','K88ZP8O','2019-11-03',24,'2019-11-27'),
(6,'H-0037-M','W6T5WZG','2021-12-10',25,NULL),
(7,'C-0050-K','PTQY0BQ','2021-12-10',30, NULL),
(8,'H-0037-M','DA2G93D','2019-05-05',15,'2019-05-06'),
(9,'A-0080-Z','PTQY0BQ','2021-12-05',5, NULL),
(10,'F-0055-G','W6T5WZG','2021-12-03',10, NULL);

select * from Student; -- test
select (stNum, Fname, Lname, numOfLeases) from Student where Not Student(stNum) in Booklease(stNum); -- idk why it don't select

insert into BookLease 
select (ISND, Title,) from Book where datediff(startDate, dateReturned) and dateReturned is not null from BookLease;


