#importações
import datetime
import time
import oci
import json
from datetime import timedelta
import argparse


parser = argparse.ArgumentParser(description="Informe o nome do compartment e o namespace.")
parser.add_argument("compartment", type=str, help="Digite o compartment OCID")
parser.add_argument("namespace", type=str, help="Digite o namespace do bucket")


args = parser.parse_args()

# Atribuindo os valores dos argumentos às variáveis
oci_compartment = args.compartment
oci_namespace = args.namespace

# Array para armazenar os dados do Zabbix
dados_zabbix = []
tamanho = 0
# Timestamp atual
timestamp = time.time()

# Convertendo timestamp para datetime
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("\n")

# Formatando o datetime
formatted_time_now = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
# Calculando o tempo subtraindo uma hora
dt_object_minus_one_hour = dt_object - timedelta(hours=1)
# Formatando o datetime após a subtração
formatted_time_moh = dt_object_minus_one_hour.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Initialize service client with default config file
config = oci.config.from_file()
object_storage_client = oci.object_storage.ObjectStorageClient(config)
monitoring_client = oci.monitoring.MonitoringClient(config)

# Definindo o namespace e o compartment
namespace_name = oci_namespace
compartment_id = oci_compartment

# Listando os buckets no namespace e compartment especificados
list_buckets_response = object_storage_client.list_buckets(
    namespace_name=namespace_name,
    compartment_id=compartment_id,
    limit=300
)

# Criando o arquivo de payload para o Zabbix
with open("zabbix_oci_payload.json", "w") as f:
    f.write("{\n")
    f.write('"data": [\n')


#criando uma lista para armazenar os nomes dos buckets
balde = []
# Adicionando os nomes dos buckets à lista
for bucket in list_buckets_response.data:
    balde.append(bucket.name)

for dtBalde in balde:
    get_bucket_response = object_storage_client.get_bucket(namespace_name=namespace_name, bucket_name=dtBalde)
    bucket_id = get_bucket_response.data.id
    query_txt = f"StoredBytes[5m]{{resourceID = \"{bucket_id}\"}}.max()"
   
    # Send the request to service, some parameters are not required, see API
    # doc for more info
    summarize_metrics_data_response = monitoring_client.summarize_metrics_data(
        compartment_id=compartment_id,
        summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
            namespace="oci_objectstorage",
            query=query_txt,
            start_time=formatted_time_moh,
            end_time=formatted_time_now),
        compartment_id_in_subtree=False)
    time.sleep(1)  # Sleep to avoid hitting API rate limits
    # Get the data from response
    #print(summarize_metrics_data_response.data)
    if not summarize_metrics_data_response.data:
        tamanho = 0
    else:
        points = summarize_metrics_data_response.data[0].aggregated_datapoints
        valores = [p.value for p in points]
        tamanho = valores[-1] if valores else 0
        # Adicionando os dados do bucket ao array para o Zabbix
        dados_zabbix.append({
            "bucket_name": f"{dtBalde}",
            "bucket_size": tamanho
        })
        
    

# Salvar em arquivo JSON para envio posterior
with open("zabbix_oci_payload.json", "a") as f:
    for item in dados_zabbix:
        f.write(json.dumps(item) + ",\n")
    f.write("]\n")
    f.write("}")
    
print(f"Arquivo gerado com {len(dados_zabbix)} entradas.")