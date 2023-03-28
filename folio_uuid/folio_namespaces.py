import enum


class FOLIONamespaces(enum.Enum):
    """
    ENUM for FOLIO Objects. Helping the FolioUUID to create
    unique deterministic uuids within a folio tenant
    """

    # Inventory (0-2, 14)
    holdings = 0
    items = 1
    instances = 2
    authorities = 14

    # SRS (3-5, 16-18)
    srs_records_bib = 3
    srs_records_holdingsrecord = 16
    srs_records_auth = 17
    srs_records_edifact = 18
    raw_records = 4
    parsed_records = 5

    # Circulation (6-7, 25)
    loans = 6
    requests = 7
    fees_fines = 25

    # Users (8-9, 23)
    users = 8
    permissions_users = 9
    request_preference = 24

    # Acquisitions (10-12, 15)
    orders = 10
    po_lines = 11
    organizations = 12
    edifact = 15

    # ERM
    # ERM Does not honor generated UUIDs

    # Courses (19-22)
    course = 19
    course_listing = 20
    instructor = 21
    reserve = 22

    # Other
    note = 23
    other = 13
