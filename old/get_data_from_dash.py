import oci

config = oci.config.from_file()


# Initialize service client with default config file
dashboard_service_client = oci.dashboard_service.DashboardClient(config)


# Send the request to service, some parameters are not required, see API
# doc for more info
get_dashboard_response = dashboard_service_client.get_dashboard(
    dashboard_id="ocid1.consoledashboard.oc1..aaaaaaaawzcpyeffzjh5bu6fw435zrqxif4gzohbgmvptdjmxheo6l2g3xqq")

# Get the data from response
print(get_dashboard_response.data)
