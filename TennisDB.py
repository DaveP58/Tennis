import sqlite3 
from icecream import ic as cprint



# def get_connection(db_name):
#     """Establish a connection to the SQLite database."""
#     try:
#         return sqlite3.connect(db_name)
#     except  Exception as e:
#         cprint(f"Error connecting to database: {e}")
#         raise

# connection = sqlite3.connect('Tennis.db')
# cursor = connection.cursor()


# cursor.execute(''' SELECT * FROM members WHERE fname='Dave' ''')
# Dave = cursor.fetchall()
# cursor.close()
# connection.close()

def findMember(recID):
    """Find a member by recID ."""
    connection = sqlite3.connect('Tennis.db')
    cursor = connection.cursor()
    try:
        cursor.execute(''' SELECT * FROM members WHERE recID=? ''', (recID,))
        member = cursor.fetchall()
        return member
        cprint (f"Member found: {member}")   
    except Exception as e:
        cprint(f"Error finding member: {e}")
        return None
    finally:
        cursor.close()
        connection.close()
        
def updateMember(recID, fname, lname, email):
    """Update a member's details."""
    connection = sqlite3.connect('Tennis.db')
    cursor = connection.cursor()
    try:
        cursor.execute(''' UPDATE members SET fname=?, lname=?, email=? WHERE recID=? ''', (fname, lname, email, recID))
        connection.commit()
        cprint(f"Member with recID {recID} updated successfully.")
    except Exception as e:
        cprint(f"Error updating member: {e}")
    finally:
        cursor.close()
        connection.close()

