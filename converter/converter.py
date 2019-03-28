import argparse
import subprocess
import time
import json
import zipfile
import sys
import os
import re


def zip_folder(folder_path, output_path):
    base_dir = os.path.abspath(folder_path)
    try:
        with zipfile.ZipFile(output_path, "w",
                             compression=zipfile.ZIP_DEFLATED) as zf:
            base_path = os.path.normpath(base_dir)
            for dirpath, dirnames, filenames in os.walk(base_dir):
                for name in sorted(dirnames):
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if ".ipynb" not in path:
                        zf.write(path, os.path.relpath(path, base_path))
                for name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, name))
                    if os.path.isfile(path):
                        filename, file_extension = os.path.splitext(name)
                        if str(file_extension) != ".ipynb":
                            zf.write(path, os.path.relpath(path, base_path))
    except Exception as message:
        print(message)
        sys.exit(1)
    finally:
        zf.close()


def remove_empty_lines(filename):
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)


def rw_file(filename, **kwargs):
    for k, v in kwargs.items():
        with open(filename, "r+") as fp:
            if "tensorflow" in k:
                lines = [line.replace(k, v) if k in line else line for line in fp]
            else:
                lines = [line.replace(line[:], "".join([v, "\n"])) if k in line else line for line in fp]

            fp.seek(0)
            fp.truncate()
            fp.writelines(lines)

    tf_gpu = "tensorflow-gpu=="
    with open(filename, "r+") as fp:
        lines = fp.readlines()
        for li in lines:
            try:
                if tf_gpu in li:
                    ver = li.split("==", 1)[1]
                    minor_ver = "12" if int(ver.split(".")[1]) > 8 else "8"
                    ver = "1." + minor_ver + ".0"
                    li = tf_gpu + ver + "\n"
                else:
                    li = li
            except Exception:
                ver = "1.12.0"
                li = tf_gpu + ver + "\n"

            fp.seek(0)
            fp.truncate()
            fp.writelines(lines)


def get_args_convert2py():
    try:
        parser = argparse.ArgumentParser(description="Convert Jupyter Notebook '.ipynb' files to python3 '.py' files")
        parser.add_argument("file", nargs='+', help="List one or more '.ipynb' files to be converted.")
        args = parser.parse_args()
        return args
    except Exception as e:
        raise RuntimeError('Parsing converting arguments failed. {} '.format(e))


def get_args_convert2or():
    try:
        parser = argparse.ArgumentParser(description="Wrap and convert python3 '.py' files into an '.zip' file"
                                                     "that can be uploaded as a task by NebulaAI Orion platform")
        # parser.add_argument("file", nargs='*')
        args = parser.parse_args()
        return args
    except Exception as e:
        raise RuntimeError('Parsing converting arguments failed. {} '.format(e))


def check_dir_path(theme, desc, loop, workspace_dir=None):
    for i in range(loop):
        dir_path = input(desc)
        if "project path" in theme:
            if dir_path == "":
                dir_path = os.curdir
        elif "output path" in theme:
            if dir_path == "":
                res = input("Warning: output path is empty, no files will be output."
                            " Please confirm('y' for empty output path, or the new output path): ")
                if not res.lower().startswith("y"):
                    dir_path = res

        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.abspath(os.curdir), dir_path)

        if "project path" not in theme:

            try:
                os.makedirs(dir_path)
            except FileExistsError:
                pass

            if dir_path.startswith(os.path.abspath(workspace_dir) + os.sep):
                return dir_path
            else:
                print("Invalid {}, it is outside your project. please try again. ".format(theme))
        else:
            if os.path.isdir(dir_path):
                return dir_path
            else:
                print("Invalid {}, please try again. ".format(theme))

    else:
        sys.exit("Invalid {}, system exits.".format(theme))


def check_file_path(theme, desc, loop, workspace_dir):
    for i in range(loop):
        file_path = input(desc)
        if os.path.isfile(file_path):
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.path.abspath(os.curdir), file_path)

            if file_path.startswith(os.path.abspath(workspace_dir) + os.sep):
                return file_path
            else:
                print("Invalid entry-point file path, file is outside of your project.")
        else:
            print("Invalid {} path, please try again.".format(theme))
    else:
        sys.exit("Invalid {] path, system exits.".format(theme))


