from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file 
from functions.run_python_file import run_python_file  
def main():
# get_files_info tests
    print("Result for current directory:")
    print("" + get_files_info("calculator", "."))

    print("\nResult for 'pkg' directory:")
    print("" + get_files_info("calculator", "pkg"))

    print("\nResult for '/bin' directory:")
    print("" + get_files_info("calculator", "/bin"))

    print("\nResult for '../' directory:")
    print("" + get_files_info("calculator", "../"))


# get_file_content tests
    # print("Result for get_file_content('calculator', 'lorem.txt')")
    # print(get_file_content("calculator", "lorem.txt"))


    # print("Result for get_file_content('calculator', 'main.py')")
    # print(get_file_content("calculator", "main.py"))

    # print("Result for get_file_content('calculator', 'pkg.calculator.py')")
    # print(get_file_content("calculator", "pkg/calculator.py"))

    # print("Result for get_file_content('calculator', '/bin/cat')")
    # print(get_file_content("calculator", "/bin/cat"))

    # print("Result for get_file_content('calculator', 'pkg/does_not_exist.py')")
    # print(get_file_content("calculator", "pkg/does_not_exist.py"))

# write_file tests
    # print("Result for 'calculator', 'lorem.txt', 'wait, this isn't lorem ipsum'")
    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)

    # print("Result for 'calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet'")
    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)
    
    # print("Result for 'calculator', '/tmp/temp.txt', 'this should not be allowed")
    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # )print(result)

# run_python_file tests
    # print('Result for run_python_file("calculator", "main.py")')
    # result = run_python_file("calculator", "main.py")
    # print(result)

    # print('Result for run_python_file("calculator", "main.py", ["3+5"])')
    # result = run_python_file("calculator", "main.py", ['3+5'])
    # print(result)

    # print('run_python_file("calculator", "tests.py")')
    # result = run_python_file("calculator", "tests.py")
    # print(result)

    # print('Result for run_python_file("calculator", "../main.py")')
    # result = run_python_file("calculator", "../main.py")
    # print(result)

    # print('run_python_file("calculator", "nonexistent.py")')
    # result = run_python_file("calculator", "nonexistent.py")
    # print(result)

if __name__ == "__main__":
    main()
