import sqlite3

db = sqlite3.connect("studenci.db")
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ocena (
        IDOcena INTEGER NOT NULL,
        IDStudent INTEGER NOT NULL,
        IDPrzedmiot INTEGER NOT NULL,
        Ocena varchar(3) NOT NULL,
        CONSTRAINT Ocena_PK PRIMARY KEY ("IDOcena" AUTOINCREMENT),
        CONSTRAINT Ocena_Przedmiot FOREIGN KEY (IDPrzedmiot)
        REFERENCES Przedmiot (IDPrzedmiot),
        CONSTRAINT Ocena_Student FOREIGN KEY (IDStudent)
        REFERENCES Student (IDStudent)
    
    );
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Przedmiot (
        IDPrzedmiot INTEGER NOT NULL, 
        Nazwa varchar(30) NOT NULL,
        CONSTRAINT "Przedmiot_PK" PRIMARY KEY("IDPrzedmiot" AUTOINCREMENT)
); 
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Student (
        IDStudent INTEGER NOT NULL ,
        Imie varchar(30) NOT NULL,
        Nazwisko varchar(30) NOT NULL,
        CONSTRAINT "Student_PK" PRIMARY KEY("IDStudent" AUTOINCREMENT)
);
''')

db.commit()
db.close()