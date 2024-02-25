from azure.storage.blob import BlobServiceClient, BlobClient
import io
import pandas as pd

def get_details():
    connection_string = "BlobEndpoint=https://httpplaywright.blob.core.windows.net/;QueueEndpoint=https://httpplaywright.queue.core.windows.net/;FileEndpoint=https://httpplaywright.file.core.windows.net/;TableEndpoint=https://httpplaywright.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=b&srt=sco&sp=rwdlaciyx&se=2025-12-03T00:34:46Z&st=2024-02-13T16:34:46Z&spr=https,http&sig=lXiCL5LzwMIW16vXWVOvFgGSAGMCk3QaB8faSBXvCIU%3D"
    container_name = 'pandas'
    return connection_string, container_name

def get_clients_with_connection_string():
    connection_string, container_name = get_details()
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client


## Read

def read_from_blob(blob_file_path):
    container_client = get_clients_with_connection_string()
    blob_client = container_client.get_blob_client(blob_file_path)
    byte_data = blob_client.download_blob()
    return byte_data


# List

def list_files_in_blob():
    container_client = get_clients_with_connection_string()
    file_ls = [file['name'] for file in list(container_client.list_blobs())]
    return file_ls

# Upload
def upload_to_blob(file_name,file_type,df):
    connection_string, container_name = get_details()
    blob=BlobClient.from_connection_string(
    connection_string,
    container_name=container_name,
    blob_name=file_name
    )

    if file_type=='xlsx':
        writer=io.BytesIO()
        df.to_excel(writer, index=False)
        file_data=writer.getvalue()

    elif file_type=='csv':
        file_data=df.to_csv(encoding='latin-1',sep=';')
        
    try:
        blob.upload_blob(file_data,overwrite=True)
        return "Upload arquivo realizado com sucesso"
    except Exception as err:
        return err

#Delete

def delete_blob(blob_name):
    connection_string, container_name = get_details()
    blob = BlobClient.from_connection_string(connection_string, container_name=container_name, blob_name=blob_name)
    blob.delete_blob(delete_snapshots="include")
    print(f"Deleted {blob_name}")

if __name__ == "__main__":
    container_client = get_clients_with_connection_string()
    