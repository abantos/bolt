"""

"""
import logging
import os


def execute_tag(**kwargs):
    config = kwargs.get('config')
    repo_location = config.get('repository') or '.'
    repo = _create_repo(repo_location)
    release_branch = config.get('release-branch')
    branch_var = config.get('current-branch-var')
    current_branch = os.environ.get(branch_var)

    if release_branch == current_branch:
        tag = config.get('tag')
        repo.create_tag(tag)
        repo.git.push('--tags')




def register_tasks(registry):
    registry.register_task('git-tag', execute_tag)



def _create_repo(repo_location):
    import git
    return git.Repo(repo_location)