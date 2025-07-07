import oci
import json
from datetime import datetime
import time

config = oci.config.from_file()
object_storage_client = oci.object_storage.ObjectStorageClient(config)

namespace_name = "grwpg6hbkpoi"
compartment_id = "ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma"


list_buckets_response = object_storage_client.list_buckets(
    namespace_name=namespace_name,
    compartment_id=compartment_id,
    limit=300
)

balde = []

for bucket in list_buckets_response.data:
    #print(bucket)
    #print(f"Name: {bucket.name}")
    balde.append(bucket.name)

for dtBalde in balde:
    #print(dtBalde)
    get_bucket_response = object_storage_client.get_bucket(namespace_name=namespace_name, bucket_name=dtBalde)
    print(f"Bucket Name..: {get_bucket_response.data.name} \nBucket id....: {get_bucket_response.data.id} \nStorage Tier.: {get_bucket_response.data.storage_tier}")
    time.sleep(1)
