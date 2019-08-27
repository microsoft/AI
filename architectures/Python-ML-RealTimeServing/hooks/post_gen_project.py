import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dirpath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))


def move_files(parentdir, subdir):
    root = os.path.join(PROJECT_DIRECTORY, parentdir)
    for filename in os.listdir(os.path.join(root, subdir)):
        shutil.move(os.path.join(root, subdir, filename), os.path.join(root, filename))
    os.rmdir(os.path.join(root, subdir))


if __name__ == "__main__":

    if "{{ cookiecutter.deployment_type }}" == "aks":
        remove_dir("./iotedge")
        move_files(".", "./aks")

    if "{{ cookiecutter.deployment_type }}" == "iotedge":
        remove_dir("./aks")
        move_files(".", "./iotedge")

   
