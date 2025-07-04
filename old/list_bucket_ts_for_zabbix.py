import oci
import json
from datetime import datetime

config = oci.config.from_file()
object_storage_client = oci.object_storage.ObjectStorageClient(config)

namespace_name = "grwpg6hbkpoi"
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"
zabbix_host = "meu_host_zabbix"  # substitua pelo nome exato do host cadastrado no Zabbix

list_buckets_response = object_storage_client.list_buckets(
    namespace_name=namespace_name,
    compartment_id=compartment_id,
    limit=300
)

dados_zabbix = []

with open("zabbix_oci_payload3.json", "w") as f:
    f.write("{\n")
    f.write('"data": [\n')


for bucket in list_buckets_response.data:
    list_objects_response = object_storage_client.list_objects(
        namespace_name=namespace_name,
        bucket_name=bucket.name,
        fields="size"
    )
    total_size = sum(obj.size for obj in list_objects_response.data.objects)

    dados_zabbix.append({
        "bucket_name": f"{bucket.name}",
        "bucket_size": total_size
    })

# Salvar em arquivo JSON para envio posterior
with open("zabbix_oci_payload3.json", "a") as f:
    for item in dados_zabbix:
        f.write(json.dumps(item) + ",\n")
    f.write("]\n")
    f.write("}")


print(f"Arquivo gerado com {len(dados_zabbix)} entradas.")