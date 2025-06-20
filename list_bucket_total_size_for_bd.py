import oci
import mysql.connector
import argparse


parser = argparse.ArgumentParser(description="Informe o nome do compartment e o namespace.")
parser.add_argument("compartment", type=str, help="Digite o compartment OCID")
parser.add_argument("namespace", type=str, help="Digite o namespace do bucket")


args = parser.parse_args()

# Exibindo os valores
print(f"Compartment: {args.compartment}")
print(f"Namespace: {args.namespace}")

oci_compartment = args.compartment
oci_namespace = args.namespace




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

config = oci.config.from_file()

# Initialize service client with default config file
object_storage_client = oci.object_storage.ObjectStorageClient(config)
identity_client = oci.identity.IdentityClient(config)

oci_compartment_txt = identity_client.get_compartment(oci_compartment).data


print(f"Trabalhando com o compartment: {oci_compartment_txt.name}")


list_buckets_response = object_storage_client.list_buckets(
    namespace_name=oci_namespace,
    compartment_id=oci_compartment,
    limit=300)


for bucket in list_buckets_response.data:

    list_objects_response = object_storage_client.list_objects(
    namespace_name=oci_namespace,
    bucket_name=bucket.name,
    fields="size")
    
    total_size = sum(obj.size for obj in list_objects_response.data.objects)
    print(f"Compartment: {oci_compartment_txt.name} Bucket: {bucket.name} Size: {total_size} bytes")
    # Inserir um registro
    qry_inserir = """
    INSERT INTO monitor_oci (oci_compartment, oci_bucket, oci_size)
    VALUES (%s, %s, %s)
    """
    dados = (oci_compartment_txt.name, bucket.name, total_size)
    cursor.execute(qry_inserir, dados)
    # Confirmar a inserção no banco
    conexao.commit()

# Encerrar conexões
cursor.close()
conexao.close()
    
    
#    print(f"Total size of objects in bucket {bucket.name}: {total_size} bytes")
print("")
print(f"Listando o total de: {len(list_buckets_response.data)} buckets")


