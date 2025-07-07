import oci



# Create a default config using DEFAULT profile in default location
# Refer to
# https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm#SDK_and_CLI_Configuration_File
# for more info
config = oci.config.from_file()


# Initialize service client with default config file
object_storage_client = oci.object_storage.ObjectStorageClient(config)


# Send the request to service, some parameters are not required, see API
# doc for more info
list_buckets_response = object_storage_client.list_buckets(
    namespace_name="grwpg6hbkpoi",
    compartment_id="ocid1.compartment.oc1..aaaaaaaa2tfrl5y3pqx2ckjb6utznfcffijn4ufdi6a7nykq6vuz7pip6cma")

#ist_objects_response = object_storage_client.list_objects(
#   namespace_name="grwpg6hbkpoi",
#   bucket_name="oci_oci_spo_ar_jcorp_db_arch",
#   fields="size")


#or object in list_objects_response.data.objects:
#   print(object.name)
#    print(object.size)
    
#otal_size = sum(obj.size for obj in list_objects_response.data.objects)

#rint(f"Total size of objects in bucket: {total_size} bytes")
#rint(f"Tamanho total: {total_size / (1024**2):.2f} MB\n")
# Uncomment the following lines to print all bucket names
#print(list_objects_response.data)

for bucket in list_buckets_response.data:
    #rint(bucket.name)
    print(bucket)
    
