import os
import tempfile
from typing import Dict, Any, List, Optional
import boto3
from botocore.client import Config
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class MinIOPDFLoader:
    """
    A custom loader to parse PDF files from MinIO S3 storage using LangChain.
    Configured via environment variables, keyword arguments, or a config dictionary.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None, **kwargs):
        """
        Initialize MinIO PDF Loader.

        Args:
            config: Optional dictionary with MinIO configuration.
            **kwargs: Override configuration parameters.
        """
        self.config = self._load_config(config or {}, **kwargs)

        # Validate required configuration
        required_keys = ['endpoint_url', 'access_key', 'secret_key', 'bucket_name']
        for key in required_keys:
            if not self.config.get(key):
                raise ValueError(f"Missing required configuration: {key}")

        self.bucket_name = self.config['bucket_name']

        # Configure S3 client for MinIO
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.config['endpoint_url'],
            aws_access_key_id=self.config['access_key'],
            aws_secret_access_key=self.config['secret_key'],
            region_name=self.config.get('region_name', 'us-east-1'),
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'}
            ),
            use_ssl=self.config.get('use_ssl', True),
            verify=False  # NOTE: Set to True in production with proper SSL certificates
        )

    def _load_config(self, base_config: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Load configuration from provided dictionary, kwargs, and environment variables.
        Priority: kwargs > base_config > env vars > defaults
        """
        config = {}

        config['endpoint_url'] = kwargs.get('endpoint_url') \
            or base_config.get('endpoint_url') \
            or os.getenv('MINIO_ENDPOINT_URL')

        config['bucket_name'] = kwargs.get('bucket_name') \
            or base_config.get('bucket_name') \
            or os.getenv('MINIO_BUCKET_NAME')

        config['region_name'] = kwargs.get('region_name') \
            or base_config.get('region_name') \
            or os.getenv('MINIO_REGION_NAME', 'us-east-1')

        config['access_key'] = kwargs.get('access_key') \
            or base_config.get('access_key') \
            or os.getenv('MINIO_ACCESS_KEY')

        config['secret_key'] = kwargs.get('secret_key') \
            or base_config.get('secret_key') \
            or os.getenv('MINIO_SECRET_KEY')

        use_ssl_env = os.getenv('MINIO_USE_SSL', 'true').lower()
        config['use_ssl'] = kwargs.get('use_ssl') \
            if 'use_ssl' in kwargs else \
            base_config.get('use_ssl', use_ssl_env in ('true', '1', 'yes', 'on'))

        return config

    def load_pdf_from_s3_uri(self, s3_uri: str) -> List[Document]:
        if not s3_uri.startswith('s3://'):
            raise ValueError("URI must start with 's3://'")

        uri_parts = s3_uri[5:].split('/', 1)
        bucket = uri_parts[0]
        key = uri_parts[1] if len(uri_parts) > 1 else ''

        if bucket != self.bucket_name:
            raise ValueError(f"Bucket in URI ({bucket}) doesn't match configured bucket ({self.bucket_name})")

        return self._load_pdf_by_key(key, s3_uri)

    def load_pdf_by_key(self, object_key: str) -> List[Document]:
        s3_uri = f"s3://{self.bucket_name}/{object_key}"
        return self._load_pdf_by_key(object_key, s3_uri)

    def _load_pdf_by_key(self, object_key: str, s3_uri: str) -> List[Document]:
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            try:
                self.s3_client.download_file(self.bucket_name, object_key, temp_file.name)
                loader = PyPDFLoader(temp_file.name)
                documents = loader.load()

                for doc in documents:
                    doc.metadata.update({
                        's3_uri': s3_uri,
                        'bucket': self.bucket_name,
                        'key': object_key,
                        'source_type': 'minio_s3',
                        'loader_type': 'minio_pdf_loader'
                    })
                return documents
            finally:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)

    def get_text_content(self, s3_uri: str) -> str:
        documents = self.load_pdf_from_s3_uri(s3_uri)
        return "\n".join(doc.page_content for doc in documents)

    def get_text_content_by_key(self, object_key: str) -> str:
        documents = self.load_pdf_by_key(object_key)
        return "\n".join(doc.page_content for doc in documents)

    def list_pdfs(self, prefix: str = "") -> List[str]:
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            pdf_keys = [
                obj['Key']
                for obj in response.get('Contents', [])
                if obj['Key'].lower().endswith('.pdf')
            ]
            return pdf_keys
        except Exception as e:
            print(f"Error listing PDFs: {e}")
            return []

    def check_connection(self) -> bool:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


class MinIOPDFUploader:
    """
    Utility class to upload PDF files to MinIO and return their S3 URIs.
    """

    def __init__(
        self,
        endpoint_url: str = None,
        bucket_name: str = None,
        region_name: str = None,
        access_key: str = None,
        secret_key: str = None,
        use_ssl: bool = None
    ):
        """
        Initialize MinIO PDF Uploader with either provided values or environment variables.

        Args:
            endpoint_url: MinIO server endpoint (e.g. "http://localhost:9000")
            bucket_name: Bucket name
            region_name: AWS region (default: "us-east-1")
            access_key: MinIO access key
            secret_key: MinIO secret key
            use_ssl: Whether to use SSL (default: True if env MINIO_USE_SSL is "true")
        """
        self.endpoint_url = endpoint_url or os.getenv("MINIO_ENDPOINT_URL")
        self.bucket_name = bucket_name or os.getenv("MINIO_BUCKET_NAME")
        self.region_name = region_name or os.getenv("MINIO_REGION_NAME", "us-east-1")
        self.access_key = access_key or os.getenv("MINIO_ACCESS_KEY")
        self.secret_key = secret_key or os.getenv("MINIO_SECRET_KEY")

        if use_ssl is None:
            use_ssl_env = os.getenv("MINIO_USE_SSL", "true").lower()
            self.use_ssl = use_ssl_env in ("true", "1", "yes", "on")
        else:
            self.use_ssl = use_ssl

        # Create S3 client
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
            use_ssl=self.use_ssl,
            verify=False  # Change to True if you have valid SSL certs
        )

    def upload_file(self, file_path: str, object_name: str = None) -> str:
        """Upload a local file to MinIO and return its S3 URI."""
        if not object_name:
            object_name = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            return f"s3://{self.bucket_name}/{object_name}"
        except Exception as e:
            raise RuntimeError(f"Failed to upload {file_path} to MinIO: {e}")

    def upload_fastapi_file(self, upload_file, object_name: str = None) -> str:
        """Upload a FastAPI UploadFile directly to MinIO."""
        if not object_name:
            object_name = upload_file.filename

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(upload_file.file.read())
            tmp.flush()
            return self.upload_file(tmp.name, object_name)


