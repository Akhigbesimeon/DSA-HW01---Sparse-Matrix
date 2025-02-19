from sparse_matrix import SparseMatrix
import os

def execute_operation():
    import sys

    # path to the sample inputs folder
    sample_inputs_folder = 'sparse_matrix/sample_input'

    # Check if the folder exists
    if not os.path.exists(sample_inputs_folder):
        print(f"Error: The folder '{sample_inputs_folder}' does not exist.")
        sys.exit(1)

    # list all the files 
    matrix_files = [f for f in os.listdir(sample_inputs_folder) if f.endswith('.txt')]
    if len(matrix_files) < 2:
        print("Error: At least two matrix files are required in the 'sample_inputs' folder.")
        sys.exit(1)

    # display available files
    print("\nAvailable matrix files:")
    for index, file_name in enumerate(matrix_files, start=1):
        print(f"{index}. {file_name}")

    # Ask user to select two files
    try:
        file_num_1 = int(input("\nEnter the number for the first matrix file: "))
        file_num_2 = int(input("Enter the number for the second matrix file: "))

        # Validate user input
        if file_num_1 < 1 or file_num_1 > len(matrix_files) or file_num_2 < 1 or file_num_2 > len(matrix_files):
            print("Error: Invalid file selection. Please choose numbers from the list.")
            sys.exit(1)

        # Get the file 
        file_path_1 = os.path.join(sample_inputs_folder, matrix_files[file_num_1 - 1])
        file_path_2 = os.path.join(sample_inputs_folder, matrix_files[file_num_2 - 1])

    except ValueError:
        print("Error: Invalid input. Please enter numbers only.")
        sys.exit(1)

    # Ask the user for the operation
    operation = input("\nWhat operation would you like to perform? (Add, Subtract, Multiply): ").strip().lower()

    # Load the matrices
    try:
        print("\nLoading matrices...")
        matrix_a = SparseMatrix(file_path=file_path_1)
        matrix_b = SparseMatrix(file_path=file_path_2)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while loading matrices: {e}")
        sys.exit(1)

    # Display matrix dimensions for clarity
    print(f"\nMatrix A dimensions: {matrix_a.get_dimensions()}")
    print(f"Matrix B dimensions: {matrix_b.get_dimensions()}")

    # Validate matrix dimensions for the chosen operation
    if operation in ["add", "subtract"] and matrix_a.get_dimensions() != matrix_b.get_dimensions():
        print("Error: Both matrices must have the same dimensions for addition or subtraction.")
        sys.exit(1)
    elif operation == "multiply" and matrix_a.get_dimensions()[1] != matrix_b.get_dimensions()[0]:
        print("Error: The number of columns in Matrix A must match the number of rows in Matrix B for multiplication.")
        sys.exit(1)

    # Perform the operation
    result_matrix = None
    try:
        if operation == "add":
            result_matrix = matrix_a.add(matrix_b)
        elif operation == "subtract":
            result_matrix = matrix_a.subtract(matrix_b)
        elif operation == "multiply":
            result_matrix = matrix_a.multiply(matrix_b)
        else:
            print("Error: Invalid operation. Please choose 'Add', 'Subtract', or 'Multiply'.")
            sys.exit(1)

        # Display the result in the specified format
        if result_matrix:
            print("\nOperation Result:")
            result_matrix.display()
        else:
            print("Error: The operation could not be completed.")

    except Exception as e:
        print(f"An unexpected error occurred during the operation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    execute_operation()