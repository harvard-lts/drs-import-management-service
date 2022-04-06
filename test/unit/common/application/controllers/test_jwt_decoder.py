from datetime import datetime, timedelta
from unittest import TestCase

import jwt
from jwt import DecodeError, InvalidSignatureError

from app.common.application.controllers.jwt_decoder import JwtDecoder


class TestJwtDecoder(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_PRIVATE_JWT_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCcxOCduyFGosFB
a27H9h2G4EEW/4CIvVSbXe4x2S1m3jWRPHCAiwji1dm4KvRcCvi7jKA3B7E+rv1b
f5TX5hIK0Ej1O3ou6BuaI6sW8KXXhLJVez4+vI5VZGEt2jzfvQ7Vwu/LDJ/l6+aI
sISFQ7TBYxL447yKsURsfcE3BIoBrgnWE+OclzS12kKHXBozcZhP9KOJpd7gPSRv
iWMGTzoSYD6UQR6yauYNjlCQioOXMrZ0nSLZv1SJE5kJIq/OrCanvJ650s+5UKkg
JVjOlrK277hc1UIXDhDTyU9+/9R9fgA1TRkeqJknpdvuF8+6ETe4AJmP0Cm3e6lz
tfQ6NMe7AgMBAAECggEAGIOQvBlu8qSwo5IxGIObymN2yinZ54fzmvftL05Oky9c
IQHadb9H/HCEQxA0ddAhZPJweypwxOSIKa6hj8EiQR6gyfgq+vrAljHNpyCqTjEp
0cQbz6Ocfi3cJFdj/XiKwVJiPNYUiteAjQ9NKamUskjTxqeV6/ocQPrJI9lJ20kl
BbvG3xHDuIUQ9XAdCsSQIWCWcodeDZiOgFX3wK+9cyT2I6Mn7OWQiETIIDvp4Rep
CcB8+4d4KviRH6sbutv70U2JOu/ZO1JS0HnOZnPB+uXx5F4vWWOoMegLOrBCdjRd
m80fDx0FPfsv7BeKcmcZ3x+Q5Y5OErzhxZtVH6fZwQKBgQDMvkMGSV25Zj6TCwCc
u3CqsmXWPxNnstEBQe/GVZ0Ef0aJmKK/ZBm85ZLvaCnooNW9w3+IY+qNPIkKe3ci
NkE84y05sFAvMNT9nt+JTchngSYQs2zLPuEApli2n2DzhWzp8vejPcYYTW92xbqg
jG81wX7EBNpl5jdO6LmevgmPJQKBgQDEBALpC3b2weYwuOIfeFz72xd/37XSyCLk
Z6SZ7Q/IY0cKGfZqGJ8qAnp4agZsRg/6dIZaaO4Q+vyQvu0EWnkil1ySMKcYKRGZ
cvfmR2WQluno8/Kp0LTq3hiJnfwTxIlMNnmPjXKuiqn1EDJBHZtOWP6JRjvRx8zv
KiI8bg41XwKBgFLnY6pjAMF2xjWySdAtEeT8kcHcDpZ50KmqslVkC01r3/sNRDEt
bkKPzxyD2BxrK8FILRbkJnCEJ5WIAuhmgaoO7xwh6YYCRuxfbXJifZhzsh8nGBGA
Z4lk0h04kgBpcX2VtXJzLAhhKpY0YGpsEwf4TsU+ldSXEKQyFh9SIfrFAoGAbQu6
PsGFBhOqppJEIbPJLsec1CO1ODTkzGIoPQWX0SgBvknhPvbBnRJR5ak+N3/mpbOr
hqJ3RnUKis/cdZ6LY0YHVsDARH2cb9x4suAnTX/XUyRbbENSUpMJ3Y1JTgn5Q6/O
gqDzGszDbjT7cCQzYSu7Ns0evD7F8ItlDm8/cksCgYBBpoPPLMdciRsADH4yHYS+
yStkDWV1mdjVgrobFZl5ZqGroYADCRqcag7s05ABKdQq4Sy/zjl5GLY4a5Eal/9H
Q3kNZCqHwkGn97UmDo9rvmhXpUI7Lz8WcFMHGvdOipNPmYJNMtZMgJ6fX8xRvJGN
zg9c0ScvQiGL4awjHNvadw==
-----END PRIVATE KEY-----"""

        cls.TEST_PUBLIC_JWT_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnMTgnbshRqLBQWtux/Yd
huBBFv+AiL1Um13uMdktZt41kTxwgIsI4tXZuCr0XAr4u4ygNwexPq79W3+U1+YS
CtBI9Tt6LugbmiOrFvCl14SyVXs+PryOVWRhLdo8370O1cLvywyf5evmiLCEhUO0
wWMS+OO8irFEbH3BNwSKAa4J1hPjnJc0tdpCh1waM3GYT/SjiaXe4D0kb4ljBk86
EmA+lEEesmrmDY5QkIqDlzK2dJ0i2b9UiROZCSKvzqwmp7yeudLPuVCpICVYzpay
tu+4XNVCFw4Q08lPfv/UfX4ANU0ZHqiZJ6Xb7hfPuhE3uACZj9Apt3upc7X0OjTH
uwIDAQAB
-----END PUBLIC KEY-----"""

        cls.TEST_DECODED_MESSAGE = {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=30)
        }

    def setUp(self) -> None:
        self.test_encoded_message = jwt.encode(
            payload=self.TEST_DECODED_MESSAGE,
            key=self.TEST_PRIVATE_JWT_KEY,
            algorithm=JwtDecoder.ENCODING_ALGORITHM,
            headers={
                "alg": JwtDecoder.ENCODING_ALGORITHM,
                "typ": "JWT",
                "iss": "test_issuer"
            }
        )

    # TODO
    # def test_decode_happy_path(self) -> None:
    #     sut = JwtDecoder(self.TEST_PUBLIC_JWT_KEY)
    #
    #     actual = sut.decode(self.test_encoded_message)
    #     expected = self.TEST_DECODED_MESSAGE
    #
    #     self.assertEqual(actual, expected)

    def test_decode_invalid_signature(self) -> None:
        sut = JwtDecoder(self.TEST_PUBLIC_JWT_KEY.replace("6", "5"))

        with self.assertRaises(InvalidSignatureError):
            sut.decode(self.test_encoded_message)

    def test_decode_wrong_encoded_message(self) -> None:
        sut = JwtDecoder(self.TEST_PUBLIC_JWT_KEY)

        with self.assertRaises(DecodeError):
            sut.decode("wrong_encoded_message")
