import oci
config = oci.config.from_file()

# Initialize service client with default config file
object_storage_client = oci.object_storage.ObjectStorageClient(config)

list_buckets_response = object_storage_client.list_buckets(
    namespace_name="grwpg6hbkpoi",
    compartment_id="ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma",
    limit=300)


for bucket in list_buckets_response.data:

    list_objects_response = object_storage_client.list_objects(
    namespace_name="grwpg6hbkpoi",
    bucket_name=bucket.name,
    fields="size")
    #print(bucket.name)
    total_size = sum(obj.size for obj in list_objects_response.data.objects)
    print(f"Total size of objects in bucket {bucket.name}: {total_size} bytes")