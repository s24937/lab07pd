import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import sqlite3

def fetch_data():
    try:
        mydb = sqlite3.connect("studenci.db")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT o.IDOcena, s.Imie, s.Nazwisko, p.Nazwa, o.[Ocena] FROM Student AS s JOIN Ocena AS o ON o.IDStudent=s.IDStudent JOIN Przedmiot AS p ON p.IDPrzedmiot = o.IDPrzedmiot")

        result = mycursor.fetchall()
        mydb.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()
    return result
def load_data():
    data = fetch_data()

    treeview.delete(*treeview.get_children())
    for row in data:
        treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Dodaj nowgo studenta")

    imie_label = ttk.Label(new_window,text="Imie:")
    imie_label.pack()
    imie_entry = ttk.Entry(new_window)
    imie_entry.pack()

    nazwisko_label = ttk.Label(new_window, text="Nazwisko:")
    nazwisko_label.pack()
    nazwisko_entry = ttk.Entry(new_window)
    nazwisko_entry.pack()

    przedmiot_label = ttk.Label(new_window, text="Nazwa przedmiotu:")
    przedmiot_label.pack()
    przedmiot_entry = ttk.Entry(new_window)
    przedmiot_entry.pack()

    ocena_label = ttk.Label(new_window, text="Ocena")
    ocena_label.pack()
    ocena_entry = ttk.Entry(new_window)
    ocena_entry.pack()

    def add_new():
        new_imie = imie_entry.get()
        new_nazwisko = nazwisko_entry.get()
        new_przedmiot = przedmiot_entry.get()
        new_ocena = ocena_entry.get()

        try:
            mydb = sqlite3.connect("studenci.db")
            mycursor = mydb.cursor()

            mycursor.execute("SELECT Nazwa FROM Przedmiot WHERE Nazwa = (?)", (new_przedmiot,))
            if mycursor.fetchall() == []:
                mycursor.execute("INSERT INTO Przedmiot (Nazwa) VALUES (?)", (new_przedmiot,))
            mycursor.execute("SELECT Imie, Nazwisko FROM Student WHERE Imie == (?) AND Nazwisko == (?)",
                             (new_imie, new_nazwisko))
            if mycursor.fetchall() == []:
                mycursor.execute("INSERT INTO Student (Imie,Nazwisko) VALUES (?,?)", (new_imie, new_nazwisko))
            mycursor.execute("SELECT IdStudent FROM Student WHERE Imie == (?) AND Nazwisko == (?)",
                             (new_imie, new_nazwisko))
            IdStudent = mycursor.fetchall()[0][0]
            mycursor.execute("SELECT IdPrzedmiot FROM Przedmiot WHERE Nazwa == (?)", (new_przedmiot,))
            IdPrzedmiot = mycursor.fetchall()[0][0]
            mycursor.execute("INSERT INTO Ocena (IdStudent,IdPrzedmiot,Ocena) VALUES (?,?,?)",
                             (IdStudent, IdPrzedmiot, new_ocena))
            mydb.commit()

        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()

        load_data()

        new_window.destroy()

    add_button = ttk.Button(new_window, text="Dodaj", command=add_new)
    add_button.pack()

def open_details_window(event):
    selected_item = treeview.focus()
    if selected_item:
        item_data = treeview.item(selected_item)
        item_values = item_data["values"]

    details_window = tk.Toplevel(root)
    details_window.title("Szczegóły")

    id_label = ttk.Label(details_window, text="ID:")
    id_label.pack()
    id_entry = ttk.Entry(details_window)
    id_entry.insert(0, item_values[0])
    id_entry.config(state="disabled")
    id_entry.pack()

    imie_label = ttk.Label(details_window, text="Imie:")
    imie_label.pack()
    imie_entry = ttk.Entry(details_window)
    imie_entry.insert(0, item_values[1])
    imie_entry.pack()

    nazwisko_label = ttk.Label(details_window, text="Nazwisko:")
    nazwisko_label.pack()
    nazwisko_entry = ttk.Entry(details_window)
    nazwisko_entry.insert(0, item_values[2])
    nazwisko_entry.pack()

    przedmiot_label = ttk.Label(details_window, text="Przedmiot:")
    przedmiot_label.pack()
    przedmiot_entry = ttk.Entry(details_window)
    przedmiot_entry.insert(0, item_values[3])
    przedmiot_entry.pack()

    ocena_label = ttk.Label(details_window, text="Ocena:")
    ocena_label.pack()
    ocena_entry = ttk.Entry(details_window)
    ocena_entry.insert(0, item_values[4])
    ocena_entry.pack()

    def delete_data():
        try:
            mydb = sqlite3.connect("studenci.db")
            mycursor = mydb.cursor()
            mycursor.execute("DELETE FROM Ocena WHERE IDOcena = (?)", (id_entry.get(),))
            mydb.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
        load_data()

    delete_button = ttk.Button(details_window, text="Usuń Ocene", command=delete_data)
    delete_button.pack()

    def update_data():
        try:
            mydb = sqlite3.connect("studenci.db")
            mycursor = mydb.cursor()

            mycursor.execute(
                "SELECT p.IdPrzedmiot FROM Przedmiot AS p JOIN Ocena AS o ON p.IdPrzedmiot=o.IdPrzedmiot WHERE o.IdOcena = (?)",
                (id_entry.get(),))
            result = [mycursor.fetchall()[0]][0][0]
            if result != []:
                mycursor.execute("UPDATE Przedmiot SET Nazwa = (?) WHERE IdPrzedmiot = (?)",
                                 (przedmiot_entry.get(), result))

            mycursor.execute(
                "SELECT s.IdStudent FROM Student AS s JOIN Ocena AS o ON s.IdStudent=o.IdStudent WHERE o.IdOcena = (?)",
                (id_entry.get(),))
            result = [mycursor.fetchall()[0]][0][0]
            if result != []:
                mycursor.execute("UPDATE Student SET Imie = (?), Nazwisko = (?) WHERE IdStudent = (?)",
                                 (imie_entry.get(), nazwisko_entry.get(), result))
            mycursor.execute("UPDATE Ocena SET Ocena = (?) WHERE IdOcena = (?)", (ocena_entry.get(), id_entry.get()))
            mydb.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
        finally:
            if mycursor:
                mycursor.close()
            if mydb:
                mydb.close()
        load_data()

    update_button = ttk.Button(details_window, text="Zaaktualizuj informacje", command=update_data)
    update_button.pack()

root = tk.Tk()

screen_width = get_monitors()[0].width
screen_height = get_monitors()[0].height

root.title()
root.geometry(f"{int(screen_width/2)}x{int(screen_height/2)}")
root.iconbitmap("./bookshelf.ico")

treeview = ttk.Treeview(root)
treeview["columns"] = ("id", "imie", "nazwisko", "przedmiot", "ocena")
treeview.pack()
treeview.heading("id", text="Id")
treeview.heading("imie", text="Imie")
treeview.heading("nazwisko", text="Nazwisko")
treeview.heading("przedmiot", text="Przedmiot")
treeview.heading("ocena", text="Ocena")
treeview.column("#0", width=0)

add_new_book_button = tk.Button(root, text="Dodaj nową ocene", command=open_new_window)
add_new_book_button.pack()

treeview.bind("<Double-1>", open_details_window)

load_data()

root.mainloop()








