import importlib.metadata

from folio_uuid.folio_namespaces import FOLIONamespaces
from folio_uuid.folio_uuid import FolioUUID

try:
    __version__ = importlib.metadata.version("folio_uuid")
except importlib.metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "unknown"
