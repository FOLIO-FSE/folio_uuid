# content of test_sample.py

import pytest
from folio_uuid import FOLIONamespaces
from folio_uuid import FolioUUID

made_up_okapi_url = "https://okapi.folio.ebsco.com"


def test_deterministic_uuid_generation_basic():
    deterministic_uuid = FolioUUID(made_up_okapi_url, FOLIONamespaces.items, "test")
    assert "ccfe50c7-e610-5584-a826-f918d7c8684d" == str(deterministic_uuid)


def test_deterministic_uuid_generation_sierra_weak_record_key():
    deterministic_uuid = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.items,
        "i3696836",
    )
    assert "da5b73ed-73ff-5d0f-8e11-e902a10dc60a" == str(deterministic_uuid)


def test_deterministic_uuid_generation_integer():
    deterministic_uuid = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.items,
        3696836,
    )
    assert "d0fb4758-e240-55f9-ae0f-fa1a1d693179" == str(deterministic_uuid)


def test_deterministic_uuid_generation_sierra_weak_record_key2():
    deterministic_uuid = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.items,
        "3696836",
    )
    assert deterministic_uuid


def test_deterministic_uuid_generation_empty_legacy_id():
    with pytest.raises(ValueError):
        FolioUUID(
            made_up_okapi_url,
            FOLIONamespaces.items,
            "",
        )


def test_deterministic_uuid_generation_space_legacy_id():
    with pytest.raises(ValueError):
        FolioUUID(
            made_up_okapi_url,
            FOLIONamespaces.items,
            " ",
        )


def test_deterministic_uuid_generation_none_legacy_id():
    with pytest.raises(ValueError):
        FolioUUID(
            made_up_okapi_url,
            FOLIONamespaces.items,
            None,
        )


def test_deterministic_uuid_generation_sierra_strong_record_key():
    deterministic_uuid = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.items,
        "i36968365",
    )
    assert "da5b73ed-73ff-5d0f-8e11-e902a10dc60a" == str(deterministic_uuid)


def test_deterministic_uuid_generation_sierra_strong_record_key_dot():
    deterministic_uuid = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.items,
        ".i36968365",
    )
    assert "da5b73ed-73ff-5d0f-8e11-e902a10dc60a" == str(deterministic_uuid)


def test_deterministic_uuid_generation_holdings():
    deterministic_uuid = FolioUUID(
        "https://okapi-bugfest-juniper.folio.ebsco.com",
        FOLIONamespaces.holdings,
        "000000167",
    )
    assert "a0b4c8a2-01fd-50fd-8158-81bd551412a0" == str(deterministic_uuid)


def test_checkdigit_creation():
    """Translated to python from https://github.com/SydneyUniLibrary/sierra-record-check-digit/blob/master/index-test.js"""
    known_check_digits = [
        [100114, "0"],
        [2539964, "0"],
        [100610, "1"],
        [1655776, "1"],
        [583623, "2"],
        [1629736, "2"],
        [572288, "3"],
        [4093863, "3"],
        [284683, "4"],
        [3898776, "4"],
        [395792, "5"],
        [3040121, "5"],
        [542671, "6"],
        [2626834, "6"],
        [459573, "7"],
        [2699873, "7"],
        [581326, "8"],
        [2054794, "8"],
        [539148, "9"],
        [1203395, "9"],
        [585345, "x"],
        [1562237, "x"],
    ]

    for combo in known_check_digits:
        assert FolioUUID.calculate_sierra_check_digit(combo[0]) == combo[1]


def test_obvious_record_numbers_with_check_digits():
    ids = [
        ["b33846327", "b3384632"],
        ["b47116523@mdill", "b4711652"],
        ["o100007x", "o100007"],
        ["b1125421x", "b1125421"],
        [".b1125421x", "b1125421"],
        ["#b33846327", "#b33846327"],
        ["b", "b"],
        [".b", ".b"],
        ["9999999", "9999999"],
        ["https://id.kb.se/fnrgl", "https://id.kb.se/fnrgl"],
        ["111", "111"],
        ["111111111111", "111111111111"],
        ["b12345", "b12345"],
        ["b4711652@", "b4711652@"],
        ["b4711652@toolong", "b4711652@toolong"],
        [".b12345", ".b12345"],
        [".b4711652@", ".b4711652@"],
        [".b4711652@toolong", ".b4711652@toolong"],
    ]

    for id_combo in ids:
        assert FolioUUID.clean_iii_identifiers(id_combo[0]) == id_combo[1]


def test_deterministic_uuid_srs_namespaces():
    deterministic_uuid_1 = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.srs_records_holdingsrecord,
        1,
    )
    deterministic_uuid_2 = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.srs_records_bib,
        1,
    )
    assert str(deterministic_uuid_2) != str(deterministic_uuid_1)

def test_deterministic_uuid_with_tenant_id():
    with_tenant_id = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.instances,
        "b1234567",
        "diku"
    )

    without_tenant_id = FolioUUID(
        made_up_okapi_url,
        FOLIONamespaces.instances,
        "b1234567"
    )
    assert str(with_tenant_id) == '053f8903-2be6-5fe4-985c-6fc6f2dbb566'
    assert str(without_tenant_id) == '27d1e3f0-35a7-53fe-99ff-7bdb492bff49'
    