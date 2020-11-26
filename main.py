# Intro to Python
# Alexander Hess
# Final

# Imports
# PyQT5, Regular Expression, SQLite3
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re
import sqlite3


# SQL Connection class
class SqlConnect:
    def __init__(self):
        self.eflag = False
        self.error = None
        self.db = None

    def create(self):
        if self.db is not None:
            sql_create_prime_table = """ CREATE TABLE IF NOT EXISTS People (
                                        id integer PRIMARY KEY,
                                        first text NOT NULL,
                                        last text NOT NULL,
                                        address text,
                                        city text,
                                        state text,
                                        zip text
                                        ); """

            sql_create_notes_table = """ CREATE TABLE IF NOT EXISTS Notes (
                                        id integer PRIMARY KEY,
                                        title text,
                                        note text,
                                        pid integer,
                                        FOREIGN KEY (pid) REFERENCES People(id)
                                        ); """

            c = self.db.cursor()

            c.execute(sql_create_prime_table)
            c.execute(sql_create_notes_table)

    def add_person(self, *data):
        # Query
        sql = ''' INSERT INTO people(first, last, address, city, state, zip)
                    VALUES(?,?,?,?,?,?) '''

        # Execution
        c = self.db.cursor()
        c.execute(sql, data)
        self.db.commit()

    def add_note(self, *data):
        # Query
        sql = ''' INSERT INTO notes(title, note, pid)
                    VALUES(?,?,?)'''

        # Execution
        c = self.db.cursor()
        c.execute(sql, data)
        self.db.commit()

    # Search by first name
    def search_people_fn(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE first=?", (data,))

        res = c.fetchall()

        return res

    # Search by last name
    def search_people_ln(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE last=?", (data,))

        res = c.fetchall()

        return res

    # Search by name
    def search_people_n(self, *data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE first=? AND last=?", (data,))

        res = c.fetchall()

        return res

    # Search by address
    def search_people_ad(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE address=?", (data,))

        res = c.fetchall()

        return res

    # Search by city
    def search_people_ct(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE city=?", (data,))

        res = c.fetchall()

        return res

    # Search by state
    def search_people_st(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE state=?", (data,))

        res = c.fetchall()

        return res

    # Search by zip
    def search_people_zp(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM people WHERE zip=?", (data,))

        res = c.fetchall()

        return res

    def get_notes(self, data):
        # Execution
        c = self.db.cursor()
        c.execute("SELECT * FROM notes WHERE pid=?", (data,))

        result = c.fetchall()

        return result

    def count_persons(self):
        # Query
        sql = ''' SELECT COUNT( id ) FROM people '''

        self.connect()
        c = self.db.cursor()
        c.execute(sql)

        return str(c.fetchone()[0])

    def count_notes(self):
        # Query
        sql = ''' SELECT COUNT( id ) FROM notes '''

        self.connect()
        c = self.db.cursor()
        c.execute(sql)

        return str(c.fetchone()[0])

    def close(self):
        self.db.close()

    def connect(self):
        try:
            self.db = sqlite3.connect("db")
        except sqlite3.Error as e:
            # If it errors, program will close
            self.error = e
            self.eflag = True


# # # # # # # # # #
# End of Database #
# # # # # # # # # #

# # # # # # # # # # # # #
# Start of GUI Sections #
# # # # # # # # # # # # #

# Add person class
class AddPersonWindow(QDialog):
    # Window for adding new persons
    def __init__(self, parent=None):
        super(AddPersonWindow, self).__init__(parent)

        self.layout = QGridLayout()

        # Labels
        self.firstlab = QLabel("First Name")
        self.lastlab = QLabel("Last Name")
        self.addresslab = QLabel("Address")
        self.citylab = QLabel("City")
        self.statelab = QLabel("State")
        self.ziplab = QLabel("Zip")

        # Input boxes
        self.first = QLineEdit()
        self.first.setToolTip("First Name")
        self.last = QLineEdit()
        self.last.setToolTip("Last Name, or initial")
        self.address = QLineEdit()
        self.address.setToolTip("Street Address")
        self.city = QLineEdit()
        self.city.setToolTip("City")
        self.state = QLineEdit()
        self.state.setToolTip("2 letter state code, i.e. CA")
        self.state.setMaxLength(2)
        self.zip = QLineEdit()
        self.zip.setToolTip("5 digit or 9 digit zip code (include '-')")
        self.zip.setMaxLength(10)

        # Buttons
        self.addbutton = QPushButton("Add")
        self.addbutton.clicked.connect(self.validate)
        self.cancelbutton = QPushButton("Cancel")
        self.cancelbutton.clicked.connect(self.close)

        # Add everything to layout

        self.layout.addWidget(self.firstlab, 1,0)
        self.layout.addWidget(self.first, 1,1)
        self.layout.addWidget(self.lastlab, 1,4)
        self.layout.addWidget(self.last, 1,5)
        self.layout.addWidget(self.addresslab, 2,0)
        self.layout.addWidget(self.address, 2,1, 1,3)
        self.layout.addWidget(self.citylab, 3,0)
        self.layout.addWidget(self.city, 3,1)
        self.layout.addWidget(self.statelab, 3,2)
        self.layout.addWidget(self.state, 3,3)
        self.layout.addWidget(self.ziplab, 3,4)
        self.layout.addWidget(self.zip, 3,5)
        self.layout.addWidget(self.addbutton, 5,1)
        self.layout.addWidget(self.cancelbutton, 5,3)

        self.setLayout(self.layout)
        self.setWindowTitle("Add Person")

    # Validate function
    def validate(self):
        # Set input validation flags
        fpass = False
        lpass = False
        apass = False
        cpass = False
        spass = False
        zpass = False

        # Validate
        # First name must start capitalized and be more than 1 letter
        if re.match('[A-Z][a-z]+', self.first.text()):
            fpass = True
            self.first.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.first.setStyleSheet("""QLineEdit { background-color: red }""")
        # Last name must start with a capital letter, may contain just initial or full
        if re.match('[A-Z][a-z]*', self.last.text()):
            lpass = True
            self.last.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.last.setStyleSheet("""QLineEdit { background-color: red }""")
        # Address must contain numbers and letters, obviously
        # Addresses have so much variation that validation standard is hard
        if re.match('[0-9]+[A-Z]* [A-Za-z ]*', self.address.text()):
            apass = True
            self.address.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.address.setStyleSheet("""QLineEdit { background-color: red }""")
        # City name, capitalized, Allowing up to 3 worded cities
        if re.match('([A-Z][a-z]*)|([A-Z][a-z]* [A-Z][a-z]*)|([A-Z][a-z]* [A-Z][a-z]* [A-Z][a-z]*)', self.city.text()):
            cpass = True
            self.city.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.city.setStyleSheet("""QLineEdit { background-color: red }""")
        # State, two letters capitalized
        if re.match('[A-Z]{2}', self.state.text()):
            spass = True
            self.state.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.state.setStyleSheet("""QLineEdit { background-color: red }""")
        # Zip code, 5 numbers or 5-4
        if re.match('[0-9]{5}', self.zip.text()) or re.match('[0-9]{5}[-][0-9]{4}', self.zip.text()):
            zpass = True
            self.zip.setStyleSheet("""QLineEdit { background-color: green }""")
        else:
            self.zip.setStyleSheet("""QLineEdit { background-color: red }""")

        # Complete Validation Check
        # If this fails, validation ends and no data is sent to database
        if fpass and lpass and apass and cpass and spass and zpass:
            db = SqlConnect()
            db.connect()

            # Send to db
            db.add_person(self.first.text(), self.last.text(), self.address.text(), self.city.text(),
                          self.state.text(), self.zip.text())

            db.close()

            self.accept()


# Search Person class
class SearchPersonWindow(QDialog):
    def __init__(self, parent=None):
        super(SearchPersonWindow, self).__init__(parent)

        self.results = None

        self.layout = QGridLayout()

        # Labels
        self.firstlab = QLabel("First Name")
        self.lastlab = QLabel("Last Name")
        self.addresslab = QLabel("Address")
        self.citylab = QLabel("City")
        self.statelab = QLabel("State")
        self.ziplab = QLabel("Zip")

        # Input boxes
        self.first = QLineEdit()
        self.first.setToolTip("First Name")
        self.last = QLineEdit()
        self.last.setToolTip("Last Name, or initial")
        self.address = QLineEdit()
        self.address.setToolTip("Street Address")
        self.city = QLineEdit()
        self.city.setToolTip("City")
        self.state = QLineEdit()
        self.state.setToolTip("2 letter state code, i.e. CA")
        self.state.setMaxLength(2)
        self.zip = QLineEdit()
        self.zip.setToolTip("5 digit or 9 digit zip code (include '-')")
        self.zip.setMaxLength(10)

        # Buttons
        self.searchbutton = QPushButton("Search")
        self.searchbutton.clicked.connect(self.searchDB)
        self.cancelbutton = QPushButton("Cancel")
        self.cancelbutton.clicked.connect(self.reject)

        # Add everything to layout

        self.layout.addWidget(self.firstlab, 1, 0)
        self.layout.addWidget(self.first, 1, 1)
        self.layout.addWidget(self.lastlab, 1, 4)
        self.layout.addWidget(self.last, 1, 5)
        self.layout.addWidget(self.addresslab, 2, 0)
        self.layout.addWidget(self.address, 2, 1, 1, 3)
        self.layout.addWidget(self.citylab, 3, 0)
        self.layout.addWidget(self.city, 3, 1)
        self.layout.addWidget(self.statelab, 3, 2)
        self.layout.addWidget(self.state, 3, 3)
        self.layout.addWidget(self.ziplab, 3, 4)
        self.layout.addWidget(self.zip, 3, 5)
        self.layout.addWidget(self.searchbutton, 5, 1)
        self.layout.addWidget(self.cancelbutton, 5, 3)

        self.slab = QLabel()
        self.layout.addWidget(self.slab, 6,1)

        self.setLayout(self.layout)
        self.setWindowTitle("Search Person")
        self.show()

    def searchDB(self):
        # DB connection
        self.slab.setText("Entering Search")

        db = SqlConnect()
        db.connect()

        # Variables
        first = self.first.text()
        last = self.last.text()
        address = self.address.text()
        city = self.city.text()
        state = self.state.text()
        zip = self.zip.text()

        self.slab.setText("Searching")
        # Search by whatever field is filled
        # Priority is by most specific first to most generalized
        if first != '':
            if last != '':
                self.slab.setText("Searching by name")
                self.results = db.search_people_n((first, last))
                self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
            else:
                self.slab.setText("Searching by first name")
                self.results = db.search_people_fn(first)
                self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
        elif self.last.text() != '':
            self.slab.setText("Searching by last name")
            self.results = db.search_people_ln(last)
            self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
        elif self.address.text() != '':
            self.slab.setText("Searching by address")
            self.results = db.search_people_ad(address)
            self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
        elif self.city.text() != '':
            self.slab.setText("Searching by city")
            self.results = db.search_people_ct(city)
            self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
        elif self.state.text() != '':
            self.slab.setText("Searching by state")
            self.results = db.search_people_st(state)
            self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")
        elif self.zip.text() != '':
            self.slab.setText("Searching by zip")
            self.results = db.search_people_zp(zip)
            self.slab.setText("Search Complete. " + str(len(self.results)) + " result(s).")

        db.close()

        displayresults(self.results)


# Display Search results, opens another window
def displayresults(results):
    # Display Results in new window
    disp = QDialog()
    disp.setWindowTitle("Results")

    layout = QVBoxLayout()

    # Number of results
    rlab = QLabel(str(len(results)) + " result(s).")
    layout.addWidget(rlab)

    # Results display
    listbox = extQListWidget()

    # Add results
    for x in results:
        listbox.addItem(str(x[0]) + ": " + str(x[1]) + " " + str(x[2]) + " " + str(x[4]) + ", " + str(x[5]))

    # Show full details on click
    listbox.itemDoubleClicked.connect(partial(listbox.displaydetails, results[listbox.currentRow()+1]))

    layout.addWidget(listbox)

    closewin = QPushButton("Close")
    closewin.clicked.connect(disp.close)
    layout.addWidget(closewin)

    disp.setLayout(layout)

    disp.show()
    disp.exec_()


# Extension of QListWidget
# Simply for custom click function
class extQListWidget(QListWidget):

    def displaydetails(self, results, item):
        fulldetails = QDialog()
        layout = QGridLayout()

        fulldetails.setWindowTitle(item.text())

        # Result labels
        entry = QLabel("Entry: " + str(results[0]))
        first = QLabel(str(results[1]))
        last = QLabel(str(results[2]))
        address = QLabel(str(results[3]))
        city = QLabel(str(results[4]))
        state = QLabel(str(results[5]))
        zip = QLabel(str(results[6]))

        # Add to layout
        layout.addWidget(entry, 0,0)
        layout.addWidget(first, 1,0)
        layout.addWidget(last, 1,1)
        layout.addWidget(address, 2,0, 1,3)
        layout.addWidget(city, 3,0)
        layout.addWidget(state, 3,1)
        layout.addWidget(zip, 3,2)

        addnote = QPushButton("Add New Note")
        addnote.clicked.connect(partial(addnewnote, results[0]))

        layout.addWidget(addnote, 4,1)

        closewin = QPushButton("Close")
        closewin.clicked.connect(fulldetails.reject)
        layout.addWidget(closewin, 4,2)

        # DB Query for notes
        db = SqlConnect()
        db.connect()
        notes = db.get_notes(results[0])
        db.close()

        notecount = QLabel(str(len(notes)) + " total notes")

        layout.addWidget(notecount, 5,0)

        # Display notes only if some exist
        if len(notes) > 0:
            notesbox = extQListWidget()

            for x in notes:
                notesbox.addItem(str(x[0]) + " " + str(x[1]))

            notesbox.itemDoubleClicked.connect(partial(notesbox.notedisplay, notes[notesbox.currentRow()+1]))

            layout.addWidget(notesbox, 6,0, 5,3)

        fulldetails.setLayout(layout)

        fulldetails.show()
        fulldetails.exec_()

    def notedisplay(self, note, item):
        notedetails = QDialog()
        notedetails.setWindowTitle(str(note[1]))

        layout = QVBoxLayout()

        # Display note, cannot be edited
        message = QTextEdit()
        message.setText(str(note[2]))
        message.setReadOnly(True)
        message.setMaximumSize(300,500)

        layout.addWidget(message)

        okbtn = QPushButton("Ok")
        okbtn.clicked.connect(notedetails.accept)

        layout.addWidget(okbtn)

        notedetails.setLayout(layout)

        notedetails.show()
        notedetails.exec_()


# Add New Note
def addnewnote(pid):
    notewindow = QDialog()
    notewindow.setWindowTitle("Add Note")

    layout = QGridLayout()

    title = QLabel("Title:")
    layout.addWidget(title, 0,0)

    titlebx = QLineEdit()
    layout.addWidget(titlebx, 0,1)

    msg = QLabel("Note Text:")
    layout.addWidget(msg, 1,0)

    msgbox = QTextEdit()
    msgbox.setMaximumSize(200,300)
    layout.addWidget(msgbox, 2,0, 1,2)

    accptbtn = QPushButton("Add")
    accptbtn.clicked.connect(partial(noteaddquery, titlebx, msgbox, pid, notewindow))
    cnclbtn = QPushButton("Cancel")
    cnclbtn.clicked.connect(notewindow.reject)

    layout.addWidget(accptbtn, 3,0)
    layout.addWidget(cnclbtn, 3,1)

    notewindow.setLayout(layout)

    notewindow.show()
    notewindow.exec_()


# Note Add query
# I tried to be sneaky above
# but my attempt failed and I do not have time
# at the moment to test possible solutions better
# than this. I will later as I expand on this program
def noteaddquery(title, msg, pid, q):
    anotherwindow = QDialog()
    anotherwindow.setWindowTitle("Query Result")

    layout = QVBoxLayout()

    l1 = QLabel()

    try:
        db = SqlConnect()
        db.connect()

        db.add_note(title.text(), msg.toPlainText(), pid)

        db.close()

        l1.setText("Success")
    except sqlite3.Error as e:
        l1.setText("Failure: " + str(e))

    layout.addWidget(l1)

    okbtn = QPushButton("Ok")
    okbtn.clicked.connect(anotherwindow.accept)
    layout.addWidget(okbtn)

    anotherwindow.setLayout(layout)

    anotherwindow.show()
    anotherwindow.exec_()

    # Close note window
    return q.accept()


# Main
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Address Book")
        self.setMinimumHeight(150)
        self.setMinimumWidth(100)

        # Set layout
        self.layout = QVBoxLayout()

        # Stats
        self.db = SqlConnect()
        self.db.connect()
        self.db.create()

        self.personstats = QLabel()
        self.notestats = QLabel()

        self.update_counts()

        self.layout.addWidget(self.personstats)
        self.layout.addWidget(self.notestats)

        # Primary buttons
        self.addperson = QPushButton("Add New Person")
        self.addperson.clicked.connect(self.add_person)
        self.searchperson = QPushButton("Search Person")
        self.searchperson.clicked.connect(self.search_person)
        self.closebutton = QPushButton("Quit")
        self.closebutton.clicked.connect(self.close)

        # Add buttons to layout
        self.layout.addWidget(self.addperson)
        self.layout.addWidget(self.searchperson)
        self.layout.addWidget(self.closebutton)

        # Add layout to window
        self.setLayout(self.layout)

    def update_counts(self):
        self.personstats.setText("Total Persons: " + self.db.count_persons())
        self.notestats.setText("Total Notes: " + self.db.count_notes())

    # Add person function
    def add_person(self):
        d = AddPersonWindow()
        d.exec_()

        self.update_counts()

    # Search Person function
    def search_person(self):
        d = SearchPersonWindow()
        d.exec_()


# main function for run
def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()


# Execute Program
main()
