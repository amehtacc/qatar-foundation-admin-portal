import re

VALID_CATEGORIES = [
    "Technology",
    "Business",
    "Design",
    "Marketing",
    "Data Science",
    "Other"
]

EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


def validate_email(email):

    return re.match(EMAIL_REGEX, email)