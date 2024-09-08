import mysql.connector

class AirportModel:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except mysql.connector.Error as err:
            print(f"Ошибка при подключении к базе данных: {err}")
            return False

    def get_airports(self, min_lat, max_lat, min_lon, max_lon):
        if not self.connection:
            return []  # База данных не подключена

        cursor = self.connection.cursor()
        query = ("SELECT city, country, latitude, longitude FROM airports "
                 "WHERE latitude BETWEEN %s AND %s AND longitude BETWEEN %s AND %s")
        cursor.execute(query, (min_lat, max_lat, min_lon, max_lon))
        airports = cursor.fetchall()
        cursor.close()
        return airports

    def close_connection(self):
        if self.connection:
            self.connection.close()