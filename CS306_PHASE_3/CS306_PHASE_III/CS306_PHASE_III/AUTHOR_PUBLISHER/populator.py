import mysql.connector
from faker import Faker
import random
from connect import create_connection

# Connect to your MySQL server
connection = create_connection()

# Create a cursor object
cursor = connection.cursor()

# Create a Faker instance
fake = Faker()

# Number of records to generate
num_records = 1000000

# Create tables
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS PUBLISHER(
        pub_name VARCHAR(255),
        pub_id INT DEFAULT NULL AUTO_INCREMENT,
        PRIMARY KEY(pub_id)
);
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS AUTHOR(
        au_id INT DEFAULT NULL AUTO_INCREMENT,
        pub_id INT DEFAULT NULL,
        au_firstname VARCHAR(255),
        au_lastname VARCHAR(255),
        au_nation VARCHAR(50),
        PRIMARY KEY(au_id),
        FOREIGN KEY(pub_id) REFERENCES PUBLISHER(pub_id) ON DELETE CASCADE
    );
    """
)

pub_id_counter = 1
# Generate and insert data for PUBLISHER table
for _ in range(num_records):
    pub_name = fake.company()
    # Assign the current counter value as pub_id
    pub_id = pub_id_counter

    cursor.execute(
        """
        INSERT INTO PUBLISHER (pub_id, pub_name)
        VALUES (%s, %s)
        """,
        (pub_id, pub_name),
    )

    # Increment the counter for the next pub_id
    pub_id_counter += 1
    print("Data added to PUBLISHER table")

print('PUBLISHER table data addition is done.')

# Generate and insert data for AUTHOR table
cursor.execute("SELECT pub_id FROM PUBLISHER")
publisher_ids = cursor.fetchall()

for _ in range(num_records):
    au_firstname = fake.first_name()
    au_lastname = fake.last_name()
    au_nation = fake.country()
    pub_id = random.choice(publisher_ids)[0]

    cursor.execute(
        """
        INSERT INTO AUTHOR (pub_id, au_firstname, au_lastname, au_nation)
        VALUES (%s, %s, %s, %s)
        """,
        (pub_id, au_firstname, au_lastname, au_nation),
    )
    print("Data added to AUTHOR table")

print('AUTHOR table data addition is done.')

# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
