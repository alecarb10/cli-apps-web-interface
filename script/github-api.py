from github import Github
import argparse
import csv


def stats(repo, g):
    repo = g.get_repo(repo)
    return repo.stargazers_count


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
            repositories.append(data)
            # repositories.append({'name': data['name'], 'git': data['git']})
    return repositories


def load_links(file_name):
    with open(file_name, "r") as linkscsv:
        reader = csv.reader(linkscsv)
        links = []
        for data in reader:
            links.append(data['git'])
    return links

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
    links = load_links(args.inputfile)
    repos = [url.replace("https://github.com/", "") for url in links]
    g = Github("access_token")
    # for link in links:
    #     repos = link.update("https://github.com/", "")
    # repo = [link.replace("https://github.com/", "") for link in links]
    counts = stats(repos, g)
    for data in repositories:
        data['cloned'] = '0'
        data['stars'] = counts
        data['watch'] = ''
        data['fork'] = ''
    fieldnames = ['name', 'git', 'cloned', 'stars', 'watch', 'fork']
    save(args.outfile, repositories, fieldnames)


if __name__ == "__main__":
    main()