def get_params():
    # check workspace path
    description_proj = "(Required) Project path: \n\t(Press 'Enter' or '.' for the current directory, " \
                  "'..' for the parent directory of the current folder): "
    topic_proj = "project path"
    workspace_path = check_dir_path(topic_proj, description_proj, 3)

    # check executable file path
    description_fp = "(Required) Entry-point file path(executable file path): "
    topic_fp = "entry-point file"
    exec_file_path = check_file_path(topic_fp, description_fp, 3, workspace_path)

    # check external data url format
    has_data_uri = input("Data configuration: \n\t"
                         "Do you have external data(data stored outside your project database)\n\t"
                         "that needs to be downloaded from a specific uri (y/n)? ")
    if has_data_uri.lower().startswith("y"):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for i in range(3):
            data_uri = input("\n\tExternal data uri: ")
            if re.match(regex, data_uri):
                # check external data_path
                description_dp = "\n\tPath to save the downloaded data within your project: "
                topic_dp = "external data saving path"
                data_saving_path = check_dir_path(topic_dp, description_dp, 3, workspace_path)
                break
            else:
                print("Invalid data uri, please try again. \n\t", exec_file_path)
        else:
            sys.exit("Invalid data uri, system exits.")

    else:
        data_uri = ""
        data_saving_path = ""

    # check output_path
    description_out = "\nPath for the task results(project output directory): "
    topic_out = "output path"
    output_path = check_dir_path(topic_out, description_out, 3, workspace_path)
    return workspace_path, exec_file_path, data_uri, data_saving_path, output_path


def convert2py():
    """
    Convert Jupyter Notebook '.ipynb' files to python3 '.py' files.
    """

    # parse converter arguments
    args = get_args_convert2py()
    try:
        p = list()
        for i in range(len(sys.argv) - 1):
            p.append(subprocess.Popen(["jupyter", "nbconvert", "--to", "python", args.file[i]]))
            p[i].wait()
        print('Converted files successfully!')

    except Exception as e:
        raise RuntimeError("Converting files failed: {}".format(e))


def convert2or():
    """
        Wrap and convert python3 '.py' files into an '.zip' file that can be uploaded
        as a task by NebulaAI Orion platform.
    """
    # parse converter arguments
    args = get_args_convert2or()

    # input data parameters
    try:
        workspace_dir, exec_file_name, data_uri, data_path, output_path = get_params()
        entry_filename = os.path.splitext(os.path.basename(exec_file_name))[0]
    except Exception as e:
        print('Invalid arguments, {}'.format(e))
        sys.exit(1)

    else:
        # Generate requirements.txt
        try:
            import pipreqs
        except ImportError as e:
            raise RuntimeError('Package installation failed: {}'.format(e))

        else:
            time.sleep(1)
            try:
                p = subprocess.Popen(["pipreqs", "--force", workspace_dir])
                p.wait()
                time.sleep(1)

                # fix the bug raising from 'tensorflow', 'tensorflow_gpu' and "tensorflow-gpu>1.12.0"
                filename = os.path.join(workspace_dir, "requirements.txt")

                rw_file(filename, matplotlib="matplotlib", tensorflow_gpu="", tensorflow="tensorflow-gpu")
                remove_empty_lines(filename)
                print("Generated 'requirements.txt' successfully!")

            except Exception as e:
                raise RuntimeError("Generating 'requirements.txt' failed: {}".format(e))

            else:
                # Generate params.json
                try:
                    exec_file_name_v = os.path.relpath(exec_file_name, start=workspace_dir)
                    data_path_v = "" if data_path == "" else os.path.relpath(data_path, start=workspace_dir)
                    output_path_v = "" if output_path == "" else os.path.relpath(output_path, start=workspace_dir)
                    params_json = json.dumps({"exec_file_name": exec_file_name_v,
                                              "data_uri": data_uri,
                                              "data_path": data_path_v,
                                              "output_path": output_path_v,
                                              })
                    with open(os.path.join(workspace_dir, "params.json"), 'w+') as f:
                        f.write(params_json)
                    print("Generated 'params.json' successfully!")

                except Exception as e:
                    raise IOError("Generating 'params.json' failed: {}".format(e))

                else:
                    time.sleep(2)
                    try:
                        zip_folder_path = os.path.join(workspace_dir, os.pardir, "task_files")

                        if not os.path.exists(zip_folder_path):
                            os.makedirs(zip_folder_path)

                        output_filename = str(entry_filename) + "_orion.zip"
                        zip_folder(workspace_dir, os.path.join(zip_folder_path, output_filename))
                        print('Zipped files successfully!')
                    except Exception as e:
                        raise RuntimeError('Zipping files failed: {}'.format(e))
                    else:
                        try:
                            os.remove(os.path.join(workspace_dir, "params.json"))
                            os.remove(os.path.join(workspace_dir, "requirements.txt"))
                        except Exception as e:
                            raise RuntimeError('Removing files failed: {}'.format(e))
