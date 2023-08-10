"""Label operations."""


LABEL_TO_CATEGORY = {
    "_$!<Mobile>!$_": "mobile",
    "_$!<Home>!$_": "home",
    "_$!<Main>!$_": "home",
    "_$!<HomePage>!$_": "home",
    "_$!<Work>!$_": "work",
    "_$!<School>!$_": "school",
    "_$!<HomeFAX>!$_": "fax",
    "_$!<WorkFAX>!$_": "fax",
    "_$!<OtherFAX>!$_": "fax",
    "_$!<Pager>!$_": "pager",
    "_$!<Anniversary>!$_": "anniversary",
    "_$!<Other>!$_": "other",
}

CATEGORY_TO_ICON = {
    "name": "🔖",
    "phonetic": "🎧",
    "date": "📅",
    "phone": "📞",
    "email": "📧",
    "url": "🌐",
    "message": "💬",
    "address": "📫",
    "mobile": "📱",
    "home": "🏠",
    "work": "💼",
    "school": "🏫",
    "fax": "📠",
    "pager": "📟",
    "anniversary": "💍",
    "related": "👥",
    "note": "📋",
    "other": "❓",
}


def category_icon(category: str, default_icon: str = "❌") -> str:
    """Return the icon of given category."""
    return CATEGORY_TO_ICON.get(category, default_icon)


def label_icon(label: str, default_category: str = "unkown") -> str:
    """Return the icon of given label."""
    return category_icon(LABEL_TO_CATEGORY.get(label, default_category))
