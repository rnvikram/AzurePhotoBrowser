from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions, generate_blob_sas, BlobSasPermissions
import datetime 

class BlobService():
    def __init__(self, name,key, container_name ) -> None:
        self.azure_storage_connection_string = f"DefaultEndpointsProtocol=https;AccountName={name};AccountKey={key};EndpointSuffix=core.windows.net"
        self.name =  name
        self.key = key
        self.sas_token = generate_account_sas(
            account_name=name,
            account_key=key,
            resource_types=ResourceTypes(service=True,container=True),
            permission=AccountSasPermissions(read=True, list=True,process=True),
            expiry=datetime.datetime.utcnow().utcnow() + datetime.timedelta(hours=1)
        )

        self.blob_service_client = BlobServiceClient(account_url=f"https://{name}.blob.core.windows.net", credential=self.sas_token)
        self.container_name = container_name
        self.container_client=self.blob_service_client.get_container_client(self.container_name)

    def list_files_in_blob(self, name, results_per_page=200):
        blob_list = self.container_client.list_blobs(name_starts_with=f"Engagement/", results_per_page=results_per_page).by_page(None)
        blob_list_final = []
        for blob in list(next(blob_list)):
            blob_list_final.append( blob.name)
        return blob_list_final
    

    def get_blob_sas_url(self, blob_name):
        sas_blob = generate_blob_sas(account_name=self.name, 
                                    container_name=self.container_name,
                                    blob_name=blob_name,
                                    account_key=self.key,
                                    permission=BlobSasPermissions(read=True),
                                    expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1))
        url = 'https://'+self.name+'.blob.core.windows.net/'+self.container_name+'/'+blob_name+'?'+sas_blob
        return url