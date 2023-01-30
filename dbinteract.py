import sqlite3

conn = sqlite3.connect('deadlines.db')

cur = conn.cursor()


def create_deadlines_table():
    create_script = """
    CREATE TABLE IF NOT EXISTS deadlines (
        guild_id    INT,
        name        TEXT,
        deadline    INT
    )
    """
    cur.execute(create_script)
    conn.commit()


def insert_deadline(guild_id, name, deadline):
    insert_script = "INSERT INTO deadlines (guild_id, name, deadline) VALUES (?, ?, ?)"

    cur.execute(insert_script, (guild_id, name, deadline))
    conn.commit()
    return True

def read_deadline(guild_id):
    """
    takes in guild_id, returns a list of tuples where tuple[0] is name and tuple[1] is the deadline
    """
    
    fetch_script = f"SELECT name, deadline FROM deadlines WHERE guild_id={guild_id}"

    cur.execute(fetch_script)
    ans = cur.fetchall()
    return ans


def delete_all_data():
    """
    !!!!
    clears all data from a table
    """
    fetch_script = "DELETE FROM deadlines"
    cur.execute(fetch_script)

# if __name__ == "__main__":
#     create_deadlines_table()
#     insert_deadline(123, "yo", "t1")
#     insert_deadline(123, "y2", "t2")
#     insert_deadline(124, "y2", "t2")
#     print(read_deadline(123))
#     delete_all_data()
#     print(read_deadline(123))
#     insert_deadline(123, "yo", "t1")
#     insert_deadline(123, "y2", "t2")
#     insert_deadline(124, "y2", "t2")
#     print(read_deadline(123))
#     delete_all_data()
#     print(read_deadline(123))

create_deadlines_table()
