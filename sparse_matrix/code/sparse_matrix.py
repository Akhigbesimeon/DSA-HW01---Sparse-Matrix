class SparseMatrix:
    def __init__(self, file_path=None):
        """
        Initialize a sparse matrix.
        """
        if file_path:
            self.data, self.dimensions = self._read_matrix_file(file_path)
            print(f"Successfully loaded matrix from {file_path} with dimensions {self.dimensions}")
        else:
            self.data = {}  # Dictionary to store non-zero elements
            self.dimensions = (0, 0)  

    def _read_matrix_file(self, file_path):
        """
       Load a sparse matrix from a file and get its size and data
        """
        matrix_data = {}
        rows, cols = 0, 0

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.startswith('rows='):
                        rows = int(line.split('=')[1])
                    elif line.startswith('cols='):
                        cols = int(line.split('=')[1])
                    elif line and not line.startswith('#') and '=' not in line:
                        try:
                            # Parse (row, col, value) from the line
                            row, col, value = map(int, line.strip('()').split(','))
                            matrix_data[(row, col)] = value
                        except ValueError as e:
                            raise ValueError(f"Invalid data in file: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

        return matrix_data, (rows, cols)

    def get_dimensions(self):
        """
        Get the matrix size as a tuple.
        """
        return self.dimensions

    def add(self, other_matrix):
        """
        Add another sparse matrix and return the result as a new one.
        """
        if self.dimensions != other_matrix.dimensions:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = SparseMatrix()
        result.dimensions = self.dimensions
        result.data = self.data.copy()

        # Add elements from the other matrix
        for (row, col), value in other_matrix.data.items():
            result.data[(row, col)] = result.data.get((row, col), 0) + value

        return result

    def subtract(self, other_matrix):
        """
        Subtract another sparse matrix and return the result as a new one.
        """
        if self.dimensions != other_matrix.dimensions:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result = SparseMatrix()
        result.dimensions = self.dimensions
        result.data = self.data.copy()

        # Subtract elements from the other matrix
        for (row, col), value in other_matrix.data.items():
            result.data[(row, col)] = result.data.get((row, col), 0) - value

        return result

    def multiply(self, other_matrix):
        """
        Multiply with another sparse matrix and return the result.
        """
        if self.dimensions[1] != other_matrix.dimensions[0]:
            raise ValueError("Matrices cannot be multiplied due to incompatible dimensions.")

        result = SparseMatrix()
        result.dimensions = (self.dimensions[0], other_matrix.dimensions[1])
        result.data = {}

        # Perform matrix multiplication
        for (i, k), val1 in self.data.items():
            for (j, l), val2 in other_matrix.data.items():
                if k == j:  # Column of first matrix matches row of second matrix
                    result.data[(i, l)] = result.data.get((i, l), 0) + val1 * val2

        return result

    def display(self):
        """
        Print the matrix
        """
        rows, cols = self.dimensions
        print(f"rows={rows}")
        print(f"cols={cols}")
        for (row, col), value in sorted(self.data.items()):
            print(f"({row}, {col}, {value})")