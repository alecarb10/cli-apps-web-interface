import csv
from git import Repo
import git
import os


with open("/home/ale/tesi/cli-apps/data/apps.csv", "r") as filecsv:
    lettore = csv.DictReader(filecsv)
    repositories = []
    names = []
    cloned = []
    for links in lettore:
        repositories.append(links['git'])
        names.append(links['name'])
        # cloned.append(False)

    # print(repositories)
    # print(names)
    # print(cloned)
    # return repositories
    # return names
    # exit(0)

    i = 0

    # Per i repo con i link savannah non funziona il  comando Repo.clone, COME PD lo risolvo?

    # for repo in repositories[:len(names)]:
    for repo in repositories[:10]:
        cloned.append(False)
        if cloned[i] is False:
            parent_dir = "/home/ale/tesi/repositories"
            directory = names[i]
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)

            if repositories[i] is not "":
                Repo.clone_from(repo, path)
                cloned[i] = True
                i += 1
            else:
                i += 1
