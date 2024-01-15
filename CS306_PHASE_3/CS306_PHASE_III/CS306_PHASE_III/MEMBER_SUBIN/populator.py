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

# Create a table
cursor.execute(
    """
        CREATE TABLE IF NOT EXISTS MEMBER(
            MEM_ID INT PRIMARY KEY AUTO_INCREMENT,
            MEM_FIRSTNAME VARCHAR(50),
            MEM_LASTNAME VARCHAR(50),
            MEM_ADDRESS VARCHAR(255),
            MEM_DATE INT
        );
    """
)

cursor.execute(

    """
        CREATE TABLE IF NOT EXISTS SUBIN_SUBSCRIPTION(
            sub_id INT PRIMARY KEY AUTO_INCREMENT,
            FROM_YEAR INT,
            SUB_PRICE DECIMAL(10, 2),
            SUB_TYPE VARCHAR(50),
            MEM_ID INT,
            FOREIGN KEY (MEM_ID) REFERENCES MEMBER (MEM_ID) ON DELETE CASCADE
        );
    """
)

# Generate and insert data
for _ in range(num_records):
    MEM_FIRSTNAME = fake.first_name()
    MEM_LASTNAME = fake.last_name()
    MEM_ADDRESS = fake.email()
    MEM_DATE = random.randint(2000, 2023)

    cursor.execute(
        """
        INSERT INTO MEMBER (MEM_FIRSTNAME, MEM_LASTNAME, MEM_ADDRESS, MEM_DATE)
        VALUES (%s, %s, %s, %s)
        """,
        (MEM_FIRSTNAME, MEM_LASTNAME, MEM_ADDRESS, MEM_DATE),
    )
    print("data added to MEMBER table")

print('MEMBER table data addition is done.')

cursor.execute("SELECT MEM_ID FROM CS306.MEMBER")
member_ids = cursor.fetchall()


for _ in range(num_records):
    from_year = random.randint(2000, 2023)
    sub_price = random.uniform(10.0, 500.0)
    sub_type = random.choice(['Basic', 'Premium', 'VIP'])
    mem_id = random.choice(member_ids)[0]  # MEMBER tablosundaki gerçek MEM_ID değerlerinden birini kullan
    cursor.execute("INSERT INTO CS306.SUBIN_SUBSCRIPTION (FROM_YEAR, SUB_PRICE, SUB_TYPE, MEM_ID) VALUES (%s, %s, %s, %s)",
                   (from_year, sub_price, sub_type, mem_id))

    print("data added to SUBIN_SUBSCRIPTION table")


print('SUBIN_SUBSCRIPTION table data addition is done.')


# Commit the changes
connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
