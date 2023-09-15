from pyspark.sql import SparkSession

# Configure the MariaDB JDBC connection
jdbc_hostname = "localhost"
jdbc_port = 3306
jdbc_database = "star_classification"
jdbc_username = "nasa"
jdbc_password = "verystrongpassword123*"

jdbc_url = f"jdbc:mysql://{jdbc_hostname}:{jdbc_port}/{jdbc_database}"

# Create a Spark session
spark = SparkSession.builder.appName("CSV to MariaDB").config("spark.jars", "/app/mysql-connector-java-8.0.13.jar").getOrCreate()

# Read CSV data
csv_data = spark.read.option("header", "true").csv("/app/star_classification.csv")

connection_properties = {
    "user": jdbc_username,
    "password": jdbc_password,
}

# Write the data to MariaDB
csv_data.write.mode("overwrite").option("url", jdbc_url).jdbc(jdbc_url, "target_table_name", properties=connection_properties)

# Stop the Spark session
spark.stop()
