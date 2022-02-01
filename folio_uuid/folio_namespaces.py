import enum


class FOLIONamespaces(enum.Enum):
    """
    ENUM for FOLIO Objects. Helping the FolioUUID to create
    unique deterministic uuids within a folio tenant
    """

    # Inventory
    holdings = 0
    items = 1
    instances = 2
    athorities = 14

    # SRS
    srs_records = 3
    raw_records = 4
    parsed_records = 5

    # Circulation
    loans = 6
    requests = 7

    # Users
    users = 8
    permissions_users = 9

    # Acquisitions
    orders = 10
    po_lines = 11
    organizations = 12
    edifact = 15

    # ERM
    # ERM Does not honor generated UUIDs

    # Other
    other = 13
