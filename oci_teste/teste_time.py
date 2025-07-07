import datetime
import time
from datetime import timedelta
# Timestamp atual
timestamp = time.time()

# Convertendo timestamp para datetime
dt_object = datetime.datetime.fromtimestamp(timestamp)
print(f"Objeto datetime: {dt_object}")

# Formatando o datetime
formatted_time = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
print(f"Tempo formatado: {formatted_time}")

print("\n --------\n")
dt_object_minus_one_hour = dt_object - timedelta(hours=1)





# Obtendo informações sobre o tempo do sistema
#local_time = time.localtime(timestamp)
#print(f"Informações locais: {local_time}")



# Converter de volta para timestamp (opcional)
new_timestamp = dt_object_minus_one_hour.timestamp()

print(f"Timestamp original........: {timestamp}")
print(f"Novo timestamp (opcional).: {new_timestamp}")
print("\n --------\n")
print(f"Objeto datetime original........: {dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}")
print(f"Objeto datetime após subtração..: {dt_object_minus_one_hour.strftime("%Y-%m-%dT%H:%M:%S.%fZ")}")
print("\n --------\n")
