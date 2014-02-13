__author__ = 'root'
from .diff import (
    create_grid,
    find_matches,
)

class BooleanPlus(object):

    def __init__(self, truthfulness, mod):
        self.truth = truthfulness
        self.modified = mod

    def __nonzero__(self):
        '''
        for evaluating as a boolean
        '''
        return self.truth

    def is_modified(self):
        return self.modified


class CellComparator():

    def __init__(self, data):
        self.data = data

    def __eq__(self, other):
        return self.equal(self.data, other.data)

    def equal(self, cell1, cell2):
        if not cell1["cell_type"] == cell2["cell_type"]:
            return False
        if cell1["cell_type"] == "heading":
            return cell1["source"] == cell2["source"] and \
                cell1["level"] == cell2["level"]
        elif self.istextcell(cell1):
            return cell1["source"] == cell2["source"]
        else:
            return self.compare_cells(cell1,cell2)


    def istextcell(self, cell):
        return "source" in cell

    def equaloutputs(self, output1, output2):
        if not len(output1) == len(output2):
            return False
        for i in range(0, len(output1)):
            if not output1[i] == output2[i]:
                return False
        return True

    def count_similar_lines(self, cell1, cell2):
        grid = create_grid(cell1['input'], cell2['input'])
        matches = []
        for colnum in range(len(grid)):
            new_matches = find_matches(grid[colnum],colnum)
            matches = matches + new_matches

        matched_cols = [r[0] for r in matches]
        matched_rows = [r[1] for r in matches]

        unique_cols = []
        [unique_cols.append(col) for col in matched_cols if col not in unique_cols]
        unique_rows = []
        [unique_rows.append(row) for row in matched_rows if row not in unique_rows]

        return min(len(unique_cols), len(unique_rows))

    def compare_cells(self, cell1, cell2):
        '''
        return true if exactly equal or if equal but modified,
        otherwise return false
        return type: BooleanPlus
        '''
        eqlanguage = cell1["language"] == cell2["language"]
        eqinput = cell1["input"] == cell2["input"]
        eqoutputs = self.equaloutputs(cell1["outputs"], cell2["outputs"])
        if eqlanguage and eqinput and eqoutputs:
            return BooleanPlus(True, False)
        unchanged_count = self.count_similar_lines(cell1, cell2)
        similarity_percent = (2.0 * unchanged_count) / (len(cell1) + len(cell2))
        if similarity_percent >= 0.50:
            return BooleanPlus(True, True)
        return BooleanPlus(False, True)






