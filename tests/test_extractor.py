from pathlib import Path
from icd_extractor.extractor import extract, main

__author__ = "Atiladanvi"
__copyright__ = "Atiladanvi"
__license__ = "MIT"


def test_extract():
    """API Tests"""
    file = '/tests/icd10cm_codes_test.txt'
    root = Path().absolute().__str__()

    assert extract(root + file) == root + '/storage/icd10cm_codes_test.json'


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["./icd10cm_codes_test.txt"])
    captured = capsys.readouterr()
    assert "FILE_PATH: ./icd10cm_codes_test.txt" in captured.out
