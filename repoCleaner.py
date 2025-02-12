import os
import datetime
from github import Github

# Your GitHub token (replace with your actual token, or load it from an environment variable for better security)
GITHUB_TOKEN = "github_id"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Read repos from masterRepoList.txt
def read_repositories():
    with open("masterRepoList.txt", "r") as file:
        repos = file.readlines()
    return [repo.strip() for repo in repos]

# Initialize GitHub client
def initialize_github():
    return Github(GITHUB_TOKEN)

# Get stale branches based on the last commit date (older than 1 year)
def get_stale_branches(repo):
    stale_branches = []
    one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)

    for branch in repo.get_branches():
        try:
            last_commit = branch.commit.committer.date  # Access commit date
            if last_commit < one_year_ago:
                stale_branches.append(branch.name)
        except AttributeError:
            print(f"Skipping branch {branch.name}, no commit date found.")
    
    return stale_branches

# Deleting the selected branches
def delete_branches(repo, branches_to_delete):
    for branch_name in branches_to_delete:
        try:
            branch = repo.get_git_ref(f"heads/{branch_name}")
            branch.delete()
            print(f"Deleted branch: {branch_name}")
        except Exception as e:
            print(f"Error deleting branch {branch_name}: {str(e)}")

# Main function to run the utility
def repo_cleaner():
    repos = read_repositories()
    github_client = initialize_github()

    for repo_url in repos:
        repo_name = repo_url.split("/")[-1]
        user_repo = github_client.get_repo(f"kumarece1305/{repo_name}")

        stale_branches = get_stale_branches(user_repo)
        
        if stale_branches:
            print(f"Stale branches in {repo_name}: {stale_branches}")
            user_input = input("Do you want to delete these branches? (y/n): ")

            if user_input.lower() == 'y':
                branches_to_delete = input(f"Which branches to delete from {stale_branches}? (comma-separated): ")
                branches_to_delete = branches_to_delete.split(",")
                delete_branches(user_repo, branches_to_delete)
            else:
                print(f"Skipping deletion for {repo_name}")
        else:
            print(f"No stale branches in {repo_name}")

    print("repoCleaner run complete.")

if __name__ == "__main__":
    repo_cleaner()
