import os
import subprocess

def run_git_command(command):
    """Helper function to run Git commands and handle errors."""
    try:
        result = subprocess.run(command, check=True, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.cmd}")
        print(f"Error message: {e.stderr}")
        return False

def has_changes_to_commit(directory):
    """Check if there are changes to commit in the specified directory."""
    result = subprocess.run(f"git status {directory} --porcelain", shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return bool(result.stdout.strip())

def acp(final_path):
    print(f"Processing directory: {final_path}")
                    
    if not os.path.isdir(final_path):
        print(f"Directory {final_path} does not exist. Skipping.")
        return
    
    if not has_changes_to_commit(final_path):
        print(f"No changes to commit in {final_path}. Skipping.")
        return
    
    # Stage changes in the directory
    if not run_git_command(f"git add {final_path}"):
        print(f"Failed to stage changes in {final_path}. Skipping.")
        return

    # Commit the changes with a generic message
    if not run_git_command(f'git commit -m "Auto-commit add directory: {final_path}"'):
        print(f"Failed to commit changes in {final_path}. Skipping.")
        return

    # Push the changes to the remote repository
    if not run_git_command(f"git push origin main"):
        print(f"Failed to push changes for {final_path}. Skipping.")
        return

    print(f"Pushed changes for {final_path}")

paths = [
         "model1/no_bg_cropped_resized/", 
         "model2/split_with_augmentation/", 
         ]
dirs = ["test", "val", "train"]
big_categories = os.listdir("./model1/improved")
categories1 = os.listdir("./model1/full_dataset")
categories1 += ["bottom", "dress", "footwear", "top"]
categories2 = os.listdir("./model2/full_dataset")

for path in paths:
    if path.split("/")[0] == "model1":
        categories = categories1
    else:
        categories = categories2

    # improved
    if path == "model1/improved/" or path == "model1/improved_no_footwear/" or path == "model1/no_bg_cropped_no_footwear/":
        for big_category in big_categories:
            for dir in dirs:
                for category in categories:
                    final_path = os.path.join(path, big_category, dir, category)
                    acp(final_path)
    # no_bg_cropped_resized
    elif path == "model1/no_bg_cropped_resized/":
        for category in categories:
            final_path = os.path.join(path, category)
            acp(final_path)
    # split_with_augmentation
    elif path == "model2/split_with_augmentation/":
        for dir in dirs:
            for category in categories:
                final_path = os.path.join(path, dir, category)
                acp(final_path)

print("All selected directories processed.")