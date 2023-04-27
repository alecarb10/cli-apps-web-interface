import csv
import argparse

def init_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', action="store", type=str)
    parser.add_argument('outfile', action="store", type=str)
    return parser

def load(file_name):
    with open(file_name, "r") as filecsv:
        reader = csv.DictReader(filecsv)
        repositories = []
        for data in reader:
            # repositories.append(data)
            repositories.append({'name': data['name'], 'git': data['git']})
    return repositories

def save(out_file_name, repositories, fieldnames):
    with open(out_file_name, "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories[:10]:
            writer.writerow(data)

def main():
    parser = init_argparser()
    args = parser.parse_args()
    repositories = load(args.inputfile)
    for data in repositories:
        data['cloned'] = '0'
        data['fork'] = 'N'
    fieldnames = ['name', 'git', 'cloned', 'fork']
    save(args.outfile, repositories, fieldnames)


if __name__ == "__main__":
    main()
