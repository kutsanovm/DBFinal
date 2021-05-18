DROP TABLE MarvelStudent;
DROP TABLE StudentHomeroom;
DROP TABLE StudentPersonalInfo;
DROP TABLE StudentHousing;

CREATE TABLE StudentHomeroom(
    ProfessorID int primary key auto_increment,
    Professor varchar(50),
    ClassRoomNumber int
);

CREATE TABLE StudentPersonalInfo(
    PersonnelID int primary key auto_increment,
    BirthDate date,
    Superpower varchar(50)
);

CREATE TABLE StudentHousing(
    HousingID int primary key auto_increment,
    Address varchar(70),
    RA varchar(50)
);

CREATE TABLE MarvelStudent(
        StudentID int primary key auto_increment,
        PersonnelID int,
        ProfessorID int,
        HousingID int,
        FirstName varchar(50),
        LastName varchar(50),
        FOREIGN KEY (PersonnelID) references StudentPersonalInfo(PersonnelID),
        FOREIGN KEY (ProfessorID) references StudentHomeroom(ProfessorID),
        FOREIGN KEY (HousingID) references StudentHousing(HousingID)
);

DROP VIEW StudentHomeroomView;
DROP VIEW StudentPowerView;

DROP VIEW UpdateProfessorView;
DROP VIEW UpdateRAView;
DROP VIEW UpdateAddressView;
DROP VIEW StudentBirthdayView;


CREATE VIEW StudentHomeroomView AS
SELECT FirstName, LastName, Professor
FROM MarvelStudent INNER JOIN StudentHomeroom ON MarvelStudent.ProfessorID = StudentHomeroom.ProfessorID;

CREATE VIEW StudentPowerView AS
SELECT FirstName, LastName, Superpower
FROM MarvelStudent INNER JOIN StudentPersonalInfo ON MarvelStudent.StudentID = StudentPersonalInfo.PersonnelID;

CREATE VIEW StudentBirthdayView AS
SELECT FirstName, LastName, Birthdate
FROM MarvelStudent INNER JOIN StudentPersonalInfo ON MarvelStudent.StudentID = StudentPersonalInfo.PersonnelID;

CREATE VIEW UpdateProfessorView
AS
SELECT MarvelStudent.StudentID AS StudentID, StudentHomeroom.Professor as Professor
FROM
     MarvelStudent
         JOIN
            StudentHomeroom ON StudentHomeroom.ProfessorID = MarvelStudent.ProfessorID;

DROP VIEW UpdateRAView;

CREATE VIEW UpdateRAView
AS
SELECT MarvelStudent.StudentID AS StudentID, StudentHousing.RA as RA
FROM
     MarvelStudent
         JOIN
            StudentHousing ON StudentHousing.HousingID = MarvelStudent.HousingID;

CREATE VIEW UpdateAddressView
AS
SELECT MarvelStudent.StudentID AS StudentID, StudentHousing.Address as Address
FROM
     MarvelStudent
         JOIN
            StudentHousing ON StudentHousing.HousingID = MarvelStudent.HousingID;

DROP VIEW AllDataView;

CREATE VIEW AllDataView
AS
SELECT MarvelStudent.FirstName AS FirstName, MarvelStudent.LastName as LastName, StudentPersonalInfo.Superpower as Superpower, StudentHomeroom.Professor as Professor, StudentHousing.RA as RA
FROM
     MarvelStudent
        JOIN
            StudentHomeroom ON StudentHomeroom.ProfessorID = MarvelStudent.ProfessorID
        JOIN
            StudentHousing ON StudentHousing.HousingID = MarvelStudent.HousingID
        JOIN
            StudentPersonalInfo ON StudentPersonalInfo.PersonnelID = MarvelStudent.PersonnelID;

