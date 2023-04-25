-- Anna Bergknut
-- 1. Create a database and tables
create database temp;

create table Craftsman(craftsmanNumber int , craftsmanName varchar(50), comentence varchar(50), price int, primary key (craftsmanNumber));
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
INSERT INTO Job (jobNumber, craftsmanNumber, customerNumber, startDate, duration) VALUES
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

-- 3. Skriv en SQL-sats som visar varje kund och deras totala inköpta arbetstid. Resultattabellen skall visa följande kolumner: kundens namn, telefonnummer, och totala inköpta arbetstid.
-- 4. Skapa en vy som visar hur mycket varje hantverkare tjänat totalt på deras olika jobb fram tills 2018-05-15 med kolumnerna hantverkarens namn, och total inkomst.

#select craftsmanName, (CraftsmanA.price*(CraftsmanA.price))totalGain from CraftsmanA left join craftsmanName on CraftsmanA.craftsmanNumber = jobA.craftsmanNumber right join JobA on JobA.startdate >= 2018-05-15 group by craftsmanName;
#select craftsmanName, (CraftsmanA.price*(CraftsmanA.price))totalGain from CraftsmanA, JobA where CraftsmanA.craftsmanNumber = jobA.craftsmanNumber and JobA.startdate >= 2018-05-15 group by craftsmanName;


-- 5. Skapa en trigger på tabellen Job som, när man gör en bokning, kollar om det nya jobbet är bokat på mindre än 2 timmar. Vi alla vet att det minst tar 2 timmar att göra valfritt arbete, så om den nya bokningen är mindre än 2 timmar, ändra den till 2.
-- 6. Skapa en procedur som hanterar bokningen av ett arbete. Två arbeten för samma hantverkare kan inte påbörjas samma dag, en kontroll för detta måste ske i proceduren.
declare booler bool;
set booler = false;
select exists (select 1 from FROM Job WHERE craftsmanNumber = icustomerNumber AND startDate = istartDate) into booler;
if booler = true then 
-- 7. Skriv en SQL-sats som visar varje hantverkare, varje jobb hantverkarna gjort, och vilken kund varje jobb gjorts för. Om en hantverkare inte jobbat, skall denne ändå visas i resultatet. Resultattabellen skall visa följande kolumner: craftsmanNumber, craftsmanName, jobNumber, customerNumber
  
  