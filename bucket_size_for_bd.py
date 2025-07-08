# ##############################################################################################################################
# Coleta de Tamanho de Buckets do OCI Object Storage para Banco de Dados MySQL
# Versão 1.0
# Autor: Samir Lins Nagib (samir@g.globo)
# Data: 07/07/2025  
# Descrição: Este script coleta o tamanho dos buckets do OCI Object Storage e insere uns dados para ingetão em um banco de 
# dados MySQL.
# Requisitos: Biblioteca OCI Python SDK, Biblioteca MySQL Connector/Python
# Configuração do banco de dados MySQL: Deve existir um banco de dados chamado 'buckets_monitor_geral' e uma tabela 
# chamada 'monitor_oci' com as colunas especificadas.
# Uso: Execute o script passando o OCID do compartment e o namespace do bucket como argumentos de linha de comando.
# Exemplo: python bucket_size_for_bd.py <compartment_ocid> <namespace>
# ##############################################################################################################################
#importações
import datetime
import time
import oci
import json
from datetime import timedelta
import argparse
import mysql.connector

parser = argparse.ArgumentParser(description="Informe o nome do compartment e o namespace.")
parser.add_argument("compartment", type=str, help="Digite o compartment OCID")
parser.add_argument("namespace", type=str, help="Digite o namespace do bucket")

args = parser.parse_args()

# Atribuindo os valores dos argumentos às variáveis
oci_compartment = args.compartment
oci_namespace = args.namespace


bd_conection = mysql.connector.connect(
    host='10.86.129.16',       # ou IP do servidor MySQL
    user='samir',
    password='[2b5A&;caQ9Y#+99&f)n'
)

# Criar o banco de dados se não existir
cursor_bd = bd_conection.cursor()

cursor_bd.execute("CREATE DATABASE IF NOT EXISTS buckets_monitor_geral DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
cursor_bd.close()

bd_conection.commit()
bd_conection.close()


# Conectar ao banco de dados
conexao = mysql.connector.connect(
    host='10.86.129.16',       # ou IP do servidor MySQL
    user='samir',
    password='[2b5A&;caQ9Y#+99&f)n',
    database='buckets_monitor_geral'
)

cursor = conexao.cursor()

# Criar a tabela
comando_criacao = """
CREATE TABLE IF NOT EXISTS monitor_oci (
    id_oci_table INT AUTO_INCREMENT PRIMARY KEY,
    momento_oci_table TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    oci_compartment VARCHAR(255),
    oci_bucket VARCHAR(255),
    oci_size BIGINT UNSIGNED
);
"""
cursor.execute(comando_criacao)
#cursor.commit()





# Timestamp atual
timestamp = time.time()

# Convertendo timestamp para datetime
dt_object = datetime.datetime.fromtimestamp(timestamp)

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
identity_client = oci.identity.IdentityClient(config)
monitoring_client = oci.monitoring.MonitoringClient(config)


# Definindo o namespace e o compartment
namespace_name = oci_namespace
compartment_id = oci_compartment
oci_compartment_txt = identity_client.get_compartment(oci_compartment).data

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

    # Get the data from response
    if not summarize_metrics_data_response.data:
        tamanho = 0
    else:
        points = summarize_metrics_data_response.data[0].aggregated_datapoints
        
        valores = [p.value for p in points]
        tamanho = valores[-1] if valores else 0
        print(f"Compartment: {oci_compartment_txt.name} Bucket: {dtBalde} Size: {tamanho} bytes")

        # Inserir um registro
        qry_inserir = """
        INSERT INTO monitor_oci (oci_compartment, oci_bucket, oci_size)
        VALUES (%s, %s, %s)
        """
        dados = (oci_compartment_txt.name, dtBalde, tamanho)
        cursor.execute(qry_inserir, dados)
        # Confirmar a inserção no banco
        conexao.commit()
    




# Encerrar conexões
cursor.close()
conexao.close()
    