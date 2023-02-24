import sqlite3
from datetime import datetime

conn = sqlite3.connect('deadlines.db')

cur = conn.cursor()


def create_deadlines_table() -> None:
    """
    Creates a `deadlines` table.
    """
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
    """
    Inserts deadlines to `deadlines` table
    """
    deadline = datetime.fromisoformat(deadline).timestamp()
    curr_timezone = fetch_timezone(guild_id)
    deadline += curr_timezone[0]*60

    check_script = f"SELECT COUNT(*) FROM deadlines WHERE guild_id={guild_id} AND name ='{name}'"
    cur.execute(check_script)
    ans = cur.fetchall()

    if ans[0][0] != 0:
        return False

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

    curr_timezone = fetch_timezone(guild_id)

    for i in ans:
        deadline_local = datetime.fromtimestamp( \
            (i[1] - (curr_timezone[0]*60))).isoformat(" " ,"seconds")
        i = list(i)
        i[1] = deadline_local
        i = tuple(i)

    return ans


def delete_all_data():
    """
    !!!!
    clears all data from a table
    """
    fetch_script = "DELETE FROM deadlines"
    cur.execute(fetch_script)


def delete_deadline(guild_id):
    """
    deletes deadlines corresponding to guild_id
    """
    fetch_script = f"DELETE FROM deadlines where guild_id = {guild_id}"
    cur.execute(fetch_script)
    conn.commit()


def fetch_timezone(guild_id):
    """
    fetches the timezoen diff (in minutes) for the provided guild_id
    """
    timezone_script = f"SELECT timezone FROM timezone WHERE guild_id={guild_id}"
    cur.execute(timezone_script)
    timezone_minutes = cur.fetchall()

    #timezone_minutes is a list , if guild id doesnt exist we take 5h30mins as default
    if len(timezone_minutes) == 0:
        timezone_minutes = [330]

    return timezone_minutes


def create_timezonediff_table():
    """
    creates a timezone table which contains timezone difference
    """
    create_script = """
    CREATE TABLE IF NOT EXISTS timezone (
        guild_id    INT,
        timezone    INT
    )
    """
    cur.execute(create_script)
    conn.commit()


def sort_deadlines(ans):
    #sort deadlines using selection sort
    for i in range(len(ans)):
        for j in range(i+1, len(ans)):
            if ans[j][1] < ans[i][1]:
                ans[i], ans[j] = ans[j], ans[i]
    return ans


#if __name__ == "__main__":
#     create_deadlines_table()
#     insert_deadline(123, "yo", "t1")
#     insert_deadline(123, "y2", "t2")
#     insert_deadline(124, "y2", "t2")
#     print(read_deadline(123))
#     delete_deadline(123)
#     print(read_deadline(123))
#     print(read_deadline(124))
#     insert_deadline(123, "yo", "t1")
#     insert_deadline(123, "y2", "t2")
#     insert_deadline(124, "y2", "t2")
#     print(read_deadline(123))
#     delete_deadline(123)
#     print(read_deadline(123))
#     print(read_deadline(124))
#     delete_deadline(124)

create_deadlines_table()
create_timezonediff_table()
