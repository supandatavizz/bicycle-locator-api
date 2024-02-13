import dask.dataframe as dd
import mysql.connector

def load_parquet_to_mysql(parquet_file_path, mysql_host, mysql_user, mysql_password, mysql_database):
    df = dd.read_parquet(parquet_file_path)
    pandas_df = df.compute()
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = conn.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS bicycle_location (
        id INT AUTO_INCREMENT PRIMARY KEY,
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        bicycle_id VARCHAR(36)
    )
    """
    cursor.execute(create_table_query)

    insert_query = "INSERT INTO bicycle_location (latitude, longitude, bicycle_id) VALUES (%s, %s, %s)"
    values = [tuple(row) for row in pandas_df[['Latitude', 'Longitude', 'BicycleID']].values.tolist()]
    cursor.executemany(insert_query, values)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    parquet_file_path = "bicycle_data.parquet"
    mysql_host = "localhost"
    port="3306"
    mysql_user = "root"
    mysql_password = "my-secret-pw"
    mysql_database = "bicycle_data"

    load_parquet_to_mysql(parquet_file_path, mysql_host, mysql_user, mysql_password, mysql_database)
