from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

# Create a Spark session
spark = SparkSession.builder \
    .appName("CSV to MariaDB") \
     .config("spark.jars", "/app/mysql-connector-j-8.1.0.jar") \
     .getOrCreate()

# Read CSV data
csv_data = spark.read.option("header", "true").csv("/app/star_classification.csv")

# Configure the MariaDB JDBC connection
jdbc_hostname = "mysql"
jdbc_port = 3306
jdbc_database = "star_classification"
jdbc_username = "nasa"
jdbc_password = "verystrongpassword123*"

jdbc_url = f"jdbc:mysql://{jdbc_hostname}:{jdbc_port}/{jdbc_database}"

connection_properties = {
        "user": jdbc_username,
         "password": jdbc_password,
}

# Lire les données depuis la base de données MariaDB
db_data = spark.read.jdbc(url=jdbc_url, table="target_table_name", properties=connection_properties)

# Afficher les données récupérées
db_data.show()

# Obtenir le décompte de chaque classe
class_counts = db_data.groupBy("class").count().orderBy("class")

class_names = class_counts.select("class").rdd.flatMap(lambda x: x).collect()
class_values = class_counts.select("count").rdd.flatMap(lambda x: x).collect()

colors = ["blue", "green", "red"]


plt.figure(figsize=(10, 6))
plt.bar(class_names, class_values, color=colors)
plt.xlabel("Classes")
plt.ylabel("Nombre d'occurrences")
plt.title("Répartition des classes")
plt.xticks(rotation=45)
plt.savefig("/app/class_distribution.png")


total_samples = db_data.count()
class_proportions = [(count / total_samples) for count in class_values]

plt.figure(figsize=(8, 8))
plt.pie(class_proportions, labels=class_names, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title("Proportion des classes")
plt.savefig("/app/class_proportion.png")
plt.show()

# Arrêtez la session Spark
spark.stop()
