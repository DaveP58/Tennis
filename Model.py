#imports 

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError
import sqlite3
import csv



#create database
engine = create_engine('sqlite:///Tennis.db', echo=False)
#Base class for models
Base = declarative_base()
#Session class for database operations
Session = sessionmaker(bind=engine)
session = Session()




#define models (tables  members, payments, events, teams )
class Member(Base):
    __tablename__ = 'members'
    recID = Column(Integer, primary_key=True,nullable=False)
    fname = Column(String(20), nullable=False)
    lname = Column(String(20), nullable=False)
    email = Column(String(50), nullable=False,default="not given")
    phone = Column(String(15), nullable=True)
    USTALevel = Column(String(10), nullable=True)
    TTExperience = Column(String(25), nullable=True)
    playsTennis = Column(String, default="False")
    playsTT = Column(String, default="False")
    playsPT = Column(String, default="False")
    playsRB = Column(String, default="False")
    duesPaid = Column(String, default="False")
    ballPaid = Column(String, default="False")
    ballCertified = Column(String, default="False")
    MemberSince = Column(String(25), nullable=False, default="2023-10-01")
    notes = Column(String, nullable=True, default="No notes")
    payments = relationship("Payment", back_populates="member")
    
    # teams = relationship("Team", back_populates="member", cascade="all, delete-orphan")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True,unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    date = Column(String(25), nullable=False, default="2023-10-01")
    location = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    
    payments = relationship("Payment",back_populates="events", cascade="all")
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    eventid = Column(Integer, ForeignKey('events.id'), nullable=True)
    events = relationship("Event", back_populates="payments")
    purpose = Column(String(50), nullable= True)  # e.g., "dues", "meeting", "tournament"
    payment_type = Column(String(50), nullable=False)  # e.g., "dues", "ball", "event"
    amount = Column(String, nullable=False)
    date = Column(String(25), nullable=False, default="2023-10-01")
    memberid = Column(Integer, ForeignKey('members.recID'))
    member = relationship("Member", back_populates="payments")



Base.metadata.create_all(engine)  # Create tables in the database


#Utility Functions
def findMember(recID):
    """Retrieve a member by their ID."""
    return session.query(Member).filter(Member.recID == recID).first()
   

def findEvent(eventID): 
    """Retrieve an event by its ID."""
    return session.query(Event).filter(Event.id == eventID).first()
#add queries as needed 

#confirn actions ***** needs some thinking 
def confirmAction(action, member):
    """Confirm an action with the user."""
    print(f"Are you sure you want to {action} for {member.fname} {member.lname}? (yes/no)")
    response = input().strip().lower()
    return response == 'yes'

def getmember(recID): 
    data =session.query(Member).filter(Member.recID == recID).first() 
    print (data.fname, data.lname, data.email, data.phone, data.USTALevel, data.TTExperience, data.playsTennis, data.playsTT, data.playsPT, data.playsRB, data.duesPaid, data.ballPaid, data.ballCertified, data.MemberSince, data.notes)
    return data 
    


#CRUD OPs 
def addMember():
    recID =input("Enter first recID: ")
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    USTALevel = input("Enter USTA Level (if applicable): ")
    TTExperience = input("Enter Table Tennis Experience (if applicable): ") 
    MemberSince = input("Enter Member Since (default is 2023-10-01): ") or "2023-10-01"
    if findMember(recID):
        print(f"Member with recID {recID} already exists.")
        return
    try: 
        session.add(Member(recID=recID, fname=fname, lname=lname, email=email,
                        phone=phone, USTALevel=USTALevel, TTExperience=TTExperience,
                        MemberSince=MemberSince))   
        session.commit()
        print(f"Member {fname} {lname} added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Member with this recID or email already exists.")
    
    
    # 

def addEvent():
    
    """Add a new event to the database."""
    # Get member ID to associate the event with
    # recID = input("Enter member recID to associate with the event: ")
    # member = findMember(recID)
    # if not member:
    #     print(f"No member found with recID {recID}. Please add the member first.")
    #     return
    name = input("Enter event name: ")
    date = input("Enter event date (YYYY-MM-DD): ")
    session.add(Event(name=name, date=date, location="Tennis Club", description="Monthly Tennis Event", ))
    session.commit()
    print(f"Event '{name}' added successfully ")
    
def addPayment():
    """Add a payment for a member."""
    
    memberid = input("Enter member recID to associate with the payment: ")
    eventsid = input("Enter event ID to associate with the payment: ")
    member = findMember(memberid)
    if not member:
        print(f"No member found with recID {memberid}. Please add the member first.")
        return
    event = findEvent(eventsid)
    if not event:
        print(f"No event found with ID {eventsid}. Please add the event first.")
        return
    payment_type = input("Enter payment type (cash, check, paypal): ")
    purpose = input("Enter payment reason (dues, meeting, tournment): ")
    amount = (input("Enter payment amount: "))
    date = input("Enter payment date (YYYY-MM-DD): ")
    session.add(Payment( payment_type=payment_type, amount=amount, date=date,purpose=purpose, memberid= memberid, eventid = eventsid))
    session.commit()
    print(f"Payment of {amount} for {payment_type} added successfully ")
 
 
def loadDatabaseFromCSV():
    """Load database from CSV files."""
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("Tennis.db")
    cursor = connection.cursor()

    # Open the CSV file and insert data
    with open("MemberData.csv", "r") as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip the header row
        cursor.executemany("INSERT INTO members (lname, fname, phone, email,recID,USTALevel,TTExperience,playsTennis,playsTT,playsPT,playsRB,duesPaid,ballPaid,ballCertified,MemberSince,Notes) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?)", reader)

    # Commit changes and close the connection
    connection.commit()
    connection.close() 


# connection.close()

    
def main():
    """Main function to run the application."""
    while True:
        print("\nTennis Club Management System")
        print("1. Add Member")
        print("2. Add Event")
        print("3. Add Payment")
        print("4. Exit")
        print( "99 Load Database from CSV")
        
        choice = input("Enter your choice: ")
        
        
        if choice == '1':
            addMember()
        elif choice == '2':
            addEvent()
        elif choice == '3':
            addPayment()
        elif choice == '99':
            loadDatabaseFromCSV()
        elif choice == '4':
            getmember(133116)
            print("Exiting the application.")
           
        else:
            print("Invalid choice. Please try again.")
if(__name__ == "__main__"):
    main()
#Main ops
