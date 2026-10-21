import re
from collections import defaultdict

# Regular expression for valid email addresses
EMAIL_PATTERN = re.compile(
    r'(?<![\w.+-])'
    r'([A-Za-z0-9+._-]+@'
    r'[A-Za-z0-9.-]+\.(?:com|edu|org))'
    r'(?![\w.-])',
    re.IGNORECASE
)


def extract_emails(file_path):
    domain_emails = defaultdict(set)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                matches = EMAIL_PATTERN.findall(line)

                for email in matches:
                    email = email.lower()
                    domain = email.split("@")[1]

                    domain_emails[domain].add(email)

    except FileNotFoundError:
        print("ERROR: File not found.")
        return

    except OSError as error:
        print("ERROR:", error)
        return

    # Print domains in lexicographical order
    for domain in sorted(domain_emails):
        emails = domain_emails[domain]

        smallest_email = min(emails)

        print(
            domain,
            len(emails),
            smallest_email
        )


def main():
    file_path = input("Enter text file path: ").strip()

    if not file_path:
        print("ERROR: File path cannot be empty.")
        return

    extract_emails(file_path)


if __name__ == "__main__":
    main()