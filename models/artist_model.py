import csv

class ArtistMap(object):
    def __init__(self):
        self.m = {}

    def add_csv(self, csv_file):
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            h0 = header[0] != 'card_title'
            h1 = header[1] != 'card_type'
            h2 = header[2] != 'illustrator_name'
            if h0 or h1 or h2:
                raise Exception('Check CSV schema!')

            for row in csv_reader:
                self.m[row[0]] = row[2]

    def get(self, card_title):
        if card_title not in self.m:
            return None
        return self.m[card_title]
