import oci
from datetime import datetime, timedelta

# Configuração do cliente
config = oci.config.from_file()  # Assumindo que você tenha o config no ~/.oci/config
metrics_client = oci.monitoring.MonitoringClient(config)

# Parâmetros
namespace = "grwpg6hbkpoi"
bucket_name = "noci_oci_spo_ia_jcorp_db_diario"
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"
namespace_name = "grwpg6hbkpoi"  # Pode ser visto na página do bucket

# Consulta de métricacl
end_time = datetime.now()
start_time = end_time - timedelta(hours=1)

response = metrics_client.summarize_metrics_data(
    compartment_id=compartment_id,
    summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
        namespace=namespace,
        query=f"storage.usedBytes[1h].sum{{namespace=\"{namespace_name}\", bucketName=\"{bucket_name}\"}}",
        start_time=start_time,
        end_time=end_time
    )
)

for item in response.data:
    for data_point in item.aggregated_datapoints:
        size_in_bytes = data_point.value
        print(f"Tamanho do bucket {bucket_name}: {size_in_bytes / (1024 ** 3):.2f} GB")