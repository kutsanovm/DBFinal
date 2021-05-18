import csv
import mysql.connector
from tabulate import tabulate
import pandas as pd
from pandas import DataFrame
from faker import Faker
import sys

db = mysql.connector.connect(
    host="35.236.32.138",
    user="michelle",
    password="chapmanrules",
    database="StudentsMK"
    )

curr = db.cursor()
fake = Faker()

def getProf():
    profs = ["Tony Stark", "Steve Rogers", "Sam Wilson", "Bruce Banner", "Peter Parker", "Wanda Maximoff", "Pietro Maximoff", "Clint Barton", "Natasha Romanoff", "Steven Strange", "Thor Odinson", "Loki Odinson", "Bucky Barnes", "T'Challa", "James Rhodes"]
    prof = fake.word(ext_word_list=profs)
    return prof

def getRA():
    ras = ["Pepper Potts", "Yondu", "Wong", "Shuri", "Valkyrie", "Korg", "May Lang", "Happy Hogan", "Ned Leeds", "Hank Pym", "Peggy Carter", "Sharon Carter", "Jane Foster", "Jimmy Woo", "Darcy Lewis"]
    ra = fake.word(ext_word_list=ras)
    return ra

def getPower():
    powers = ["Invisibility", "Telekonesis", "Strength", "Teleportation", "Shapeshifting", "Witch-like powers", "Immortality", "Time Travel", "X-Ray Vision", "Magnetism", "Weather Modification", "Elements"]
    power = fake.word(ext_word_list=powers)
    return power

def GenData():
    curr = db.cursor()

    for x in range(int(5)):
        print("Importing Student Data")
        curr.execute("INSERT INTO StudentHomeroom(Professor, ClassRoomNumber)"
                     "VALUES (%s, %s);", (getProf(), fake.random_digit_not_null()))
        ProfessorID = curr.lastrowid
        db.commit()

        curr.execute("INSERT INTO StudentHousing(RA, Address)"
                     "VALUES (%s, %s);", (getRA(), fake.address()))
        HousingID = curr.lastrowid
        db.commit()

        curr.execute("INSERT INTO StudentPersonalInfo(BirthDate, Superpower)"
                     "VALUES (%s, %s);", (fake.date_of_birth(maximum_age=22), getPower()))
        PersonnelID = curr.lastrowid
        StudentID = curr.lastrowid
        db.commit()

        curr.execute("INSERT INTO MarvelStudent(FirstName, LastName, StudentID, HousingID, ProfessorID, PersonnelID) "
                     "VALUES (%s, %s, %s, %s, %s, %s);",
                     (fake.first_name(), fake.last_name(), StudentID, HousingID, ProfessorID, PersonnelID))
        db.commit()
    print("Import Successful\n")

