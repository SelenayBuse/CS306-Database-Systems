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


cursor.execute(
                """CREATE TABLE IF NOT EXISTS BOOK (
                         ISBN INT PRIMARY KEY AUTO_INCREMENT,
                         TITLE VARCHAR(255),
                         NUM_COPIES INT,
                         PUB_YEAR INT
                );"""
)

cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS CHECKOUT_BOOK (
                        CHECKOUT_ID INT PRIMARY KEY AUTO_INCREMENT,
                        ISBN INT,
                        CHECKOUT_DATE DATE NOT NULL,
                        RETURN_DATE DATE,
                        DUE_DATE DATE NOT NULL
                );
                """
)


# Generate and insert data
for _ in range(num_records):
    TITLE = fake.name()
    NUM_COPIES = random.randint(1, 30)
    MEM_ADDRESS = fake.email()
    PUB_YEAR = random.randint(1880, 2023)

    cursor.execute(
        """
        INSERT INTO BOOK (TITLE, NUM_COPIES, PUB_YEAR)
        VALUES (%s, %s, %s)
        """,
        (TITLE, NUM_COPIES, PUB_YEAR),
    )
    print("data added to BOOK table")

print('BOOK table data addition is done.')

cursor.execute("SELECT ISBN FROM CS306.BOOK")
book_ids = cursor.fetchall()


for _ in range(num_records):
    ISBN = random.choice(book_ids)[0]
    CHECKOUT_DATE = fake.date()
    RETURN_DATE = fake.date()
    DUE_DATE = fake.date()
    cursor.execute("INSERT INTO CS306.CHECKOUT_BOOK (ISBN, CHECKOUT_DATE, RETURN_DATE, DUE_DATE) VALUES (%s, %s, %s, %s)",
                   (ISBN, CHECKOUT_DATE, RETURN_DATE, DUE_DATE))

    print("data added to CHECKOUT_BOOK table")


print('CHECKOUT_BOOK table data addition is done.')


# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
