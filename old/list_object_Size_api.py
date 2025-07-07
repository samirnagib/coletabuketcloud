# This is an automatically generated code sample.
# To make this code sample work in your Oracle Cloud tenancy,
# please replace the values for any parameters whose current values do not fit
# your use case (such as resource IDs, strings containing ‘EXAMPLE’ or ‘unique_id’, and
# boolean, number, and enum parameters with values not fitting your use case).

import oci
import time
from datetime import datetime

# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file()


# Initialize service client with default config file
monitoring_client = oci.monitoring.MonitoringClient(config)


# Send the request to service, some parameters are not required, see API
# doc for more info
summarize_metrics_data_response = monitoring_client.summarize_metrics_data(
    compartment_id="ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma",
    summarize_metrics_data_details=oci.monitoring.models.SummarizeMetricsDataDetails(
        namespace="oci_objectstorage",
        query='StoredBytes[5m]{resourceID = "ocid1.bucket.oc1.sa-saopaulo-1.aaaaaaaaok6kbknypm5brzllao6znmllcnjwe4mz4bhx55clup2anb37nieq"}.sum()',
        
        start_time=datetime.strptime(
            "2025-07-07T09:00:00.000Z",
            "%Y-%m-%dT%H:%M:%S.%fZ"),
        end_time=datetime.strptime(
            "2025-07-07T10:00:00.000Z",
            "%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
    
    compartment_id_in_subtree=False)

# Get the data from response
#print(summarize_metrics_data_response.data)
print(summarize_metrics_data_response.data[0].aggregated_datapoints)