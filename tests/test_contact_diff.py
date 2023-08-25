"""Unittests for contact_diff."""


from contacts.contact import Contact, ContactAddress, ContactInfo
from tests.contact_diff import ContactDiff


def test_update_field() -> None:
    """Test updating a top level field."""
    before = Contact(id="ID", name="NAME", note="NOTE")
    after = Contact(id="ID", name="NAME", note="NEW_NOTE")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [("ID", "note", "NEW_NOTE")]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []


def test_add_field() -> None:
    """Test adding a top level field."""
    before = Contact(id="ID", name="NAME")
    after = Contact(id="ID", name="NAME", note="NOTE")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [("ID", "note", "NOTE")]
    assert sorted(diff.adds) == []  # adds are for info only
    assert sorted(diff.deletes) == []


def test_delete_field() -> None:
    """Test deleting a top level field."""
    before = Contact(id="ID", name="NAME", note="NOTE")
    after = Contact(id="ID", name="NAME")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == [("ID", "note")]


def test_add_info_single_value() -> None:
    """Test adding a simple contact info."""
    before = Contact(id="ID", name="NAME")
    after = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == [("ID", "emails", {"label": "LABEL", "value": "VALUE"})]
    assert sorted(diff.deletes) == []


def test_add_info_multiple_values() -> None:
    """Test adding a rich contact info."""
    before = Contact(
        id="ID",
        name="NAME",
    )
    after = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="ADDRESS_ID",
                label="LABEL",
                value="VALUE",
                city="CITY",
                country="COUNTRY",
            )
        ],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == [
        (
            "ID",
            "addresses",
            {"label": "LABEL", "value": "VALUE", "city": "CITY", "country": "COUNTRY"},
        )
    ]
    assert sorted(diff.deletes) == []


def test_delete_info() -> None:
    """Test deleting a contact info."""
    before = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(id="ID", name="NAME")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == [("ID", "emails", "EMAIL_ID")]


def test_update_info_single_value() -> None:
    """Test updating a simple contact info."""
    before = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="LABEL", value="NEW_VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [
        ("ID", "emails", "EMAIL_ID", {"value": "NEW_VALUE"})
    ]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []


def test_update_info_multiple_values() -> None:
    """Test updating a rich contact info."""
    before = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="ADDRESS_ID",
                label="LABEL",
                value="VALUE",
                city="CITY",
                country="COUNTRY",
            )
        ],
    )
    after = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="ADDRESS_ID",
                label="LABEL",
                value="VALUE",
                city="NEW_CITY",
                country="NEW_COUNTRY",
            )
        ],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [
        (
            "ID",
            "addresses",
            "ADDRESS_ID",
            {"city": "NEW_CITY", "country": "NEW_COUNTRY"},
        )
    ]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []


def test_update_info_label() -> None:
    """Test updating a contact info."""
    before = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(
        id="ID",
        name="NAME",
        emails=[ContactInfo(id="EMAIL_ID", label="NEW_LABEL", value="VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [
        ("ID", "emails", "EMAIL_ID", {"label": "NEW_LABEL"})
    ]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []
