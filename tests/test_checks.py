"""Unittests for contact_diff."""


from pathlib import Path

import email_validator
import pytest

from contacts.category import Category
from contacts.checks import url_check
from contacts.contact import Contact, ContactAddress, ContactInfo, ContactSocialProfile
from contacts.problem import Problem
from tests.mock_address_book import MockAddressBook


class ProblemChecker:
    """Checker that verifier problem details."""

    def __init__(self, mock_address_book: MockAddressBook):
        """Initialize checker with mock address book."""
        self._mock = mock_address_book

    def problem(self, contact: Contact) -> Problem:
        """Assert that there is a problem against contact and execute any fixes."""
        assert len(contact.problems) == 1
        problem = contact.problems[0]
        assert problem.category in {Category.WARNING, Category.ERROR}
        if problem.category == Category.WARNING:
            assert problem.fix is not None, "fix missing fix for an error"
            problem.fix(self._mock)
        elif problem.category == Category.ERROR:
            assert problem.fix is None, "fix given for an error"
        return problem


@pytest.fixture(scope="session", autouse=True)
def test_environment() -> None:
    """Initialize the test environment."""
    # disable DNS checks for e-mail address and URL checks
    email_validator.TEST_ENVIRONMENT = True
    url_check.TEST_ENVIRONMENT = True


@pytest.fixture(autouse=True)
def mock_address_book() -> MockAddressBook:
    """Fixture for prefs."""
    return MockAddressBook(Path("."))


@pytest.fixture(autouse=True)
def problem_checker(mock_address_book: MockAddressBook) -> ProblemChecker:
    """Fixture for prefs."""
    return ProblemChecker(mock_address_book)


