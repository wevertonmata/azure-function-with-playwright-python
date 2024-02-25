from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

from app.log.logger import Logger
logger = Logger(__name__)


class BlobStorageFacade:
    """
    Uma fachada para se conectar a um container do Azure Blob Storage.

    Args:
    connection_string (str): A string de conexão para a conta de armazenamento.
    container_name (str): O nome do container a ser conectado.

    Attributes:
    blob_service_client (BlobServiceClient): O cliente para a conta de armazenamento.
    container_client (ContainerClient): O cliente para o container.
    """
    DEFAULT_CONTAINER = 'importar'

    def __init__(self, blob_service_client: BlobServiceClient):
        self.blob_service_client = blob_service_client
        self.container_client = self.blob_service_client.get_container_client(self.DEFAULT_CONTAINER)

    def upload_blob(self, blob_name: str, data: bytes, directory_name: str = None, container: str = DEFAULT_CONTAINER):
        """
        Faz upload de um blob para o container.

        Args:
        blob_name (str): O nome do blob a ser enviado.
        data (bytes): Os dados do blob a serem enviados.
        container (str): O nome do container.
        """
        try:
            container_client = self.blob_service_client.get_container_client(container)
            if directory_name:
                blob_client = container_client.get_blob_client(f'{directory_name}/{blob_name}')
            else:
                blob_client = container_client.get_blob_client(blob_name)

            return blob_client.upload_blob(data)
        except Exception as ex:
            logger.error(f'Erro ao subir arquivo no blob: {ex}')
            return None

    def download_blob(self, blob_name: str, directory_name: str = None, container: str = DEFAULT_CONTAINER) -> bytes:
        """
        Faz download de um blob do container e retorna seus dados como bytes.

        Args:
        blob_name (str): O nome do blob a ser baixado.

        Returns:
        bytes: Os dados do blob baixado.
        """
        container_client = self.blob_service_client.get_container_client(container)

        if directory_name:
            blob_client = container_client.get_blob_client(f'{directory_name}/{blob_name}')
        else:
            blob_client = container_client.get_blob_client(blob_name)

        return blob_client.download_blob().readall()

    def get_url_blob(self, blob_name: str, container: str) -> str:
        try:
            sas_token = generate_blob_sas(
            self.blob_service_client.account_name,
            container_name=container,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
            )
            return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{container}/{blob_name}?{sas_token}"
        except Exception as ex:
            logger.error(f'Erro ao obter URI de blob {blob_name} no container {container}: {ex}')
            return ''

    def get_blob_client(self, blob_name: str, container: str):
        return self.blob_service_client.get_blob_client(container, blob_name)

    def delete_blob(self, blob_name: str, container: str) -> None:
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container, blob=blob_name)
            blob_client.delete_blob()
        except Exception as ex:
            logger.error(f'Erro ao excluir blob {blob_name} no container {container}: {ex}')

    def list_files(self, container: str = DEFAULT_CONTAINER):
        container_client = self.blob_service_client.get_container_client(container)
        return container_client.list_blobs()

    def blob_exists(self, blob_name: str) -> bool:
        """
        Verifica se um blob existe no container.

        Args:
        blob_name (str): O nome do blob a ser verificado.

        Returns:
        bool: True se o blob existir, False caso contrário.
        """
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.exists()

    def check_container_exists(self) -> bool:
        if self.container_client is not None:
            return True
        else:
            return False

    def create_container(self, container_name: str) -> None: #pragma: no cover
        self.blob_service_client.create_container(container_name)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def delete_container(self, container_name: str) -> None: #pragma: no cover
        self.blob_service_client.delete_container(container_name)