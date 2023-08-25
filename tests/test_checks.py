"""Unit tests for contact checks."""

import pytest

from contacts.address import AddressFormat, Geocode, SemanticAddressField
from contacts.category import Category
from contacts.config import Config
from contacts.contact import Contact, ContactAddress, ContactInfo, ContactSocialProfile
from contacts.problem import Problem
from tests.mocks import MockAddressBook, MockGeocoder


class ProblemChecker:
    """Checker that verifies problem details."""

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


@pytest.fixture(autouse=True)
def problem_checker(mock_address_book: MockAddressBook) -> ProblemChecker:
    """Fixture for prefs."""
    return ProblemChecker(mock_address_book)


def test_correct_contact() -> None:
    """Test contact with no problems."""
    contact = Contact(
        id="ID",
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
            ContactInfo(id="PID1", label="_$!<Mobile>!$_", value="+1111111111"),
            ContactInfo(id="PID2", label="_$!<Home>!$_", value="+1111111112"),
            ContactInfo(id="PID3", label="_$!<Work>!$_", value="+1111111113"),
            ContactInfo(id="PID4", label="_$!<School>!$_", value="+1111111114"),
        ],
        emails=[
            ContactInfo(id="EID1", label="_$!<Home>!$_", value="test@h.com"),
            ContactInfo(id="EID2", label="_$!<Work>!$_", value="test@w.com"),
            ContactInfo(id="EID3", label="_$!<School>!$_", value="test@s.com"),
        ],
        urls=[
            ContactInfo(id="UID1", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(id="UID2", label="_$!<Work>!$_", value="http://w.com"),
            ContactInfo(id="UID3", label="_$!<School>!$_", value="http://s.com"),
        ],
        addresses=[
            ContactAddress(
                id="AID1",
                label="_$!<Home>!$_",
                value="ADDRESS_1",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
            ContactAddress(
                id="AID2",
                label="_$!<Work>!$_",
                value="ADDRESS_2",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
            ContactAddress(
                id="AID3",
                label="_$!<School>!$_",
                value="ADDRESS_3",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
        birth_date="February 2, 1922",
        custom_dates=[
            ContactInfo(id="DID1", label="favorite", value="DATE"),
        ],
        social_profiles=[
            ContactSocialProfile(id="SID1", label="GitHub", value="USER"),
            ContactSocialProfile(id="SID2", label="LinkedIn", value="USER"),
        ],
        instant_messages=[
            ContactInfo(id="IID1", label="WhatsApp", value="USER"),
            ContactInfo(id="IID2", label="Signal", value="USER"),
        ],
        note="NOTE",
    )
    assert contact.problems == []


def test_prefix_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase prefix."""
    contact = Contact(id="ID", name="NAME", prefix="dr.")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Prefix 'dr.' should be 'Dr.'."
    assert sorted(mock_address_book.updates) == [("ID", "prefix", "Dr.")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_first_name_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase first name."""
    contact = Contact(id="ID", name="NAME", first_name="bob")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "First name 'bob' should be 'Bob'."
    assert sorted(mock_address_book.updates) == [("ID", "first_name", "Bob")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_middle_name_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase middle name."""
    contact = Contact(id="ID", name="NAME", middle_name="babála")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Middle name 'babála' should be 'Babála'."
    assert sorted(mock_address_book.updates) == [("ID", "middle_name", "Babála")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_last_name_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase last name."""
    contact = Contact(id="ID", name="NAME", last_name="balon")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Last name 'balon' should be 'Balon'."
    assert sorted(mock_address_book.updates) == [("ID", "last_name", "Balon")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_suffix_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase suffix."""
    contact = Contact(id="ID", name="NAME", suffix="jr.")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Suffix 'jr.' should be 'Jr.'."
    assert sorted(mock_address_book.updates) == [("ID", "suffix", "Jr.")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_job_title_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase job title."""
    contact = Contact(id="ID", name="NAME", job_title="baker")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Job title 'baker' should be 'Baker'."
    assert sorted(mock_address_book.updates) == [("ID", "job_title", "Baker")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_department_casing_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test lowercase department."""
    contact = Contact(id="ID", name="NAME", department="bakery")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Department 'bakery' should be 'Bakery'."
    assert sorted(mock_address_book.updates) == [("ID", "department", "Bakery")]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_names_ignore_mixed_case() -> None:
    """Test mixed case name."""
    contact = Contact(id="ID", name="NAME", first_name="bobMac", last_name="o'Hare.")
    assert contact.problems == []


def test_organization_ignores_lowercase() -> None:
    """Test lowercase organization."""
    contact = Contact(id="ID", name="NAME", organization="bakers co.")
    assert contact.problems == []


def test_nickname_invalid_single_word(problem_checker: ProblemChecker) -> None:
    """Test single word nickname."""
    contact = Contact(id="ID", name="NAME", nickname="Bob")
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Nickname 'Bob' is not a full name."


def test_phone_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test mislabeled phone."""
    contact = Contact(
        id="ID",
        name="NAME",
        phones=[
            ContactInfo(id="PID", label="mobile", value="+1111111111"),
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


def test_phone_invalid_label(problem_checker: ProblemChecker) -> None:
    """Test phone with invalid label."""
    contact = Contact(
        id="ID",
        name="NAME",
        phones=[
            ContactInfo(id="PID", label="pager", value="+1111111111"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Phone label <pager> is not valid."


def test_phone_format_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test phone number in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        phones=[
            ContactInfo(id="PID", label="_$!<Work>!$_", value=" +1 (800) WEAREBAKERS")
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


def test_phone_invalid_number(problem_checker: ProblemChecker) -> None:
    """Test invalid phone number."""
    contact = Contact(
        id="ID",
        name="NAME",
        phones=[
            ContactInfo(id="PID", label="_$!<Work>!$_", value="+1 (NO) WEARENOTBAKERS")
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Phone number '+1 (NO) WEARENOTBAKERS' is not valid."


def test_phone_duplicate_numbers(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate phone numbers."""
    contact = Contact(
        id="ID",
        name="NAME",
        phones=[
            ContactInfo(id="PID1", label="_$!<Mobile>!$_", value="+1111111111"),
            ContactInfo(id="PID2", label="_$!<Home>!$_", value="+1111111111"),
            ContactInfo(id="PID3", label="_$!<Home>!$_", value="+1111111112"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Phone '+1111111111' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "phones", "PID2")]


def test_email_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test mislabeled e-mail."""
    contact = Contact(
        id="ID",
        name="NAME",
        emails=[
            ContactInfo(id="EID", label="email", value="test@h.com"),
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


def test_email_invalid_label(problem_checker: ProblemChecker) -> None:
    """Test e-mail with invalid label."""
    contact = Contact(
        id="ID",
        name="NAME",
        emails=[
            ContactInfo(id="EID", label="backup", value="test@h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "E-mail label <backup> is not valid."


def test_email_format_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test e-mail address in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        emails=[
            ContactInfo(id="EID", label="_$!<Home>!$_", value=" test@H.COM"),
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


def test_email_invalid_address(problem_checker: ProblemChecker) -> None:
    """Test invalid e-mail address."""
    contact = Contact(
        id="ID",
        name="NAME",
        emails=[
            ContactInfo(id="EID", label="_$!<Home>!$_", value="test@"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "E-mail 'test@' is not valid."


def test_email_duplicate_addresses(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate e-mail addresses."""
    contact = Contact(
        id="ID",
        name="NAME",
        emails=[
            ContactInfo(id="EID1", label="_$!<Home>!$_", value="test@h.com"),
            ContactInfo(id="EID2", label="_$!<Work>!$_", value="test@h.com"),
            ContactInfo(id="EID3", label="_$!<School>!$_", value="test@s.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "E-mail 'test@h.com' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "emails", "EID2")]


def test_url_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test mislabeled URL."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID", label="home", value="http://h.com"),
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


def test_url_wrong_home_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test URL with the wrong home page label."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID", label="_$!<Home>!$_", value="http://h.com"),
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


def test_url_invalid_label(problem_checker: ProblemChecker) -> None:
    """Test URL with invalid label."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID", label="blog", value="http://h.com"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "URL label <blog> is not valid."


def test_url_format_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test URL in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID", label="_$!<HomePage>!$_", value=" HTTP://h.com"),
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


def test_url_invalid_value(problem_checker: ProblemChecker) -> None:
    """Test invalid URL."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID", label="_$!<HomePage>!$_", value="1.1.1.1"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "URL '1.1.1.1' is not valid."


def test_url_duplicate_values(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate URLs."""
    contact = Contact(
        id="ID",
        name="NAME",
        urls=[
            ContactInfo(id="UID1", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(id="UID2", label="_$!<HomePage>!$_", value="http://h.com"),
            ContactInfo(id="UID3", label="_$!<HomePage>!$_", value="http://h.net"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "URL 'http://h.com' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "urls", "UID2")]


def test_address_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test mislabeled address."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="work",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
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


def test_address_invalid_label(problem_checker: ProblemChecker) -> None:
    """Test address with invalid label."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="mailbox",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Address label <mailbox> is not valid."


def test_address_street_geocoding_error(
    mock_geocoder: MockGeocoder,
    problem_checker: ProblemChecker,
) -> None:
    """Test address not geocoding."""
    mock_geocoder.error()
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Address 'ADDRESS' cannot be geocoded."


def test_address_missing_street(problem_checker: ProblemChecker) -> None:
    """Test address with missing street."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Street for 'ADDRESS' is missing."


def test_address_street_not_in_format(
    mock_config: Config,
    mock_address_book: MockAddressBook,
    problem_checker: ProblemChecker,
) -> None:
    """Test address with a street in format that does not have streets."""
    mock_config.address_formats = {
        "us": AddressFormat(
            city=SemanticAddressField.CITY,
            state=SemanticAddressField.STATE,
            zip_code=SemanticAddressField.ZIP_CODE,
        )
    }
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Street '1 Street' should be removed."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"street": ""})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_street_geocode_fix(
    mock_address_book: MockAddressBook,
    mock_geocoder: MockGeocoder,
    problem_checker: ProblemChecker,
) -> None:
    """Test address city fixed by geocoding."""
    mock_geocoder.provide(
        Geocode(
            street="1 Street",
            city="Eureka",
            state="CA",
            zip_code="95501",
            country_code="us",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="Street No 1\n#1",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Street 'Street No 1 #1' should be '1 Street #1'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"street": "1 Street\n#1"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_missing_city(problem_checker: ProblemChecker) -> None:
    """Test address with missing city."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "City for 'ADDRESS' is missing."


def test_address_city_not_in_format(
    mock_config: Config,
    mock_address_book: MockAddressBook,
    problem_checker: ProblemChecker,
) -> None:
    """Test address with a city in format that does not have cities."""
    mock_config.address_formats = {
        "us": AddressFormat(
            street=SemanticAddressField.STREET,
            state=SemanticAddressField.STATE,
            zip_code=SemanticAddressField.ZIP_CODE,
        )
    }
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "City 'Eureka' should be removed."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"city": ""})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_city_geocode_fix(
    mock_address_book: MockAddressBook,
    mock_geocoder: MockGeocoder,
    problem_checker: ProblemChecker,
) -> None:
    """Test address city fixed by geocoding."""
    mock_geocoder.provide(
        Geocode(
            street="1 Street",
            city="Eureka",
            state="CA",
            zip_code="95501",
            country_code="us",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eurek",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "City 'Eurek' should be 'Eureka'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"city": "Eureka"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_state_not_in_format(
    mock_config: Config,
    mock_address_book: MockAddressBook,
    problem_checker: ProblemChecker,
) -> None:
    """Test address with a state in format that does not have states."""
    mock_config.address_formats = {
        "us": AddressFormat(
            street=SemanticAddressField.STREET,
            city=SemanticAddressField.CITY,
            zip_code=SemanticAddressField.ZIP_CODE,
        )
    }
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "State 'CA' should be removed."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"state": ""})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_state_geocode_fix(
    mock_address_book: MockAddressBook,
    mock_geocoder: MockGeocoder,
    problem_checker: ProblemChecker,
) -> None:
    """Test address state fixed by geocoding."""
    mock_geocoder.provide(
        Geocode(
            street="1 Street",
            city="Eureka",
            state="CA",
            zip_code="95501",
            country_code="us",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="California",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "State 'California' should be 'CA'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"state": "CA"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_missing_zip_code(problem_checker: ProblemChecker) -> None:
    """Test address with missing zip code."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "ZIP code for 'ADDRESS' is missing."


def test_address_zip_code_not_in_format(
    mock_config: Config,
    mock_address_book: MockAddressBook,
    problem_checker: ProblemChecker,
) -> None:
    """Test address with a zip code in format that does not have zip codes."""
    mock_config.address_formats = {
        "us": AddressFormat(
            street=SemanticAddressField.STREET,
            city=SemanticAddressField.CITY,
            state=SemanticAddressField.STATE,
        )
    }
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "ZIP code '95501' should be removed."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"zip_code": ""})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_zip_code_geocode_fix(
    mock_address_book: MockAddressBook,
    mock_geocoder: MockGeocoder,
    problem_checker: ProblemChecker,
) -> None:
    """Test address zip code fixed by geocoding."""
    mock_geocoder.provide(
        Geocode(
            street="1 Street",
            city="Eureka",
            state="CA",
            zip_code="95501-1001",
            country_code="us",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "ZIP code '95501' should be '95501-1001'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"zip_code": "95501-1001"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_missing_country(problem_checker: ProblemChecker) -> None:
    """Test address with missing country."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.ERROR
    assert problem.message == "Country for 'ADDRESS' is missing."


def test_address_country_from_country_code_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test address with country in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Country for 'ADDRESS' should be 'United States'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"country": "United States"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_wrong_country_for_country_code_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test address with country in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="Canada",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Country 'Canada' should be 'United States'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"country": "United States"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_country_code_format_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test address with country code in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="US",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Country code 'US' should be 'us'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"country_code": "us"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_country_code_from_country_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test address with country in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Country code for 'ADDRESS' should be 'us'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"country_code": "us"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_country_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test address with country in wrong format."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="USA",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Country 'USA' should be 'United States'."
    assert sorted(mock_address_book.updates) == [
        ("ID", "addresses", "AID", {"country": "United States"})
    ]
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == []


def test_address_correct_custom_format(
    mock_config: Config,
    mock_geocoder: MockGeocoder,
) -> None:
    """Test address in correct custom format."""
    mock_config.address_formats = {
        "tr": AddressFormat(
            street=SemanticAddressField.STREET,
            state=SemanticAddressField.CITY,
            city=SemanticAddressField.COUNTY,
            zip_code=SemanticAddressField.ZIP_CODE,
        )
    }
    mock_geocoder.provide(
        Geocode(
            street="1. Cadde",
            neighborhood="Bahçelievler",
            city="Çankaya",
            county="Ankara",
            zip_code="06490",
            country_code="tr",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1. Cadde\nNo: 1",
                city="Ankara",
                state="Çankaya",
                zip_code="06490",
                country="Türkiye",
                country_code="tr",
            ),
        ],
    )
    assert contact.problems == []


def test_address_fix_from_custom_format(
    mock_config: Config,
    mock_address_book: MockAddressBook,
    mock_geocoder: MockGeocoder,
) -> None:
    """Test address in correct custom format."""
    mock_config.address_formats = {
        "tr": AddressFormat(
            street=SemanticAddressField.STREET,
            state=SemanticAddressField.CITY,
            city=SemanticAddressField.COUNTY,
            zip_code=SemanticAddressField.ZIP_CODE,
        )
    }
    mock_geocoder.provide(
        Geocode(
            street="1. Cadde",
            neighborhood="Bahçelievler",
            city="Çankaya",
            county="Ankara",
            zip_code="06490",
            country_code="tr",
        )
    )
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1. Cadde\nNo: 1",
                state="Ankara",
                city="Çankaya",
                zip_code="06490",
                country="Türkiye",
                country_code="tr",
            ),
        ],
    )
    assert len(contact.problems) == 2
    assert sorted(problem.message for problem in contact.problems) == [
        "City 'Çankaya' should be 'Ankara'.",
        "State 'Ankara' should be 'Çankaya'.",
    ]


def test_addresses_duplicate_values(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate addresses."""
    contact = Contact(
        id="ID",
        name="NAME",
        addresses=[
            ContactAddress(
                id="AID1",
                label="_$!<Home>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
            ContactAddress(
                id="AID2",
                label="_$!<Work>!$_",
                value="ADDRESS",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
            ContactAddress(
                id="AID3",
                label="_$!<School>!$_",
                value="ANOTHER",
                street="1 Street",
                city="Eureka",
                state="CA",
                zip_code="95501",
                country="United States",
                country_code="us",
            ),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Address 'ADDRESS' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "addresses", "AID2")]


def test_custom_date_mixed_case_label_fix(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test custom date with mixed case label."""
    contact = Contact(
        id="ID",
        name="NAME",
        custom_dates=[
            ContactInfo(id="DID", label="Favorite", value="DATE"),
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


def test_custom_date_duplicate_values(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate custom dates."""
    contact = Contact(
        id="ID",
        name="NAME",
        custom_dates=[
            ContactInfo(id="DID1", label="favorite", value="DATE"),
            ContactInfo(id="DID2", label="favorite", value="DATE"),
            ContactInfo(id="DID2", label="something else", value="DATE"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Custom date 'DATE <favorite>' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "custom_dates", "DID2")]


def test_social_profile_duplicate_values(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate social profiles."""
    contact = Contact(
        id="ID",
        name="NAME",
        social_profiles=[
            ContactSocialProfile(id="SID1", label="GitHub", value="USER"),
            ContactSocialProfile(id="SID2", label="GitHub", value="ANOTHER"),
            ContactSocialProfile(id="SID3", label="LinkedIn", value="USER"),
            ContactSocialProfile(id="SID4", label="LinkedIn", value="USER"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Social profile 'USER <LinkedIn>' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "social_profiles", "SID4")]


def test_instant_message_duplicate_values(
    mock_address_book: MockAddressBook, problem_checker: ProblemChecker
) -> None:
    """Test duplicate instant messages."""
    contact = Contact(
        id="ID",
        name="NAME",
        instant_messages=[
            ContactInfo(id="IID1", label="WhatsApp", value="USER"),
            ContactInfo(id="IID2", label="Signal", value="USER"),
            ContactInfo(id="IID3", label="Signal", value="USER"),
        ],
    )
    problem = problem_checker.problem(contact)
    assert problem.category == Category.WARNING
    assert problem.message == "Instant message 'USER <Signal>' has duplicate(s)."
    assert sorted(mock_address_book.updates) == []
    assert sorted(mock_address_book.adds) == []
    assert sorted(mock_address_book.deletes) == [("ID", "instant_messages", "IID3")]