#7.Generate reports that can be exported (excel or csv format)
def menuOptions():
    curr = db.cursor()

    print("1. To display records in the current databases, enter '1': ")
    print("2. To search and query results, enter '2': ")
    print("3. To insert new Marvel Students, enter '3'.")
    print("4. To delete a Marvel Student record, enter '4'.")
    print("5. To generate a report and export it as a CSV, enter '5'.")
    print("6. To update a student field (Address, RA, Professor), enter '6'.")
    print("7. To finish with the dataset, enter 'e'.\n")

    usr = input("Enter here: ")
    #print(usr)



    while usr != 'e':
        if usr == '1':
            try:
                curr.execute("SELECT * FROM AllDataView")
                res = curr.fetchall()
                print(tabulate(res, headers=['FirstName', 'LastName', 'Superpower', 'Professor', 'RA'], tablefmt='psql'))

                usr = input("\nWould you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
            except TypeError as e:
                print("Unexpected Error While Displaying\n", e)
            db.commit()

        if usr == '6':
            search_id = input("\nWhat is the Student ID of the student you are updating?: ")
            print("Would you like to update the address('a'), RA('ra'), or Professor('p')?:")
            usr = input("Enter here ('e' to exit): ")
            specific_upd = input("What would you like to change it to?: ")

            if usr == 'p':
                try:
                    #cursor = conn.cursor()
                    curr.execute("UPDATE UpdateProfessorView SET Professor = %s WHERE StudentID = %s", (specific_upd, search_id,))
                    print("Update has been made\n")
                    db.commit()
                    curr.close()

                    back = input("To undo this action, enter 'undo'. To continue, enter 'cont':")
                    if back == "undo":
                        curr.Rollback()

                    usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Updating\n", e)

            elif usr == 'a':
                try:
                    #cursor = conn.cursor()
                    curr.execute("UPDATE UpdateAddressView SET Address = %s WHERE StudentID = %s", (specific_upd, search_id,))
                    print("Update has been made\n")
                    db.commit()
                    curr.close()

                    back = input("To undo this action, enter 'undo'. To continue, enter 'cont':")
                    if back == "undo":
                        curr.Rollback()

                    usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Updating\n", e)

            elif usr == 'ra':
                try:
                    #cursor = conn.cursor()
                    curr.execute("UPDATE UpdateRAView SET RA = %s WHERE StudentID = %s", (specific_upd, search_id,))
                    print("Update has been made\n")
                    db.commit()
                    curr.close()

                    back = input("To undo this action, enter 'undo'. To continue, enter 'cont':")
                    if back == "undo":
                        curr.Rollback()

                    usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Updating\n", e)


        if usr == "2":
            print("\nThere are many variables to query your search by.")
            print("If you want to query by Superpowers, enter 'powers'.") #group-by
            print("If you want to query by BirthDate, enter 'birthday'.")  # sub-query
            print("If you want to query by Professors only, enter 'prof'.")
            print("To get a count of students with each power, enter 'count'.") #inner join

            usr = input("Enter here:")
            if usr == 'powers':
                try:

                    curr.execute("SELECT Superpower FROM AllDataView")

                    pow = curr.fetchall()
                    print(tabulate(pow, headers=['Superpower'], tablefmt='psql'))

                    search_by = input("Which superpower are you searching for?: ")

                    curr.execute("SELECT FirstName, LastName, Superpower, Professor FROM AllDataView WHERE Superpower = %s", (search_by,))

                    # curr.execute("SELECT * FROM StudentHomeroomView WHERE Professor = %s", (search_by,))
                    pow1 = curr.fetchall()

                    print("Your search results:\n ")

                    print(
                        tabulate(pow1, headers=['FirstName', 'LastName', 'Superpower', 'Professor'], tablefmt='psql'))

                    curr.close()


                    usr = input("\nWould you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Querying\n", e)
                db.commit()

            elif usr == 'prof':
                try:
                    curr.execute("SELECT Professor FROM AllDataView")

                    prof = curr.fetchall()
                    print(tabulate(prof, headers=['Professor'], tablefmt='psql'))

                    search_by = input("Which professor are you searching for?: ")

                    curr.execute("SELECT MarvelStudent.FirstName, MarvelStudent.LastName, StudentPersonalInfo.Superpower, StudentHomeroom.Professor FROM MarvelStudent JOIN StudentPersonalInfo ON StudentPersonalInfo.PersonnelID = MarvelStudent.PersonnelID JOIN StudentHomeroom ON StudentHomeroom.ProfessorID = MarvelStudent.ProfessorID WHERE Professor = %s", (search_by,))

                    #curr.execute("SELECT * FROM StudentHomeroomView WHERE Professor = %s", (search_by,))
                    prof1 = curr.fetchall()

                    print("Your search results:\n ")

                    print(tabulate(prof1, headers=['FirstName', 'LastName', 'Superpower', 'Professor'], tablefmt='psql'))

                    curr.close()

                    usr = input("\nWould you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")

                except mysql.Error as e:
                    print("Unexpected Error While Querying\n", e)
                db.commit()

            elif usr == 'birthday':

                try:

                    curr.execute("SELECT Birthdate FROM StudentBirthdayView")
                    bd = curr.fetchall()
                    print(tabulate(bd, headers=['Birthday'], tablefmt='psql'))

                    print("What is the max birth year you would like to query data from?\n")
                    search_by = int(input("Enter here: "))
                    #search_by = input("Which professor are you searching for?: ")


                    curr.execute("SELECT * FROM StudentBirthdayView WHERE (YEAR(Birthdate)) <= %s", (search_by,))
                    bd1 = curr.fetchall()

                    print("Your search results:\n ")

                    print(tabulate(bd1, headers=['FirstName', 'LastName', 'Birthday'], tablefmt='psql'))

                    curr.close()

                    usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Querying\n", e)
                db.commit()

            elif usr == 'count':
                try:
                    #curr.execute("SELECT FirstName, LastName, RA FROM AllDataView GROUP BY RA")

                    curr.execute("SELECT COUNT(FirstName + LastName), Superpower FROM AllDataView GROUP BY Superpower")
                    ar = curr.fetchall()

                    print("Your search results:\n ")
                    print(tabulate(ar, headers=['Count of Students', 'Superpower'], tablefmt='psql'))

                    curr.close()

                    usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
                except mysql.Error as e:
                    print("Unexpected Error While Querying\n", e)
                db.commit()

        if usr == "3":
            try:
                f_name = input("\nEnter First Name: ")
                l_name = input("Enter Last Name: ")
                prof = input("Enter Professor: ")
                addy = input("Enter Address: ")
                classroom = int(input("Enter Classroom Number: "))
                birth = input("Enter Birth Date (format 0000-00-00):")
                pow = input("Enter Superpower: ")
                ra = input("Enter RA: ")

                curr = db.cursor()

                curr.execute(
                    "INSERT INTO MarvelStudent(FirstName, LastName) VALUES(%s,%s)",
                    (f_name, l_name,))
                db.commit()

                curr.execute(
                    "INSERT INTO StudentHomeroom(Professor, ClassRoomNumber) VALUES(%s,%s)",
                    (prof, classroom,))
                db.commit()

                curr.execute(
                    "INSERT INTO StudentHousing(Address, RA) VALUES(%s,%s)",
                    (addy, ra,))
                db.commit()

                curr.execute(
                    "INSERT INTO StudentPersonalInfo(BirthDate, Superpower) VALUES(%s,%s)",
                    (birth, pow,))
                db.commit()

                curr.close()
                print("New Student Added\n")
                back = input("To undo this action, enter 'undo'. To continue, enter 'cont':")
                
                if back == "undo":
                    curr.Rollback()

                usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
            except mysql.Error as e:
                print("Unexpected Error While Inserting\n", e)

        if usr == "4":
            delete_student = input("What is the ID of the Student you are deleting?: ")
            try:
                #curr = db.curr()
                curr.execute("DELETE FROM MarvelStudent WHERE StudentID = %s", (delete_student,))
                db.commit()

                curr.execute("DELETE FROM StudentHomeroom WHERE ProfessorID = %s", (delete_student,))
                db.commit()

                curr.execute("DELETE FROM StudentHousing WHERE HousingID = %s", (delete_student,))
                db.commit()

                curr.execute("DELETE FROM StudentPersonalInfo WHERE PersonnelID = %s", (delete_student,))
                db.commit()

                print("Delete has been made\n")

                back = input("To undo this action, enter 'undo'. To continue, enter 'cont':")
                if back == "undo":
                    curr.Rollback()

                usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")

            except mysql.Error as e:
                print("Unexpected Error While Deleting\n", e)

        if usr == "5":
            try:
                exportCSV()
                usr = input("Would you like to keep manipulating the database ('e' to exit) ?: ('1', '2', '3', '4', '5', '6'):")
            except mysql.Error as e:
                print("Unexpected Error While Creating File\n", e)

def exportCSV():
    #csv_file = open('marvel.csv', "w")
    #writer = csv.writer(csv_file)
    #writer.writerow(["FirstName", "LastName", "Superpower", "Professor", "RA"])

    #curr.execute("SELECT * FROM AllDataView INTO OUTFILE '/Users/michellekutsanov/PycharmProjects/pythonProject1/marvel.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' FIELDS ESCAPED BY '\' LINES TERMINATED BY '\n'")
    curr.execute("SELECT * FROM AllDataView")

    # curr.execute("SELECT * FROM StudentHomeroomView WHERE Professor = %s", (search_by,))
    co = curr.fetchall()

    df = pd.DataFrame(co, columns=['FirstName', 'LastName', 'Superpower', 'Professor', 'RA'])
    df.to_csv('marvel.csv')
    print("CSV file successfully created.")
    db.commit()
    curr.close()

GenData() #only uncomment this on the first initial run of the code
menuOptions()


