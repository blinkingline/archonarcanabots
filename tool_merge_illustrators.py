import csv
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description='Merge two illustrator CSV files.')
    parser.add_argument('--file1', required=True, help='Path to the first CSV file')
    parser.add_argument('--file2', required=True, help='Path to the second CSV file')
    parser.add_argument('--f1-name', required=True, help='Column name for card name in file1')
    parser.add_argument('--f1-artist', required=True, help='Column name for illustrator in file1')
    parser.add_argument('--f2-name', required=True, help='Column name for card name in file2')
    parser.add_argument('--f2-artist', required=True, help='Column name for illustrator in file2')
    parser.add_argument('--output', default='skyjedi/illustrators.csv', help='Path to the output CSV file')

    args = parser.parse_args()

    def load_csv(path, name_col, artist_col):
        data = {}
        with open(path, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row[name_col].strip()
                artist = row[artist_col].strip()
                # Second halves of gigantics have blank artist.
                if name and artist:
                    data[name] = artist
        return data

    try:
        data1 = load_csv(args.file1, args.f1_name, args.f1_artist)
        data2 = load_csv(args.file2, args.f2_name, args.f2_artist)
    except KeyError as e:
        print(f"Error: Column {e} not found in input file.")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    merged_data = {}
    conflicts = []

    count_existing = 0
    count_new = 0
    count_merged = 0

    all_names = sorted(set(data1.keys()) | set(data2.keys()))

    for name in all_names:
        val1 = data1.get(name)
        val2 = data2.get(name)

        if val1 and val2:
            if val1 != val2:
                conflicts.append((name, val1, val2))
            merged_data[name] = val1
            count_merged += 1
        elif val1:
            merged_data[name] = val1
            count_existing += 1
        else:
            merged_data[name] = val2
            count_new += 1

    if conflicts:
        print("Conflicts found! No output written.")
        print(f"{'Card Name':<40} | {'File 1 Artist':<30} | {'File 2 Artist':<30}")
        print("-" * 106)
        for name, v1, v2 in conflicts:
            print(f"{name:<40} | {v1:<30} | {v2:<30}")
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(args.output, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['card_title', 'illustrator_name'])
        for name in all_names:
            writer.writerow([name, merged_data[name]])

    print(f"Successfully merged files into {args.output}")
    print(f"Existing rows: {count_existing}")
    print(f"New rows: {count_new}")
    print(f"Merged rows: {count_merged}")

if __name__ == '__main__':
    main()
