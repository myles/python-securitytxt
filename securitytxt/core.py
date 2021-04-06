from urllib.parse import urlparse

import requests


class EmptyFileException(Exception):
    pass


class DoesNotContainContactException(Exception):
    pass


class SecurityTxt:
    FIELD_CONTACT = "contact"
    FIELD_ENCRYPTION = "encryption"
    FIELD_ACKNOWLEDGMENTS = "acknowledgments"

    FIELD_CHOICES = [FIELD_CONTACT, FIELD_ENCRYPTION, FIELD_ACKNOWLEDGMENTS]

    def __init__(self, raw):
        self.raw = raw

        self.fields = {
            self.FIELD_CONTACT: [],
            self.FIELD_ENCRYPTION: [],
            self.FIELD_ACKNOWLEDGMENTS: [],
        }

        self.comments = []

    @property
    def contact(self):
        return self.fields[self.FIELD_CONTACT]

    @property
    def encryption(self):
        return self.fields[self.FIELD_ENCRYPTION]

    @property
    def acknowledgments(self):
        return self.fields[self.FIELD_ACKNOWLEDGMENTS]

    def parse(self):
        if isinstance(self.raw, bytes):
            self.raw = self.raw.decode("utf-8")

        lines = self.raw.split("\n")

        if not lines:
            raise EmptyFileException

        for line in lines:
            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Comment
            if line.startswith("#"):
                self.comments.append(line.replace("#", "").strip())
                continue

            if ":" not in line:
                continue

            field, value = line.split(":", 1)
            value = value.strip()

            if field.lower() in self.FIELD_CHOICES:
                self.fields[field.lower()].append(value)

        if not self.fields["contact"]:
            raise DoesNotContainContactException

    @classmethod
    def parse_file(cls, file_path):
        with open(file_path) as fobj:
            content = fobj.read()

        s_txt = cls(content)
        s_txt.parse()

        return s_txt

    @classmethod
    def parse_url(cls, url):
        if not url.endswith("/.well-known/security.txt"):
            url_parsed = urlparse(url)
            url = "{}://{}/.well-known/security.txt".format(
                url_parsed.scheme, url_parsed.netloc
            )

        resp = requests.get(url)

        if not resp.ok:
            raise resp.excpetion

        s_txt = cls(resp.content)
        s_txt.parse()

        return s_txt
