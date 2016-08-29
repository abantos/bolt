"""

"""
import logging
import os


def execute_tag(**kwargs):
    config = kwargs.get('config')
    repo_location = config.get('repository') or '.'
    repo = _create_repo(repo_location)
    release_branch = config.get('release-branch')
    logging.info('Release branch: ' + release_branch)
    branch_var = config.get('current-branch-var')
    current_branch = os.environ.get(branch_var)
    logging.info('Current branch: ' + current_branch)

    if release_branch == current_branch:
        tag = config.get('tag')
        message = config.get('tag-message')
        repo.create_tag(tag, message=message)
        logging.info('Tag <{tag}> created'.format(tag=tag))
        remote_template = config.get('remote-template')
        user = os.environ.get('GIT_USERNAME')
        password = os.environ.get('GIT_PASSWORD')
        remote = remote_template.format(user=user, password=password)
        repo.git.push([remote, '--tags'])




def register_tasks(registry):
    registry.register_task('git-tag', execute_tag)



def _create_repo(repo_location):
    import git
    return git.Repo(repo_location)