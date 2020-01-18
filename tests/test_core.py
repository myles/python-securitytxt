TEST_SECURITY_TXT = """# If you would like to report a security issue
# you may report it to us on HackerOne.
Contact: https://hackerone.com/ed
Encryption: https://keybase.pub/edoverflow/pgp_key.asc
Acknowledgements: https://hackerone.com/ed/thanks
"""


def test_parse():
    from securitytxt import SecurityTxt

    s_txt = SecurityTxt(raw=TEST_SECURITY_TXT)
    s_txt.parse()

    assert s_txt.contact == ["https://hackerone.com/ed"]
    assert s_txt.encryption == ["https://keybase.pub/edoverflow/pgp_key.asc"]
    assert s_txt.acknowledgements == ["https://hackerone.com/ed/thanks"]
