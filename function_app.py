import azure.functions as func
import logging
from playwright.async_api import async_playwright
from azure.storage.blob import BlobServiceClient, BlobClient
import pandas as pd
import io

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
async def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("http://playwright.dev")
        title = await page.title()
        await browser.close()
        
        d = d = {f'{title}': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(data=d)
        upload_to_blob(title,"csv",df)

        return func.HttpResponse(
             f"Title: {title}",
             status_code=200
        )

def get_details():
    connection_string = "BlobEndpoint=https://httpplaywright.blob.core.windows.net/;QueueEndpoint=https://httpplaywright.queue.core.windows.net/;FileEndpoint=https://httpplaywright.file.core.windows.net/;TableEndpoint=https://httpplaywright.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=b&srt=sco&sp=rwdlaciyx&se=2025-12-03T00:34:46Z&st=2024-02-13T16:34:46Z&spr=https,http&sig=lXiCL5LzwMIW16vXWVOvFgGSAGMCk3QaB8faSBXvCIU%3D"
    container_name = 'pandas'
    return connection_string, container_name

def get_clients_with_connection_string():
    connection_string, container_name = get_details()
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

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
    