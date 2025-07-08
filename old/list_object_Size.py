import oci

# Carrega a configuração padrão (~/.oci/config)
config = oci.config.from_file()

# Cria o cliente de Object Storage
object_storage = oci.object_storage.ObjectStorageClient(config)

# Define os parâmetros
namespace = object_storage.get_namespace().data
bucket_name = "oci_oci_spo_ia_jcorp_db_arch"  # Substitua pelo nome do seu bucket
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"  # Substitua pelo OCID do compartimento

# Obtém os detalhes do bucket
bucket = object_storage.get_bucket(namespace, bucket_name).data

# Exibe o tamanho armazenado e número de objetos
print(bucket)
print(bucket.approximate_size)
#print(f"Tamanho armazenado: {bucket.approximate_size / (1024**2):.2f} MB")
#print(f"Número de objetos: {bucket.approximate_count}")