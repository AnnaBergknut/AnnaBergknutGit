# 1. create a database
create database shitty_prov;
use shitty_prov;
create table Student(stNum varchar(255), Fname varchar(255), Lname varchar(255), Age int, Telephone varchar(255), Email varchar(255), Address varchar(255), primary key(stNum));
INSERT INTO Student (stNum, Fname, Lname, Age, Telephone, Email, Address) VALUES
('DA2G93D','Lars','Andersson',26,'07-71793336','kivaba3175@ineedsa.com','Stackekärr 121, Dyltabruk'),
('K88ZP8O','Anna','Nilsson',25,'07-79156016','veter22@aosdeag.com','Mogata Sjöhagen 60, Bullaren'),
('W6T5WZG','Anders','Johansson',29,'07-72240308','slabody@iaintel.com','Fuglie 80, Umeå'),
('PTQY0BQ','Maria','Karlsson',27,'07-77038419','anzhelagrechka@distraplo.com','Orrspelsv 130, Lycksele'),
('F62FDT84','Mikael','Mountain',26,'07-74215021','marusiam85@epubd.site','Sandviken 57, Dyltabruk');
select * from student;

create table Book(ISBN varchar(10), Title varchar(255), Author varchar(255),shelfnum varchar(255),numOfcopies int, primary key(ISBN));
INSERT INTO Book (ISBN,Title, Author, shelfNum, numOfCopies) VALUES
('F-0055-G', 'De kommer att drunkna i sina mödrars tårar', 'Johannes Anyuru','PER-5',4),
('A-0080-Z', 'Folk med ångest', 'Fredrik Backman','PER-5',4),
('H-0037-M','Välkommen till Amerika', 'Linda Boström Knausgård','SEM-1',4),
('A-0030-B','Silvervägen', 'Stina Jackson','PIN-4',5),
('C-0050-K','Drömfakulteten', 'Sara Stridsberg','PAS-3',4),
('H-0082-M','Inlandet', 'Elin Willows','NAM-8',5);
select * from book;

create table BookLease(leaseNumber int,ISBN varchar(25),stNum varchar(25) ,startDate date,leaseInDays int,dateReturned date, primary key(leasenumber), foreign key(ISBN) references Book(ISBN), foreign key(stnum) references student(stnum));
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
select * from booklease;
#(select * from student left join booklease on student.stnum = booklease.stnum)
 #union 
 #(select * from booklease right join student on booklease.stnum = student.stnum);
 
 # 2. show student that have not borrowed a book. needs to have stNum, Fname, Lname and numOfLeases.
select student.stNum,Fname,Lname,0 numOfLeases from student left join booklease on student.stNum = booklease.stNum where leasenumber is null;
 
 # 3. show books and there avrage leasetime ony compleated (lease in days)
select book.ISBN, title, avg(leaseInDays) from book left join booklease on book.ISBN = booklease.ISBN where datereturned is not null group by ISBN;

# 4. create a view that show the books curently rented. Needs to have ISBN, Title, Fname, Lname, ExpetedDate.
create view myview as 
select booklease.ISBN, Title, Fname, Lname,(date_add(startdate,interval leaseInDays day))ExpectedDate from Booklease left join book on Booklease.ISBN = book.ISBN left join student on booklease.stnum = student.stnum 
where datereturned is null;
select * from myview;

# 5. create a trigger that updates the Book's number of copies with +1 when book is returned.
DELIMITER //
create trigger Booklease_trigger after update on booklease for each row 
Begin
if NEW.dateReturned is not null then 
	update book set numofcompies = numofcopies+1 where book.ISBN = New.ISBN;
end if;
end; //
DELIMITER ;

# 6. create a poseider that check that the number of copies needs to be above 0 to be leased out. if numOfopie is 0 den abort the lease. 
# if avalible it inserts the new row into the booklease tabele, decrese the numOfcopies and display the message "Row inserted"
# else nothing wil happend and it will display the message Row NOT inserted! No copies avalible"
DELIMITER //
create procedure lease_a_Book(IN ISBNcode varchar(25),IN stnumber varchar(50),in istartdate date,in amountofdays int)
begin
declare booler bool;
declare ileasenumber int;
select Max(leasenumber)+1 from booklease into ileasenumber;
set booler = false;
select exists(select 1 from book where numofcopies > 0 and ISBN=ISBNcode) into booler;
if booler = true then 
	insert into booklease
    values(ileasenumber,ISBNcode,stnumber,istartdate, amountofdays,null);
    update book set numOfcopies=numOfcopies-1 where ISBN = ISBNcode;
	select "ROW INSERTED" as "";
else 
	select "DE DÄR GÅR INTE" as "";
end if;

end; //
DELIMITER ; 

# 7. selekt all student's leases and what book they borrowed including students that have not borrowed yet. it should show stNum, combined Fname and Lname as Name, ISBN and leaseNumber in desending order. 
select student.stNum, concat(FName," ",Lname) name_, leaseNumber, booklease.ISBN  from booklease left join student on booklease.stnum = student.stnum left join book on book.isbn = booklease.isbn order by leasenumber desc;

# (extra, create a lease)
select * from book;
select * from booklease;
call lease_a_book('A-0080-Z','Bajakuja','2020-11-10',3);
insert into student
value('bajakuja','Bajakuja','Ketchupsky',12,'1337-69-101','SenbonSakura.godmail.com','Spiritworld');