from main import validate_response, is_valid_filename, validate_sc


def test_validate_response():
    assert validate_response("") == False
    assert validate_response("Hello there") == True


def test_validate_sc_fail():
    assert validate_sc("A") == False
    assert validate_sc("B") == False


def test_validate_sc_pass():
    assert validate_sc("S") == True
    assert validate_sc("C") == True


def test_is_valid_filename_fail():
    assert is_valid_filename("a1@@!_") == False
    assert is_valid_filename("my.file.txt") == False


def test_is_valid_filename_pass():
    assert is_valid_filename("some_file_name") == True
    assert is_valid_filename("SomeFileName1") == True
