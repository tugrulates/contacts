"""Unittests for contact_diff."""


from contacts.contact import Contact, ContactInfo
from tests.contact_diff import ContactDiff


def test_add_field() -> None:
    """Test adding a top level field."""
    before = Contact(contact_id="ID", name="NAME")
    after = Contact(contact_id="ID", name="NAME", note="NOTE")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == [("ID", "note", "NOTE")]
    assert sorted(diff.deletes) == []


def test_delete_field() -> None:
    """Test deleting a top level field."""
    before = Contact(contact_id="ID", name="NAME", note="NOTE")
    after = Contact(contact_id="ID", name="NAME")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == [("ID", "note")]


def test_update_field() -> None:
    """Test updating a top level field."""
    before = Contact(contact_id="ID", name="NAME", note="NOTE")
    after = Contact(contact_id="ID", name="NAME", note="NEW_NOTE")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [("ID", "note", "NEW_NOTE")]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []


def test_add_info() -> None:
    """Test adding a contact info."""
    before = Contact(contact_id="ID", name="NAME")
    after = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == [("ID", "emails", "LABEL", "VALUE")]
    assert sorted(diff.deletes) == []


def test_delete_info() -> None:
    """Test deleting a contact info."""
    before = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(contact_id="ID", name="NAME")
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == []
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == [("ID", "emails", "EMAIL_ID")]


def test_update_info_value() -> None:
    """Test updating a contact info."""
    before = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="LABEL", value="NEW_VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [("ID", "emails", "EMAIL_ID", "LABEL", "NEW_VALUE")]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []


def test_update_info_label() -> None:
    """Test updating a contact info."""
    before = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="LABEL", value="VALUE")],
    )
    after = Contact(
        contact_id="ID",
        name="NAME",
        emails=[ContactInfo(info_id="EMAIL_ID", label="NEW_LABEL", value="VALUE")],
    )
    diff = ContactDiff(before, after)
    assert sorted(diff.updates) == [("ID", "emails", "EMAIL_ID", "NEW_LABEL", "VALUE")]
    assert sorted(diff.adds) == []
    assert sorted(diff.deletes) == []
