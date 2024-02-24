#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>

#define UNASSIGNED 0

using namespace std;

class Sudoku {
  public:
    friend ostream &operator<<(ostream &out, const Sudoku &sudoku);
    friend istream &operator>>(istream &in, Sudoku &sudoku);
    bool solve();

  private:
    int size;
    int boxSize;
    vector<vector<int>> field;

    void checkField();
    bool findUnassignedLocation(int *pRow, int *pColumn);
    bool existsInRow(int row, int value);
    bool existsInColumn(int column, int value);
    bool existsInBox(int startRow, int startColumn, int value);
    bool valid(int row, int column, int value);
};

ostream &operator<<(ostream &out, const Sudoku &sudoku) {
    for (int row = 0; row < sudoku.size; ++row) {
        for (int column = 0; column < sudoku.size; ++column) {
            out << sudoku.field[row][column] << " ";
        }

        out << endl;
    }

    return out;
}

istream &operator>>(istream &in, Sudoku &sudoku) {
    int value;
    in >> sudoku.size;
    sudoku.checkField();
    sudoku.boxSize = sqrt(sudoku.size);
    sudoku.field.resize(sudoku.size);

    for (int row = 0; row < sudoku.size; ++row) {
        sudoku.field[row].resize(sudoku.size);

        for (int column = 0; column < sudoku.size; ++column) {
            in >> value;
            sudoku.field[row][column] = value;
        }
    }

    return in;
}

bool Sudoku::solve() {
    int row = 0;
    int column = 0;

    if (!findUnassignedLocation(&row, &column)) {
        return true;
    }

    for (int value = 1; value <= size; ++value) {
        if (valid(row, column, value)) {
            field[row][column] = value;

            if (solve()) {
                return true;
            }

            field[row][column] = UNASSIGNED;
        }
    }

    return false;
}

void Sudoku::checkField() {
    if (pow((int)sqrt(size), 2) != size) {
        cout << "Invalid field" << endl;
        exit(0);
    }
}

bool Sudoku::findUnassignedLocation(int *pRow, int *pColumn) {
    for (int row = 0; row < size; ++row) {
        for (int column = 0; column < size; ++column) {
            if (field[row][column] == UNASSIGNED) {
                *pRow = row;
                *pColumn = column;
                return true;
            }
        }
    }

    return false;
}

bool Sudoku::existsInRow(int row, int value) {
    for (int column = 0; column < size; ++column) {
        if (field[row][column] == value) {
            return true;
        }
    }

    return false;
}

bool Sudoku::existsInColumn(int column, int value) {
    for (int row = 0; row < size; ++row) {
        if (field[row][column] == value) {
            return true;
        }
    }

    return false;
}

bool Sudoku::existsInBox(int startRow, int startColumn, int value) {
    for (int row = 0; row < boxSize; ++row) {
        for (int column = 0; column < boxSize; ++column) {
            if (field[row + startRow][column + startColumn] == value) {
                return true;
            }
        }
    }

    return false;
}

bool Sudoku::valid(int row, int column, int value) {
    return !existsInRow(row, value) && !existsInColumn(column, value) &&
           !existsInBox(row - row % boxSize, column - column % boxSize, value) &&
           field[row][column] == UNASSIGNED;
}

int main(int argc, char *argv[]) {
    ifstream file("field.txt");
    Sudoku sudoku;
    file >> sudoku;
    cout << sudoku << endl;
    sudoku.solve();
    cout << sudoku;
}
