-- Anna Bergknut
-- 1.Skapa tabellerna ovan, sätt lämpliga primär- och främmande nycklar för tabellerna. Nedanstående data skall in i tabellerna.
create database CraftsmanLabTest;

create table Craftsman(craftsmanNumber int, craftsmanName varchar(50), competence varchar(50), price int, primary key (craftsmanNumber));
INSERT INTO Craftsman(craftsmanNumber, craftsmanName, competence, price) VALUES
  (1, "Kalle Anka", "Målare", 540),
  (2, "Kajsa Kavat", "Snickare", 840),
  (3, "Ronja Rdotter", "Plåtslagare", 270),
  (4, "Pelle S", "Murare", 620),
  (5, "Knatte", "Murare", 670);
 select * from Craftsman;
 
 create table Customer (customerNumber int, customerName varchar(50), address varchar(50), phoneNumber varchar(50), primary key (customerNumber));
  INSERT INTO Customer (customerNumber, customerName, address, phoneNumber) VALUES
  (1, "Ada Asson", "HemmaIHuset", "070-12345"),
  (2, "Beda Bsson", "StuganVidVägen", "070-67890"),
  (3, "Ceasar Csson", "Någonstans", "070-13579"),
  (4, "Dino", "Where", "070-24680"),
  (5, "Eve Esson", "Here", "070-4044044"),
  (6, "Fabian Fsson", "Here", "070-1011011");
  select * from Customer;

 create table Job (jobNumber int, craftsmanNumber int, customerNumber int, startDate varchar(50), jobtime int, primary key (jobNumber), foreign key (customerNumber) references CustomerA(customerNumber), foreign key (craftsmanNumber) references CraftsmanA(craftsmanNumber));
 INSERT INTO Job (jobNumber, craftsmanNumber, customerNumber, startDate, jobtime) VALUES
  (1, 1, 1, "2017-10-10", 24),
  (2, 1, 3, "2017-12-12", 30),
  (3, 2, 1, "2017-12-10", 30),
  (4, 2, 2, "2017-12-12", 15),
  (5, 2, 3, "2018-05-20", 15),
  (6, 2, 4, "2018-03-03", 24),
  (7, 3, 1, "2018-04-20", 18),
  (8, 3, 2, "2018-05-05", 9),
  (9, 4, 1, "2018-06-05", 6),
  (10,4, 2, "2018-06-06", 6);  
  select * from Job;
  
  -- 2. Skriv en SQL-sats som visar hantverkarna och deras utförda arbeten. Resultattabellen ska visa följande kolumner: hantverkarens namn, hantverkarens yrke, startdatum för arbetet, och lagd tid på arbetet.
select Craftsman.craftsmanName, Craftsman.competence, Job.startDate, Job.jobtime from Craftsman, Job where Job.craftsmanNumber = Craftsman.craftsmanNumber;

-- 3. Skriv en SQL-sats som visar varje kund och deras totala inköpta arbetstid. Resultattabellen skall visa följande kolumner: kundens namn, telefonnummer, och totala inköpta arbetstid.
select customerName, phoneNumber , sum(jobtime) from Customer, Job where Customer.customerNumber = job.customerNumber group by Customer.customerName;

-- 4. Skapa en vy som visar hur mycket en hantverkare tjänat totalt på sina olika jobb fram tills 2018-05-15 med kolumnerna hantverkarens namn, och total inkomst.
create view theview as
select craftsmanName, (Craftsman.price* sum(Job.jobtime))totalGain 
from Craftsman, Job 
where Craftsman.craftsmanNumber = job.craftsmanNumber and Job.startDate >= 2018-05-15 
group by craftsmanName;
select * from theview;

-- 5. Skapa en trigger på tabellen Job som, när man gör en bokning, kollar om det nya jobbet är bokat på mindre än 2 timmar. Vi alla vet att det minst tar 2 timmar att göra valfritt arbete, så om den nya bokningen är mindre än 2 timmar, ändra den till 2.
DROP TRIGGER IF EXISTS ShortJob;
DELIMITER //
create trigger ShortJob after update on Job for each row 
Begin
if NEW.jobtime < 2 then 
	update job set jobtime = 2 where jobNumber = New.jobNumber;
end if;
end; //
DELIMITER ;

-- 6. Skapa en procedur som hanterar bokningen av ett arbete. Två arbeten för samma hantverkare kan inte påbörjas samma dag, en kontroll för detta måste ske i proceduren.
-- i never got this to work even if i tried with three different methods. 
-- one that i copied from your lesson with the count the second one with a bood witch i think was the cleanest and the last one with a while.
DROP PROCEDURE IF EXISTS theData;
DELIMITER //
CREATE PROCEDURE theData (in ijobNumber int, in icraftsmanNumber int, in icustomerNumber int, in istartDate varchar(50), in ijobtime int, out outvar text)
BEGIN
DECLARE flag INT DEFAULT 0;
-- declare booler bool; # bool ide
-- set booler = false; # bool ide
-- select exists (select 1 from FROM Job WHERE craftsmanNumber = icraftsmanNumber AND startDate = istartDate) into booler; # bool idea. it didn't like the fist select for some reason.
-- while craftsmanNumber = icraftsmanNumber AND startDate = istartDate do # while ide
-- set flag = 1; # while ide
SELECT COUNT(1) INTO flag FROM Job WHERE craftsmanNumber = icraftsmanNumber AND startDate = istartDate; # count ide
if flag=1 then # bool = true
SET outvar = 'Row NOT Inserted';
elseif flag= 0 then
INSERT INTO Job (jobNumber, craftsmanNumber, customerNumber, startDate, jobtime) VALUES (ijobNumber, icraftsmanNumber, icustomerNumber, istartDate, ijobtime);
SET outvar = 'Row Inserted';
END IF;
-- end while; # while ide
END; //
DELIMITER ;

CALL theData (11, 4, 3, "2018-06-06", 10, @myVal); #Should not pass
SELECT @myVal AS OUTPUT;
CALL theData (11, 4, 3, "2018-06-07", 10, @myVal); #Should pass
SELECT @myVal AS OUTPUT;

select * from Job; # just to test 
delete from Job where jobNumber = 11; # just to test

-- 7. Skriv en SQL-sats som visar varje hantverkare, varje jobb hantverkarna gjort, och vilken kund varje jobb gjorts för. Om en hantverkare inte jobbat, skall denne ändå visas i resultatet. Resultattabellen skall visa följande kolumner: craftsmanNumber, craftsmanName, jobNumber, customerNumber

 select Craftsman.craftsmanNumber, Craftsman.craftsmanName, Job.jobNumber, Job.customerNumber from Job, Craftsman where Craftsman.craftsmanNumber=Job.craftsmanNumber;
  
  
  