import git

def update_csv_from_repo():
    """ Automates a Git pull command from https://github.com/CSSEGISandData/COVID-19.git """
    local_repo_path = 'data/COVID-19'
    remote_repo_path = 'https://github.com/CSSEGISandData/COVID-19.git'
    
    print("Executing Git pull request from {}...".format(remote_repo_path))

    local_repo = git.Repo(local_repo_path)
    origin = local_repo.remote(name='origin')
    origin.pull()