def test_correct_contact() -> None:
    """Test contact that has no problems."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        prefix="Dr.",
        first_name="Bob",
        middle_name="Babála",
        last_name="Balon",
        suffix="Jr.",
        nickname="Bob Baker",
        job_title="Baker",
        department="Bakery",
        organization="Bakers LLC.",
        phones=[
            ContactInfo(info_id="PID1", label="_$!<Mobile>!$_", value="+1111111111"),
            ContactInfo(info_id="PID2", label="_$!<Home>!$_", value="+1111111112"),
            ContactInfo(info_id="PID3", label="_$!<Work>!$_", value="+1111111113"),
            ContactInfo(info_id="PID4", label="_$!<School>!$_", value="+1111111114"),
        ],
        emails=[
            ContactInfo(info_id="EID1", label="_$!<Home>!$_", value="test@h.com"),
            ContactInfo(info_id="EID2", label="_$!<Work>!$_", value="test@w.com"),
            ContactInfo(info_id="EID3", label="_$!<School>!$_", value="test@s.com"),
        ],
        urls=[
            ContactInfo(info_id="UID1", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(info_id="UID2", label="_$!<Work>!$_", value="http://w.com"),
            ContactInfo(info_id="UID3", label="_$!<School>!$_", value="http://s.com"),
        ],
        addresses=[
            ContactAddress(info_id="AID1", label="_$!<Home>!$_", value="ADDRESS_1"),
            ContactAddress(info_id="AID2", label="_$!<Work>!$_", value="ADDRESS_2"),
            ContactAddress(info_id="AID3", label="_$!<School>!$_", value="ADDRESS_3"),
        ],
        birth_date="February 2, 1922",
        custom_dates=[
            ContactInfo(info_id="DID1", label="favorite", value="DATE"),
        ],
        social_profiles=[
            ContactSocialProfile(info_id="SID1", label="GitHub", value="USER"),
            ContactSocialProfile(info_id="SID2", label="LinkedIn", value="USER"),
        ],
        instant_messages=[
            ContactInfo(info_id="IID1", label="WhatsApp", value="USER"),
            ContactInfo(info_id="IID2", label="Signal", value="USER"),
        ],
        note="NOTE",
    )
    assert contact.problems == []


def test_prefix_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase prefix."""
    contact = Contact(contact_id="ID", name="NAME", prefix="dr.")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Prefix 'dr.' should be 'Dr.'."
    assert sorted(mock_address_book.updates) == [("ID", "prefix", "Dr.")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_first_name_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase first name."""
    contact = Contact(contact_id="ID", name="NAME", first_name="bob")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "First name 'bob' should be 'Bob'."
    assert sorted(mock_address_book.updates) == [("ID", "first_name", "Bob")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_middle_name_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase middle name."""
    contact = Contact(contact_id="ID", name="NAME", middle_name="babála")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Middle name 'babála' should be 'Babála'."
    assert sorted(mock_address_book.updates) == [("ID", "middle_name", "Babála")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_last_name_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase last name."""
    contact = Contact(contact_id="ID", name="NAME", last_name="balon")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Last name 'balon' should be 'Balon'."
    assert sorted(mock_address_book.updates) == [("ID", "last_name", "Balon")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_suffix_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase suffix."""
    contact = Contact(contact_id="ID", name="NAME", suffix="jr.")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Suffix 'jr.' should be 'Jr.'."
    assert sorted(mock_address_book.updates) == [("ID", "suffix", "Jr.")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_job_title_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase job title."""
    contact = Contact(contact_id="ID", name="NAME", job_title="baker")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Job title 'baker' should be 'Baker'."
    assert sorted(mock_address_book.updates) == [("ID", "job_title", "Baker")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_department_capitalization(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test lowercase department."""
    contact = Contact(contact_id="ID", name="NAME", department="bakery")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Department 'bakery' should be 'Bakery'."
    assert sorted(mock_address_book.updates) == [("ID", "department", "Bakery")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_capitalization_ignores_mixed_case() -> None:
    """Test mixed case name."""
    contact = Contact(
        contact_id="ID", name="NAME", first_name="bobMac", last_name="o'Hare."
    )
    assert contact.problems == []


def test_organization_ignores_lowercase_organization() -> None:
    """Test lowercase organization."""
    contact = Contact(contact_id="ID", name="NAME", organization="bakers co.")
    assert contact.problems == []


def test_nickname_single_word(problem_checker: ProblemChecker) -> None:
    """Test single name nickname."""
    contact = Contact(contact_id="ID", name="NAME", nickname="Bob")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Nickname 'Bob' is not a full name."


def test_fixable_phone_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test phone with fixable label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        phones=[
            ContactInfo(info_id="PID", label="mobile", value="+1111111111"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Phone label <mobile> should be <_$!<Mobile>!$_>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "phones", "PID", {"label": "_$!<Mobile>!$_"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_phone_label(problem_checker: ProblemChecker) -> None:
    """Test phone with invalid label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        phones=[
            ContactInfo(info_id="PID", label="pager", value="+1111111111"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Phone label <pager> is not valid."


def test_fixable_email_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test e-mail with fixable label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        emails=[
            ContactInfo(info_id="EID", label="email", value="test@h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "E-mail label <email> should be <_$!<Home>!$_>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "emails", "EID", {"label": "_$!<Home>!$_"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_email_label(problem_checker: ProblemChecker) -> None:
    """Test e-mail with invalid label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        emails=[
            ContactInfo(info_id="EID", label="backup", value="test@h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "E-mail label <backup> is not valid."


def test_fixable_url_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test URL with fixable label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID", label="home", value="http://h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "URL label <home> should be <_$!<HomePage>!$_>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "urls", "UID", {"label": "_$!<HomePage>!$_"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_fixable_url_wrong_home_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test URL with the wrong home page label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID", label="_$!<Home>!$_", value="http://h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "URL label for 'http://h.com' should be <HomePage>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "urls", "UID", {"label": "_$!<HomePage>!$_"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_url_label(problem_checker: ProblemChecker) -> None:
    """Test URL with invalid label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID", label="blog", value="http://h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "URL label <blog> is not valid."


def test_fixable_address_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test address with fixable label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        addresses=[
            ContactAddress(info_id="AID", label="work", value="ADDRESS"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Address label <work> should be <_$!<Work>!$_>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"label": "_$!<Work>!$_"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_address_label(problem_checker: ProblemChecker) -> None:
    """Test address with invalid label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        addresses=[
            ContactAddress(info_id="AID", label="mailbox", value="ADDRESS"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Address label <mailbox> is not valid."


def test_mixed_case_custom_date_label(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test custom date with fixable mixed case label."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        custom_dates=[
            ContactInfo(info_id="DID", label="Favorite", value="DATE"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Custom date label <Favorite> should be <favorite>."
    assert sorted(mock_address_book.updates) == [
        ("ID", "custom_dates", "DID", {"label": "favorite"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_fixable_phone_number(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test phone number with wrong formatting."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        phones=[
            ContactInfo(
                info_id="PID", label="_$!<Work>!$_", value=" +1 (800) WEAREBAKERS"
            )
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert (
        problem.message
        == "Phone number ' +1 (800) WEAREBAKERS' should be '+180093273225377'."
    )
    assert sorted(mock_address_book.updates) == [
        ("ID", "phones", "PID", {"value": "+180093273225377"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_phone_number(problem_checker: ProblemChecker) -> None:
    """Test invalid phone number."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        phones=[
            ContactInfo(
                info_id="PID", label="_$!<Work>!$_", value="+1 (NO) WEARENOTBAKERS"
            )
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Phone number '+1 (NO) WEARENOTBAKERS' is not valid."


def test_fixable_email_address(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test e-mail address with wrong formatting."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        emails=[
            ContactInfo(info_id="EID", label="_$!<Home>!$_", value=" test@H.COM"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "E-mail ' test@H.COM' should be 'test@h.com'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "emails", "EID", {"value": "test@h.com"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_email_address(problem_checker: ProblemChecker) -> None:
    """Test invalid e-mail address."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        emails=[
            ContactInfo(info_id="EID", label="_$!<Home>!$_", value="test@"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "E-mail 'test@' is not valid."


def test_fixable_url(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test URL with wrong formatting."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID", label="_$!<HomePage>!$_", value=" HTTP://h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "URL ' HTTP://h.com' should be 'http://h.com'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "urls", "UID", {"value": "http://h.com"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_unfixable_url(problem_checker: ProblemChecker) -> None:
    """Test invalid URL."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID", label="_$!<HomePage>!$_", value="1.1.1.1"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "URL '1.1.1.1' is not valid."


def test_duplicate_phones(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate phone deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        phones=[
            ContactInfo(info_id="PID1", label="_$!<Mobile>!$_", value="+1111111111"),
            ContactInfo(info_id="PID2", label="_$!<Home>!$_", value="+1111111111"),
            ContactInfo(info_id="PID3", label="_$!<Home>!$_", value="+1111111112"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Phone '+1111111111' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "phones", "PID2")]


def test_duplicate_emails(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate e-mail deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        emails=[
            ContactInfo(info_id="EID1", label="_$!<Home>!$_", value="test@h.com"),
            ContactInfo(info_id="EID2", label="_$!<Work>!$_", value="test@h.com"),
            ContactInfo(info_id="EID3", label="_$!<School>!$_", value="test@s.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "E-mail 'test@h.com' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "emails", "EID2")]


def test_duplicate_urls(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate URL deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        urls=[
            ContactInfo(info_id="UID1", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(info_id="UID2", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(info_id="UID3", label="_$!<HomePage>!$_", value="http://h.net"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "URL 'http://h.com' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "urls", "UID2")]


def test_duplicate_addresses(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate address deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        addresses=[
            ContactAddress(info_id="AID1", label="_$!<Home>!$_", value="ADDRESS"),
            ContactAddress(info_id="AID2", label="_$!<Work>!$_", value="ADDRESS"),
            ContactAddress(info_id="AID3", label="_$!<School>!$_", value="ANOTHER"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Address 'ADDRESS' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "addresses", "AID2")]


def test_duplicate_social_profiles(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate social profile deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        social_profiles=[
            ContactSocialProfile(info_id="SID1", label="GitHub", value="USER"),
            ContactSocialProfile(info_id="SID2", label="GitHub", value="ANOTHER"),
            ContactSocialProfile(info_id="SID3", label="LinkedIn", value="USER"),
            ContactSocialProfile(info_id="SID4", label="LinkedIn", value="USER"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Social profile 'USER <LinkedIn>' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "social_profiles", "SID4")]


def test_duplicate_instant_messages(
    problem_checker: ProblemChecker, mock_address_book: MockAddressBook
) -> None:
    """Test duplicate instant message profile deletion."""
    contact = Contact(
        contact_id="ID",
        name="NAME",
        instant_messages=[
            ContactInfo(info_id="IID1", label="WhatsApp", value="USER"),
            ContactInfo(info_id="IID2", label="Signal", value="USER"),
            ContactInfo(info_id="IID3", label="Signal", value="USER"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Instant message 'USER <Signal>' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "instant_messages", "IID3")]
