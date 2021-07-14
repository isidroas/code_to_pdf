from git import Repo
import os

PATH = '/home/isidro/wat'


def get_git_info(path):
    repo = Repo(path)
    is_dirty = repo.is_dirty()
    commit =  str(repo.head.commit) + '*' if is_dirty else ''
    datetime = repo.head.commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
    branch = repo.active_branch.name
    return commit, datetime, branch

print(get_git_info(PATH))
#repo = Repo()
