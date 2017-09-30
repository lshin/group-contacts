from src.base import Base
from hashids import Hashids
import csv
import re
import itertools
import logging

class Contacts(Base):
    """Grouping contact command"""

    def run(self):
        """Return void

        Main processing method analyzing all data and produce a output file
        """
        input_data = self._get_input_data(self.options['--input'])
        header, data = input_data[0], input_data[1:]
        rows = len(data)

        matching_column_indexes = self._get_matching_column_indexes(header)
        matrix_data = self._build_matrix(data, matching_column_indexes)
        visited = [False for i in range(rows)]
        matched_vertices = []
        for i in range(rows):
            if not visited[i]:
                self._search(i, matrix_data, visited, matched_vertices, rows)
        self._create_identifier(data, rows, matched_vertices)
        self._save_output_data(['Identifier'] + header,  data)

    def _get_input_data(self, file):
        """Return list

        Read a file as universal newline mode
        """
        data = []
        try:
            with open(file, 'rU') as csv_file:
                reader = csv.reader(csv_file, dialect=csv.excel_tab, delimiter=',', quotechar='|')
                for row in reader:
                    data.append(row)
        except csv.Error as e:
            exit(e)
        return data

    def _get_matching_column_indexes(self, header):
        """Return list

        Check a first row which should contains all columns name
        and match with matching types and return a list of matched column index
        """
        matching_options = self.options['--type']
        return [i for i, column in enumerate(header) for option in matching_options if re.match('^{}'.format(option), column, re.IGNORECASE)]

    def _build_matrix(self, data, indexes):
        """Return list

        Create a dictionary with a search criteria key and associated column values
        and if it has multiple data, then creating a matrix map with matched rows

        n : number of rows
        m : searchable columns
        Time complexity: O(n*m + n)
        Space complexity : O(n*m)

        TODO : Maybe it's a bit slow to create a matrix for a large dataset
               Pandas module or numpy will improve this searching and grouping dataset.
        """
        matrix = [[0]*(len(data)) for i in range(len(data))]
        # create a dictionary with combined matching type criteria
        cached = {}
        for i in range(len(data)):
            for column in indexes:
                key = data[i][column]
                if key != '':
                    if key in cached:
                        cached[key].append(i)
                    else:
                        cached[key] = [i]

        # create a matrix from cached data
        for key, data in cached.iteritems():
            data_length = len(data)
            if data_length > 1:
                for i in range(1, len(data)):
                    if data[0] != data[i]:
                        matrix[data[0]][data[i]] = 1
                        matrix[data[i]][data[0]] = 1
        return matrix

    def _search(self, index, matrix_data, visited, vertices, rows):
        """Return void

        Recursive function for creating all with all adjacent vertices
        from the matrix dataset.
        """
        visited[index] = True
        for j in range(rows):
            if matrix_data[index][j] == 1 and not visited[j]:
                vertices.append((index, j))
                self._search(j, matrix_data, visited, vertices, rows)

    def _create_identifier(self, data, rows, matched):
        """Return void

        Fill indexes with unique identifiers
        And update all matched rows with a root of vertex in-place
        """
        hashid = Hashids()
        for i in range(rows):
            data[i][:0] = [hashid.encode(i)]

        for i, j in matched:
            id = data[i][0]
            data[j][0] = id

    def _save_output_data(self, header, data):
        """Return void

        Saving all output data into a csv file
        """
        output_file = self.options['--output']
        try:
            with open(output_file, 'w+') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                for row in data:
                    writer.writerow(row)
        except csv.Error as e:
            exit(e)