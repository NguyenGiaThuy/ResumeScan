from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_core.tools import tool
from utilities.minio_pdf_helper import MinIOPDFLoader


@tool("docx_loader", description="Load a DOCX resume and return its text content.")
def docx_loader(resume_path: str) -> str:
    return "\n".join([page.page_content for page in Docx2txtLoader(resume_path).load()])


@tool("pdf_loader", description="Load a PDF resume and return its text content.")
def pdf_loader(resume_path: str) -> str:
    return "\n".join([page.page_content for page in PyPDFLoader(resume_path).load()])


@tool(
    "minio_pdf_loader",
    description="Load a PDF resume from MinIO S3 using S3 URI (s3://bucket/path/file.pdf) and return its text content.",
)
def minio_pdf_loader(s3_uri: str) -> str:
    """Load PDF from MinIO S3 storage using S3 URI format"""
    try:
        loader = MinIOPDFLoader()
        return loader.get_text_content(s3_uri)
    except Exception as e:
        return f"Error loading PDF from MinIO: {str(e)}"


@tool(
    "minio_pdf_loader_by_key",
    description="Load a PDF resume from MinIO S3 using object key (path/file.pdf) and return its text content.",
)
def minio_pdf_loader_by_key(object_key: str) -> str:
    """Load PDF from MinIO S3 storage using object key"""
    try:
        loader = MinIOPDFLoader()
        return loader.get_text_content_by_key(object_key)
    except Exception as e:
        return f"Error loading PDF from MinIO: {str(e)}"


@tool(
    "list_minio_pdfs",
    description="List all PDF files available in MinIO bucket with optional prefix filter.",
)
def list_minio_pdfs(prefix: str = "") -> str:
    """List available PDF files in MinIO bucket"""
    try:
        loader = MinIOPDFLoader()
        pdf_files = loader.list_pdfs(prefix)
        if pdf_files:
            return "Available PDF files:\n" + "\n".join(
                [f"- {pdf}" for pdf in pdf_files]
            )
        else:
            return "No PDF files found in the bucket."
    except Exception as e:
        return f"Error listing PDFs from MinIO: {str(e)}"
