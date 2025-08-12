import datetime
import time
import oci
import json
from datetime import timedelta
import argparse
import random
from zabbix_utils import ItemValue, Sender

# Configurando o argparse para receber os argumentos de linha de comando
parser = argparse.ArgumentParser(description="Informe o nome do compartment e o namespace.")
parser.add_argument("compartment", type=str, help="Digite o compartment OCID")
parser.add_argument("namespace", type=str, help="Digite o namespace do bucket")
parser.add_argument("--debug", action="store_true", help="Ativa modo de debug")
args = parser.parse_args()

# Atribuindo os valores dos argumentos às variáveis
oci_compartment = args.compartment
oci_namespace = args.namespace
debug_mode = args.debug

# Funções do sistema
def consultar_bucket(bucket_name):
    try:
        get_bucket_response = object_storage_client.get_bucket(namespace_name=namespace_name, bucket_name=bucket_name)
        bucket_id = get_bucket_response.data.id
        query_txt = f'StoredBytes[5m]{{resourceID = "{bucket_id}"}}.max()'

        if debug_mode:
            print(f"🔍 Consultando métricas para bucket: {bucket_name}")
            print(f"📊 Query: {query_txt}")

        summarize_metrics_data_response = monitoring_client.summarize_metrics_data(
            compartment_id=compartment_id,
            summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
                namespace="oci_objectstorage",
                query=query_txt,
                start_time=formatted_time_moh,
                end_time=formatted_time_now
            ),
            compartment_id_in_subtree=False
        )

        if not summarize_metrics_data_response.data:
            return 0
        else:
            points = summarize_metrics_data_response.data[0].aggregated_datapoints
            valores = [p.value for p in points]
            return valores[-1] if valores else 0

    except oci.exceptions.ServiceError as e:
        if e.status == 429:
            wait_time = random.uniform(1.0, 3.0)
            print(f"🔁 Limite de requisições atingido. Aguardando {wait_time:.2f}s antes de tentar novamente para o bucket '{bucket_name}'...")
            time.sleep(wait_time)
            return consultar_bucket(bucket_name)
        else:
            print(f"❌ Erro ao consultar bucket '{bucket_name}': {str(e)}")
            return 0

# Timestamp atual
timestamp = time.time()
dt_object = datetime.datetime.fromtimestamp(timestamp)
formatted_time_now = dt_object.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
dt_object_minus_one_hour = dt_object - timedelta(hours=1)
formatted_time_moh = dt_object_minus_one_hour.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Inicializando clientes OCI
config = oci.config.from_file()
object_storage_client = oci.object_storage.ObjectStorageClient(config)
monitoring_client = oci.monitoring.MonitoringClient(config)

namespace_name = oci_namespace
compartment_id = oci_compartment

# Listando buckets
list_buckets_response = object_storage_client.list_buckets(
    namespace_name=namespace_name,
    compartment_id=compartment_id,
    limit=300
)

balde = [bucket.name for bucket in list_buckets_response.data]

if debug_mode:
    print(f"📁 Buckets encontrados: {balde}")

# Consultando métricas
dados_zabbix = []
for dtBalde in balde:
    tamanho = consultar_bucket(dtBalde)
    dados_zabbix.append({
        "bucket_name": dtBalde,
        "bucket_size": tamanho
    })

# Gerando payload
payload_json = {"data": dados_zabbix}

if debug_mode:
    print("📦 Payload JSON gerado:")
    print(json.dumps(payload_json, indent=2))

# Enviando para Zabbix
items = [
    ItemValue('teste_sender_oci', 'grafana_payload', payload_json)
]

if debug_mode:
    print("📝 Itens para envio ao Zabbix:")
    for item in items:
        print(f"🔑 Key: {item.key}, 📊 Value: {item.value}")

try:
    sender = Sender('sa-sp1-be-pool-1.monitoracao.sasp1.oci.i.globo', 10003)
    response = sender.send(items)
    print("✅ Envio realizado com sucesso.")
    if debug_mode:
        print("📨 Resposta do Zabbix Sender:")
        print(response)
except Exception as e:
    print("❌ Falha no envio para o Zabbix:")
    print(str(e))

print(f"📊 Payload gerado com {len(dados_zabbix)} entradas.")

