from pyspark.sql import SparkSession
import os

# Crear una sesión de Spark
spark = SparkSession.builder.appName('Guardar en AVRO').getOrCreate()

# Crear un DataFrame de ejemplo
data = [('Juan', 25), ('María', 30), ('Pedro', 35)]
df = spark.createDataFrame(data, ['nombre', 'edad'])

# Escribir el DataFrame en formato AVRO
df.write.format('com.databricks.spark.avro').save('C:/Users/moren/OneDrive - Pontificia Universidad Javeriana/Documents/Data_migration_repo/Data_migration/Backup')

# Verificar si el archivo de respaldo fue creado
if len(os.listdir('C:/Users/moren/OneDrive - Pontificia Universidad Javeriana/Documents/Data_migration_repo/Data_migration/Backup')) > 0:
    print('El archivo de respaldo en formato AVRO fue creado con éxito.')
else:
    print('No se pudo crear el archivo de respaldo.')

