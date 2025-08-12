# ##############################################################################################################################
# Coleta de Tamanho de Buckets do OCI Object Storage para Zabbix
# Versão 2.0
# Autor: Samir Lins Nagib (samir@g.globo)
# Data: 08/07/2025  
# Alterações: 22/07/2025
# - Adicionada lógica para lidar com limites de requisições (HTTP 429)
# - Implementada lógica de retry com espera aleatória
# - Melhorias na formatação do JSON de saída   
# - Adicionado tratamento de erros para exceções de serviço
#
# Alterações: 11/08/2025
# Inclusão da biblioteca zabbix_utils para integraçao com o zabbix
#
# Descrição: Este script coleta o tamanho dos buckets do OCI Object Storage e gera um arquivo JSON para envio ao Zabbix.
# Requisitos: Biblioteca OCI Python SDK, Zabbix configurado para receber dados via JSON
# Uso: Execute o script passando o OCID do compartment e o namespace do bucket como argumentos de linha de comando.
# Exemplo: python bucket_size_for_zabbix_v2.py <compartment_ocid> <namespace>
# ##############################################################################################################################
#importações
import datetime
import time
import oci
import json
from datetime import timedelta
import argparse
import random
from zabbix_utils import ItemValue, Sender

# Configurando o argparse para receber os argumentos de linha de comando
# Argumentos: compartment e namespace
parser = argparse.ArgumentParser(description="Informe o nome do compartment e o namespace.")
parser.add_argument("compartment", type=str, help="Digite o compartment OCID")
parser.add_argument("namespace", type=str, help="Digite o namespace do bucket")
args = parser.parse_args()

# Funções do sistema

def consultar_bucket(bucket_name):
    try:
        get_bucket_response = object_storage_client.get_bucket(namespace_name=namespace_name, bucket_name=bucket_name)
        bucket_id = get_bucket_response.data.id
        query_txt = f'StoredBytes[5m]{{resourceID = "{bucket_id}"}}.max()'

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
            print(f" [o] Limite de requisições atingido. Aguardando {wait_time:.2f}s antes de tentar novamente para o bucket '{bucket_name}'...")
            time.sleep(wait_time)
            return consultar_bucket(bucket_name)  # Tenta novamente
        else:
            print(f">> Erro ao consultar bucket '{bucket_name}': {str(e)}")
            return 0

print("Iniciando a coleta de tamanho dos buckets do OCI Object Storage...")


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

#criando uma lista para armazenar os nomes dos buckets
balde = []
# Adicionando os nomes dos buckets à lista
for bucket in list_buckets_response.data:
    balde.append(bucket.name)

# Executando a consulta com controle de taxa
for dtBalde in balde:
    tamanho = consultar_bucket(dtBalde)
    dados_zabbix.append({
        "bucket_name": dtBalde,
        "bucket_size": tamanho
    })


# Nova Abordagem: Formatação do JSON de saída

# Criar os itens para envio ao Zabbix
items = []
 
# Adicionar o payload completo para o host manager
payload_completo = json.dumps({"data": dados_zabbix})
items.append(ItemValue('teste_sender_oci', 'oci_buckets.payload', payload_completo))
 
# Adicionar itens individuais para cada bucket
for item in dados_zabbix:
    bucket_name = item["bucket_name"]
    bucket_size = item["bucket_size"]
    payload_json = json.dumps(item)
    
    print(f"Payload JSON: {payload_json}")
    # Adicionar o item com o nome do bucket como host
    items.append(ItemValue(bucket_name, 'oci_buckets.payload', payload_json))
 
# Enviar os itens ao Zabbix
sender = Sender('sa-sp1-be-pool-1.monitoracao.sasp1.oci.i.globo', 10003)
response = sender.send(items)





'''
# Salvar em arquivo JSON para envio posterior
        
payload_json = {"data": dados_zabbix}

print(json.dumps(payload_json, indent=2))

items = [
    ItemValue('teste_sender_oci', 'oci_buckets_payload', json.dumps(payload_json, indent=2))
]

sender = Sender('sa-sp1-be-pool-1.monitoracao.sasp1.oci.i.globo', 10003)
response = sender.send(items)

'''
print("Payload enviado ao Zabbix:")
print(items)
print("Resposta do Zabbix:")
print(response)
print(f"Payload gerado com {len(dados_zabbix)} entradas.")
print("Coleta concluída.")