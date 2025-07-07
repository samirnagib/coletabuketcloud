import oci
import json
from datetime import datetime

config = oci.config.from_file()
object_storage_client = oci.object_storage.ObjectStorageClient(config)

namespace_name = "grwpg6hbkpoi"
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"

list_buckets_response = object_storage_client.list_buckets(
    namespace_name=namespace_name,
    compartment_id=compartment_id,
    limit=300
)

dados_zabbix = []


for bucket in list_buckets_response.data:
    list_objects_response = object_storage_client.list_objects(
        namespace_name=namespace_name,
        bucket_name=bucket.name,
        fields="size, id"
    )
    total_size = sum(obj.size for obj in list_objects_response.data.objects)
    
    print(f"Bucket: {bucket.name}, Bucket ID: {bucket.id}, Total Size: {total_size} bytes")

    dados_zabbix.append({
        "bucket_name": f"{bucket.name}",
        "bucket_size": total_size
    })


# Salvar em arquivo JSON para envio posterior
with open("zabbix_oci_payload3.json", "w") as f:
    #for item in dados_zabbix:
    json.dump({"data": dados_zabbix}, f, indent=2)


print(f"Arquivo gerado com {len(dados_zabbix)} entradas.")

