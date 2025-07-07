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

# Exibindo os valores
#print(f"\nCompartment: {args.compartment}")
#print(f"Namespace: {args.namespace}")

# Atribuindo os valores dos argumentos às variáveis
oci_compartment = args.compartment
oci_namespace = args.namespace

# Timestamp atual
timestamp = time.time()

# Convertendo timestamp para datetime
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("\n")
#print(f"Objeto datetime: {dt_object}")
#print("\n --------\n")

# Formatando o datetime
formatted_time_now = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
#print(f"Agora.....: {formatted_time_now}")
# Calculando o tempo subtraindo uma hora
dt_object_minus_one_hour = dt_object - timedelta(hours=1)
# Formatando o datetime após a subtração
formatted_time_moh = dt_object_minus_one_hour.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
#print(f"Menos 1h..: {formatted_time_moh}")
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
#criando uma lista para armazenar os nomes dos buckets
balde = []
# Adicionando os nomes dos buckets à lista
for bucket in list_buckets_response.data:
    balde.append(bucket.name)

for dtBalde in balde:
    get_bucket_response = object_storage_client.get_bucket(namespace_name=namespace_name, bucket_name=dtBalde)
 #   print(f"Bucket Name..: {get_bucket_response.data.name} \nBucket id....: {get_bucket_response.data.id} \nStorage Tier.: {get_bucket_response.data.storage_tier}")
    
    bucket_id = get_bucket_response.data.id
    query_txt = f"StoredBytes[5m]{{resourceID = \"{bucket_id}\"}}.sum()"
    
    # Prepare the query text
 #   print(f"Query Text..: {query_txt}")


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

    # Get the data from response
    #print(summarize_metrics_data_response.data)
    if not summarize_metrics_data_response.data:
        #print("\n --------\n")
        print(f"Bucket...: {dtBalde}: [0] bytes")
        #print("\n --------\n")
        continue
    points = summarize_metrics_data_response.data[0].aggregated_datapoints
    
    valores = [p.value for p in points]
    
    print(f"Bucket...: {dtBalde}: {valores} bytes")
    #print(summarize_metrics_data_response.data[0].aggregated_datapoints)

    # Sleep to avoid hitting API rate limits
    time.sleep(1)
