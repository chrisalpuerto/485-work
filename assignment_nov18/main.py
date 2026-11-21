# Edit distance programming assignment.
# Requires Python 3; no third-party packages or compilation are needed. From
# this directory, run `python3 main.py` and enter two words when prompted.
# To test the example in the assignment, enter `evaluation` and `elution`;
# the program should report an edit distance of 3.


def build_matrix(word1, word2):
    
    rows = len(word1) + 1
    cols = len(word2) + 1
    matrix = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        matrix[row][0] = row
    for col in range(cols):
        matrix[0][col] = col

    for row in range(1, rows):
        for col in range(1, cols):
            replacement_cost = 0 if word1[row - 1] == word2[col - 1] else 1
            matrix[row][col] = min(
                matrix[row - 1][col] + 1,  # Delete from word1.
                matrix[row][col - 1] + 1,  # Insert into word1.
                matrix[row - 1][col - 1] + replacement_cost,
            )

    return matrix


def find_alignment(word1, word2, matrix):
    
    top = []
    bottom = []
    row = len(word1)
    col = len(word2)

    while row > 0 or col > 0:
        if row > 0 and col > 0:
            replacement_cost = 0 if word1[row - 1] == word2[col - 1] else 1
            if matrix[row][col] == matrix[row - 1][col - 1] + replacement_cost:
                top.append(word1[row - 1])
                bottom.append(word2[col - 1])
                row -= 1
                col -= 1
                continue

        if row > 0 and matrix[row][col] == matrix[row - 1][col] + 1:
            top.append(word1[row - 1])
            bottom.append("_")
            row -= 1
        else:
            top.append("_")
            bottom.append(word2[col - 1])
            col -= 1

    return "".join(reversed(top)), "".join(reversed(bottom))


def print_matrix(word1, word2, matrix):
    """Print each prefix distance with its letter labels."""
    width = max(3, len(str(max(len(word1), len(word2)))))
    print(" " * (width + 1) + " ".join(f"{letter:>{width}}" for letter in "-" + word2))
    for row, values in enumerate(matrix):
        label = "-" if row == 0 else word1[row - 1]
        print(f"{label:>{width}} " + " ".join(f"{value:>{width}}" for value in values))


def main():
    print("WELCOME TO EDIT DISTANCE DEMONSTRATION")
    word1 = input("The first word: ").strip()
    word2 = input("The second word: ").strip()

    matrix = build_matrix(word1, word2)
    aligned_word1, aligned_word2 = find_alignment(word1, word2, matrix)

    print("\nDistance matrix (rows: first word; columns: second word):")
    print_matrix(word1, word2, matrix)
    print(f"\nEdit distance: {matrix[-1][-1]}")
    print("Alignment:")
    print(aligned_word1)
    print(aligned_word2)


if __name__ == "__main__":
    main()
