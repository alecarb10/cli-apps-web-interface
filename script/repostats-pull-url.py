import csv
import json

from git import Repo
import git
import os
import argparse
import subprocess


def init_argparser():
    parser = argparse.ArgumentParser()
    # parser.add_argument('inputfile', action="store", type=str)
    parser.add_argument('-o', '--outfile', nargs='?', action="store", type=str)
    parser.add_argument('-u', '--urls', nargs='?', type=str)
    return parser


def load(file_name):
    with open(file_name, "r") as filecsv:
        reader = csv.DictReader(filecsv, delimiter='\t')
        repositories = []
        for data in reader:
            repositories.append(data)
    return repositories


def save(out_file_name, repositories, fieldnames):
    with open(out_file_name, "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories[:10]:
            writer.writerow(data)


def stats(row):
    if 'https://github.com/' in row['git']:
        repo = row['git'].rsplit("/", 2)
        user = repo[1]
        project = repo[2]
        proc = subprocess.Popen(["curl", f"https://api.github.com/repos/{user}/{project}"], stdout=subprocess.PIPE)
        print(project)
        output = proc.stdout.read()
        stat = json.loads(output)
        row['stars'] = stat["stargazers_count"]
        row['watch'] = stat["subscribers_count"]
        row['fork'] = stat["forks_count"]
        print("Statistiche di " + row['git'] + " aggiornate")
    else:
        row['stars'] = '/'
        row['watch'] = '/'
        row['fork'] = '/'
        print("Statistiche di " + row['git'] + " aggiornate")


def clone(repositories, url):
    whitelist = ['https://github.com/', 'https://git.savannah.gnu.org/', 'https://repo.or.cz/', 'https://ezix.org/',
                 'https://git.skoll.ca/', 'https://gitlab.com/', 'https://git.finalrewind.org/',
                 'https://gitlab.xiph.org/', 'git://git-annex.branchable.com', 'http://www.wagner.pp.ru/',
                 'https://code.blicky.net/', 'https://git.deluge-torrent.org/', 'https://git.zx2c4.com/',
                 'https://src.adamsgaard.dk/', 'https://www.kariliq.nl/', 'https://git.calcurse.org/',
                 'https://dev.gnupg.org/', 'https://tildegit.org/', 'git://git.suckless.org/', 'https://git.sr.ht/',
                 'https://git.frama-c.com/', 'git://git.z3bra.org/', 'https://git.meli.delivery/',
                 'https://0xacab.org/', 'https://basedwa.re/', 'https://codeberg.org/']
    for row in repositories[:10]:
        if url == row['git']:
            if row['cloned'] == '0':
                parent_dir = "/home/ale/tesi/cli-apps-web-interface/repositories"
                directory = row['name']
                path = os.path.join(parent_dir, directory)
                for item in whitelist:
                    if row['git'].startswith(item):
                        os.mkdir(path)
                        Repo.clone_from(row['git'], path)
                        row['cloned'] = 1
                        proc = subprocess.Popen(["cloc", "--json", "--quiet", path], stdout=subprocess.PIPE)
                        output = proc.stdout.read()
                        loc = json.loads(output)
                        row['lines_of_code'] = loc['SUM']['code']
                stats(row)
            else:
                parent_dir = "/home/ale/tesi/cli-apps-web-interface/repositories"
                directory = row['name']
                path = os.path.join(parent_dir, directory)
                g = git.Repo(path)
                g.remotes.origin.pull()
                proc = subprocess.Popen(["cloc", "--json", "--quiet", path], stdout=subprocess.PIPE)
                output = proc.stdout.read()
                loc = json.loads(output)
                row['lines_of_code'] = loc['SUM']['code']
                stats(row)
        else:
            next(iter(row))


def main():
    parser = init_argparser()
    args = parser.parse_args()
    # filecsv = '/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv'
    # link = 'https://git.savannah.gnu.org/git/nano.git'
    repositories = load(args.outfile)
    url = args.urls
    # repositories = load(filecsv)
    # url = link
    clone(repositories, url)
    fieldnames = ['name', 'git', 'cloned', 'stars', 'watch', 'fork', 'lines_of_code', 'description', 'like']
    save(args.outfile, repositories, fieldnames)
    # save(filecsv, repositories, fieldnames)


if __name__ == "__main__":
    main()
