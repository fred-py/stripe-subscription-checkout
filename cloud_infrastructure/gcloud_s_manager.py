# Import the Secret Manager client library.
from google.cloud import secretmanager
#from google.cloud import run_v1

# https://cloud.google.com/secret-manager/docs/reference/libraries#client-libraries-install-python



def get_env(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode('UTF-8')




#client = run_v1.ServicesClient()
#service_name = client.service_path("stripe-checkout-424311", "australia-southeast1", "service-c4790b5")

# Fetch the latest service configuration
#service = client.get_service(service_name)
#print(service)
# Update the service configuration
# ...
#client.replace_service(service_name, service)