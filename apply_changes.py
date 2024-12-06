import subprocess
import sys
import json
import base64
import http.client
from pathlib import Path

__mypath = Path.cwd()


def file_get_contents(file_name, default_content):
    f = __mypath / file_name
    if(not f.exists()):
        return default_content
    return f.read_text();

def file_put_contents(file_name, file_text):
    f = __mypath / file_name
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(file_text)

def post_data_to_zenit(input):
    
    conn = http.client.HTTPSConnection("zenit-web.ir")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    conn.request("POST", "/wp-admin/admin-ajax.php?action=zenitgene", input.encode(), headers)

    response = conn.getresponse()
    response_data = response.read().decode()
    conn.close()

    return response_data

def run_command(command):
    """Run a shell command and return the output."""
    print(f"##:{' '.join(command)}")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout.strip()

def get_current_branch():
    return run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])

def branch_exists(branch_name):
    try:
        run_command(['git', 'rev-parse', '--verify', branch_name])
        return True
    except SystemExit:
        return False

def change_branch(branch_name):
    if branch_exists(branch_name):
        run_command(['git', 'checkout', branch_name])
        print(f"Switched to existing branch '{branch_name}'")
    else:
        run_command(['git', 'checkout', '-b', branch_name])
        print(f"Created and switched to new branch '{branch_name}'")

def apply_changes(contents):

    contents = json.loads(contents)

    for c in contents:
        if(c):
            file_put_contents(c["file"], base64.b64decode(c["content"]).decode())


def commit_changes(branch_name, message):
    run_command(['git', 'add', '.'])  # Add all changes
    run_command(['git', 'commit', '-m', message])
    run_command(['git', 'push', '--set-upstream', 'origin', branch_name])
    print(f"Committed changes and set upstream for branch '{branch_name}'.")

def merge_branch(original_branch):
    run_command(['git', 'merge', original_branch])
    print(f"Merged branch '{original_branch}' into the current branch.")

def check_if_anything_to_commit():
    output = run_command(['git', 'status', '--porcelain'])
    return bool(output)

def main(new_branch):

    zenit_config = file_get_contents('zenit-config.hjson', '[]')
    zenit_changes = post_data_to_zenit(zenit_config)

    original_branch = get_current_branch()
    print(f"Current branch: {original_branch}")

    if check_if_anything_to_commit():
        commit_changes(original_branch, f"Auto Commit: {original_branch}")

    # Step 2: Change branch to new_branch, create new if not exists
    change_branch(new_branch)

    # Step 3: Apply some changes to files
    apply_changes(zenit_changes)
    file_put_contents('zenit-config.hjson', zenit_config)

    any_thing_to_commit = check_if_anything_to_commit()

    if any_thing_to_commit:
        # Step 4: Commit this branch, set upstream also
        commit_changes(new_branch, f"Changes applied in {new_branch}")

    # Step 5: Change branch back to original one
    change_branch(original_branch)

    if any_thing_to_commit:
        # Step 6: Merge new_branch into the original branch
        merge_branch(new_branch)

    # Step 7: If merge is successful, commit changes
    print("Merge completed successfully.")


main('zenit-gene')