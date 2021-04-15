import pytest

from icd_extractor.extractor import extract, main

__author__ = "Atiladanvi"
__copyright__ = "Atiladanvi"
__license__ = "MIT"


def test_fib():
    """API Tests"""
    assert extract(1) == 1


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["./icd10cm_codes_2018.txt"])
    captured = capsys.readouterr()
    assert "FILE_PATH: ./icd10cm_codes_2018.txt" in captured.out
