import math
import re
import uuid
from warnings import warn

from folio_uuid.folio_namespaces import FOLIONamespaces


class FolioUUID(uuid.UUID):
    """Creates deterministic UUIDs for FOLIO"""

    base_namespace = uuid.UUID("8405ae4d-b315-42e1-918a-d1919900cf3f")

    def __init__(
        self,
        tenant_string: str,
        folio_object_type: FOLIONamespaces,
        legacy_identifier: str,
        *,
        tenant_id: str = None,  # Deprecated
        okapi_url: str = None,  # Deprecated
    ):
        """
        Create a deterministic UUID for a FOLIO tenant

        Parameters
        ----------
        tenant_string : str
            The tenant id (or other tenant identifying string, eg. tenant-specific API base URL)
        folio_object_type : FOLIONamespaces
            Enum helping to avoid collisions within a tenant.
        legacy_identifier : str
            The actual identifier from the legacy system
        *,
        tenant_id : str
            The tenant ID of the target tenant. Default: None, Keyword-only (Deprecated)
        okapi_url : str
            The URL of the target tenant at okapi. Default: None, (Deprecated)
        """
        if not str(legacy_identifier or "").strip():
            raise ValueError("Legacy Identifier not provided")
        clean_id = self.clean_iii_identifiers(legacy_identifier)
        if okapi_url:
            warn(
                "okapi_url is deprecated. Use tenant_string instead",
                DeprecationWarning,
                stacklevel=2,
            )
        value_components = [okapi_url or tenant_string, folio_object_type.name, clean_id]
        if tenant_id:
            warn(
                "tenant_id is deprecated. Use tenant_string instead",
                DeprecationWarning,
                stacklevel=2,
            )
            value_components.insert(1, tenant_id)
        u = uuid.uuid5(
            self.base_namespace,
            ":".join(value_components),
        )
        super(FolioUUID, self).__init__(str(u))

    @staticmethod
    def calculate_sierra_check_digit(record_number: int) -> str:
        """Rewritten to python from
        https://github.com/SydneyUniLibrary/sierra-record-check-digit/blob/master/index.js"""
        m = 2
        x = 0
        i = record_number
        while i > 0:
            a = i % 10
            i = math.floor(i / 10)
            x += a * m
            m += 1
        r = x % 11
        return "x" if r == 10 else str(r)

    @staticmethod
    def clean_iii_identifiers(identifier: str) -> str:
        """
        Cleans potential III/SIERRA/Millennium Identifiers from noise like
        the dot (.) and check digits and potential other things at
        the end of the strings. All other types of identifiers
        should just run through.

        Parameters
        ----------
        identifier : str
            An identifier of any kind.

        """
        reg_pattern = r"^(\.?[bcoiv]?)([0-9]{5,7})([0-9Xx]?)(@\w{1,5})?$"
        match = re.search(reg_pattern, str(identifier))
        if not match or not match[1]:  # No match, no III id
            return str(identifier)
        fore = match[1]
        number_part = match[2]
        last_char = match[3]
        if len(number_part) > 6:
            # Aft  is reachable by aft = match[3]
            nums = int(number_part)
            if FolioUUID.calculate_sierra_check_digit(nums) == last_char:
                return f"{fore.replace('.', '')}{nums}"
            else:
                return f"{fore.replace('.', '')}{number_part}"
        elif len(number_part) == 6:
            return f"{fore.replace('.', '')}{number_part}"
        else:
            return str(identifier)
