from functions.get_files_info import get_files_info

def test_calculator_path():
    result = get_files_info("calculator", ".")
    print(result)

def test_pkg_path():
    result = get_files_info("calculator", "pkg")
    print(result)

def test_bin_path():
    result = get_files_info("calculator", "/bin")
    print(result)

def test_parent_path():
    result = get_files_info("calculator", "../")
    print(result)

test_calculator_path()
test_pkg_path()
test_bin_path()
test_parent_path()