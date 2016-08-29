"""

"""
import logging


def execute_tag(**kwargs):
    config = kwargs.get('config')
    repo_location = config.get('repository') or '.'
    repo = _create_repo(repo_location)
    release_branch = config.get('release-branch')
    if release_branch == repo.active_branch.name:
        tag = config.get('tag')
        repo.create_tag(tag)
        repo.git.push('--tags')




def register_tasks(registry):
    registry.register_task('git-tag', execute_tag)



def _create_repo(repo_location):
    import git
    return git.Repo(repo_location)