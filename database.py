import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="$$",
    database="client"
)

cursor = connection.cursor()


def website_exists(website):
    """
    Returns True if the website already exists in the database.
    """

    query = """
    SELECT id
    FROM companies
    WHERE website = %s
    """

    cursor.execute(query, (website,))

    return cursor.fetchone() is not None


def save_company(website, score, selected):
    """
    Saves a processed company into the database.
    """

    status = "SELECTED" if selected else "PROCESSED"

    query = """
    INSERT INTO companies
    (website, status, score)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            website,
            status,
            score
        )
    )

    connection.commit()


def get_selected_companies():
    """
    Returns every selected company.
    """

    query = """
    SELECT *
    FROM companies
    WHERE status = 'SELECTED'
    """

    cursor.execute(query)

    return cursor.fetchall()


def get_all_companies():
    """
    Returns all processed companies.
    """

    cursor.execute(
        "SELECT * FROM companies"
    )

    return cursor.fetchall()


def close_connection():
    """
    Closes the MySQL connection.
    """

    cursor.close()
    connection.close()