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
            # repositories.append({'name': data['name'], 'git': data['git'], 'cloned': 0,
            #                      'stars': 'N', 'watch': 'N', 'fork': 'N', 'lines_of_code': 0})
    return repositories


def save(out_file_name, repositories, fieldnames):
    with open(out_file_name, "w") as outfilecsv:
        writer = csv.DictWriter(outfilecsv, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        for data in repositories[:10]:
            writer.writerow(data)


def stats(repositories):
    for data in repositories[:10]:
        if 'https://github.com/' in data['git']:
            repo = data['git'].rsplit("/", 2)
            user = repo[1]
            project = repo[2]
            proc = subprocess.Popen(["curl", f"https://api.github.com/repos/{user}/{project}"], stdout=subprocess.PIPE)
            print(project)
            output = proc.stdout.read()
            stat = json.loads(output)
            # input()
            # print(project)
            # print(stat['stargazers_count'])
            data['stars'] = stat["stargazers_count"]
            data['watch'] = stat["subscribers_count"]
            data['fork'] = stat["forks_count"]
        else:
            data['stars'] = '/'
            data['watch'] = '/'
            data['fork'] = '/'


def ctrl(repositories, url):
    for row in repositories[:10]:
        if url == row['git']:
            return True


def clone(repositories):
    for row in repositories[:10]:
        if row['cloned'] == 0:
            parent_dir = "/home/ale/tesi/cli-apps-web-interface/repositories"
            directory = row['name']
            path = os.path.join(parent_dir, directory)
        # if row['cloned'] == 0:
            if 'https://sourceforge.net/' in row['git']:
                next(iter(row))
            elif 'https://selenic.com/' in row['git']:
                next(iter(row))
            elif row['git'] == '':
                next(iter(row))
            elif 'https://www.mercurial-scm.org/' in row['git']:
                next(iter(row))
            elif 'https://github.com/' or 'https://git.savannah.gnu.org/' in row['git']:
                os.mkdir(path)
                Repo.clone_from(row['git'], path)
                row['cloned'] = 1
                # print("-----", row['git'], "-----")
                proc = subprocess.Popen(["cloc", "--json", "--quiet", path], stdout=subprocess.PIPE)
                output = proc.stdout.read()
                loc = json.loads(output)
                row['lines_of_code'] = loc['SUM']['code']
            # writer.writerow({'name': row['name'], 'git': row['git'], 'cloned': row['cloned']})
            # shutil.move(tempfile.name, filename)
            # i += 1

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


def main():
    # parser = init_argparser()
    # args = parser.parse_args()
    # inputcsv = '/home/ale/tesi/cli-apps/data/apps.csv'
    # outcsv = '/home/ale/tesi/cli-apps-web-interface/stats-ridotto.csv'
    filecsv = '/home/ale/tesi/cli-apps-web-interface/files/stats-ridotto.csv'
    link = 'https://github.com/nadrad/h-m-m'
    # repositories = load(args.outfile)
    # url = args.urls
    repositories = load(filecsv)
    url = link
    if ctrl(repositories, url) is True:
        clone(repositories)
        stats(repositories)
        print("Statistiche di " + url + " aggiornate")
    fieldnames = ['name', 'git', 'cloned', 'stars', 'watch', 'fork', 'lines_of_code']
    # save(args.outfile, repositories, fieldnames)
    save(filecsv, repositories, fieldnames)


if __name__ == "__main__":
    main()


# CONTEGGIO STAR
# curl https://api.github.com/repos/toolleeo/cli-apps | grep 'stargazers_count'
# CONTEGGIO FORKS
# curl https://api.github.com/repos/curl/curl | grep 'forks_count'
# CONTEGGIO WATCH
# curl https://api.github.com/repos/curl/curl | grep 'subscribers_count'

# https://github.com/nadrad/h-m-m https://github.com/haileys/quickserve

#     for links in repositories:
#         links['git'] = links.update("https://github.com/", "")
