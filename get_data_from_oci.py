import oci

# Carrega a configuração
config = oci.config.from_file()
object_storage = oci.object_storage.ObjectStorageClient(config)

# Substitua pelo OCID do seu compartimento
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"

# Descobre o namespace (necessário para chamadas do Object Storage)
namespace = object_storage.get_namespace().data

# Lista os buckets do compartimento
buckets = object_storage.list_buckets(namespace_name=namespace, compartment_id=compartment_id).data

for bucket in buckets:
    print(f"\nBucket: {bucket.name}")
    
    # Lista os objetos dentro do bucket
    objects = object_storage.list_objects(namespace_name=namespace, bucket_name=bucket.name).data.objects

    for obj in objects:
        print(f"  - Objeto: {obj.name} | Tamanho: {obj.size} bytes")