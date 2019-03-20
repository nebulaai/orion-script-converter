import argparse
import subprocess
import time
import json
import zipfile
import sys
import os


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
    except IOError as message:
        print(message)
        sys.exit(1)
    except OSError as message:
        print(message)
        sys.exit(1)
    except zipfile.BadZipfile as message:
        print(message)
        sys.exit(1)
    except Exception as message:
        print(message)
        sys.exit(1)
    finally:
        zf.close()


def get_args():
    try:
        parser = argparse.ArgumentParser(description='Convert files from Jupyter Notebook to python format.')
        parser.add_argument("files", nargs='+',
                            help="List files to be converted. The first arg is entry point(required).")
        args = parser.parse_args()
        return args
    except Exception as e:
        raise RuntimeError('Parsing converter arguments failed. {} '.format(e))


def get_params():
    data_uri = input("(Optional) Enter data uri (Press 'Enter' for none): " or '')
    data_path = input("(Optional) Enter data path for downloaded data(Press 'Enter' for none): " or '')
    output_path = input("(Optional) Enter path for output results(Press 'Enter' for none): " or '')
    return data_path, data_uri, output_path


def main():
    # input data parameters
    data_path, data_uri, output_path = get_params()

    # parse converter arguments
    args = get_args()
    entry_filename = os.path.splitext(args.files[0])[0]
    entry_filename_dir = os.path.dirname(os.path.abspath(args.files[0]))

    # Convert Jupyter Notebook files to python3 files
    try:
        # print(sys.argv, len(sys.argv))
        for i in range(len(sys.argv) - 1):
            p = subprocess.Popen(["jupyter", "nbconvert", "--to", "python", args.files[i]])
            p.wait()

        print('Converted Jupyter Notebook files to python files successfully!')

    except Exception as e:
        raise RuntimeError('Converting Jupyter Notebook files to python files failed: {}'.format(e))

    else:
        # Generate requirements.txt
        try:
            import pipreqs
            print('pipreqs is present!')
        except ImportError as e:
            raise RuntimeError('package installing failed: {}'.format(e))

        else:
            time.sleep(1)
            try:
                p2 = subprocess.Popen(["pipreqs", "--force", entry_filename_dir])
                print('Generated requirements.txt successfully!')
                p2.wait()
            except Exception as e:
                raise RuntimeError('Generating requirements.txt failed: {}'.format(e))

            else:
                # Generate params.json
                try:
                    params_json = json.dumps({"exec_file_name": entry_filename + ".py",
                                              "data_uri": data_uri,
                                              "data_path": data_path,
                                              "output_path": output_path
                                              })
                    with open(os.path.join(entry_filename_dir, "params.json"), 'w+') as f:
                        f.write(params_json)
                    print('Generated params.json successfully!')

                except Exception as e:
                    raise IOError('Creating params.json failed: {}'.format(e))

                else:
                    time.sleep(2)
                    try:
                        zip_folder_name = os.path.join(entry_filename_dir, os.pardir, "taskFiles")
                        print(zip_folder_name)
                        if not os.path.exists(zip_folder_name):
                            os.makedirs(zip_folder_name)
                        zip_folder(entry_filename_dir, os.path.join(zip_folder_name, entry_filename + "_orion.zip"))
                        print('zipped files successfully!')
                    except Exception as e:
                        raise RuntimeError('zipping files failed: {}'.format(e))
