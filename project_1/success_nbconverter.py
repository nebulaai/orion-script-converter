import json
import os
import sys
import re
import time
import zipfile
import subprocess

from tkinter import ttk, StringVar, messagebox, Tk, scrolledtext, Button, END
from tkinter.filedialog import askopenfilename, askdirectory


class GUI:

    def __init__(self, win):
        # 'StringVar()' is used to get the instance of input field
        self.input_text_project_dir = StringVar()
        self.input_text_exec_file = StringVar()
        self.input_text_output_dir = StringVar()
        self.input_text_data_url = StringVar()
        self.input_text_data_dir = StringVar()
        self.success = StringVar()

        self.path_project_dir = os.getcwd()
        self.path_output_dir = ''
        self.path_exec_file = ''
        self.path_data_dir = ''
        self.path_data_url = ''

        self.win = win

        self.project_dir = ""
        self.output_dir = ""
        self.exec_file = ""
        self.data_url = ""
        self.data_dir = ""
        self.has_data_uri = "no"

        self.win.title("NBAI Task Converter")
        self.win.resizable(0, 0)

        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        width = 1000
        height = 760

        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2
        self.win.geometry('%dx%d+%d+%d' % (width, height, x, y))

        self.submitButton = ttk.Button(self.win, text="Validate", width=30)
        self.submitButton_funcid = self.submitButton.bind('<Button-1>', self.validate_input)
        self.quitButton = ttk.Button(self.win, text="Convert", width=30)

        self.scr = scrolledtext.ScrolledText(window, width=85, height=12, font=("Courier New", 12))

        self.make_form()

    def make_form(self):
        self.has_data_uri = messagebox.askquestion("Data Configuration", "Do you have external data("
                                                                         "data stored outside your project database)"
                                                                         " that needs to be downloaded from a specific "
                                                                         "uri (y/n)? ")
        if self.has_data_uri == "yes":
            ttk.Button(self.win, text="Input data URI (starting with\r\n'http://', 'https://' or 'ftp://')", width=30,
                       command=lambda: self.set_path_data_url()).grid(
                row=4, ipadx=5, ipady=5, padx=5, pady=5)
            ttk.Entry(self.win, textvariable=self.input_text_data_url,
                      width=500).grid(row=4, column=1, ipadx=5, ipady=5, padx=5, pady=5)

            ttk.Button(self.win, text="Select Data Directory", width=30,
                       command=lambda: self.set_path_data_dir()).grid(row=5, ipadx=5, ipady=5, padx=5, pady=5)
            ttk.Entry(self.win, textvariable=self.input_text_data_dir,
                      width=500).grid(row=5, column=1, ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Button(self.win, text="Select Project Directory", width=30,
                   command=lambda: self.set_path_project_dir()).grid(row=1, ipadx=5, ipady=5, padx=5, pady=5)
        self.input_text_project_dir.set(self.path_project_dir)
        ttk.Entry(self.win, textvariable=self.input_text_project_dir,
                  width=500).grid(row=1, column=1, ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Button(self.win, text="Select Output Directory", width=30,
                   command=lambda: self.set_path_output_dir()).grid(row=2, ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Entry(self.win, textvariable=self.input_text_output_dir,
                  width=500).grid(row=2, column=1, ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Button(self.win, text="Select Project Entry-Point File", width=30,
                   command=lambda: self.set_path_exec_file()).grid(row=3, ipadx=5, ipady=5, padx=5, pady=5)
        ttk.Entry(self.win, textvariable=self.input_text_exec_file, width=500).grid(
            row=3, column=1, ipadx=5, ipady=5, padx=5, pady=5)

        self.submitButton.grid(row=6, ipadx=5, ipady=5, padx=5, pady=5)

    def set_path_project_dir(self):
        self.path_project_dir = askdirectory(initialdir=os.getcwd(), title="Select project directory")
        self.input_text_project_dir.set(self.path_project_dir)

    def set_path_exec_file(self):
        self.path_exec_file = askopenfilename(
            initialdir=self.input_text_project_dir.get() if self.input_text_project_dir else os.getcwd(),
            title='Select the entry-point (executable) file',
            filetypes=(("python files", "*.py *.ipynb"), ("all files", "*.*")))
        self.input_text_exec_file.set(self.path_exec_file)

    def set_path_output_dir(self):
        self.path_output_dir = askdirectory(
            initialdir=self.input_text_project_dir.get() if self.input_text_project_dir else os.getcwd(),
            title="Select output directory")
        self.input_text_output_dir.set(self.path_output_dir)

    def set_path_data_dir(self):
        self.path_data_dir = askdirectory(
            initialdir=self.input_text_project_dir.get() if self.input_text_project_dir else os.getcwd(),
            title="Select data directory")
        self.input_text_data_dir.set(self.path_data_dir)

    def set_path_data_url(self):
        self.input_text_data_dir.set(self.path_data_url)

    def validate_input(self, event):
        # check project path
        self.path_project_dir = str(self.input_text_project_dir.get())
        display_message(self.scr, "project_dir: {}".format(self.path_project_dir))
        project_path_try = self.check_project_path(self.path_project_dir)
        if project_path_try == -1:
            self.go_exit(event)
        elif project_path_try == 0:
            self.win.update()
        else:
            # check output path
            self.path_output_dir = str(self.input_text_output_dir.get())
            display_message(self.scr, "output_dir: {}".format(self.path_output_dir))
            output_path_try = self.check_output_path(self.path_output_dir, self.path_project_dir)

            if output_path_try == -1:
                self.go_exit(event)
            elif output_path_try == 0:
                self.win.update()
            else:
                if output_path_try == 2:
                    self.path_output_dir = ""

                # check exec_file
                self.path_exec_file = str(self.input_text_exec_file.get())
                if self.path_exec_file.split('.')[-1] == "ipynb":
                    self.path_exec_file_py = self.path_exec_file[:-6] + '.py'
                else:
                    self.path_exec_file_py = self.path_exec_file
                display_message(self.scr, "exec_file: {}".format(self.path_exec_file_py))

                exec_file_try = check_file_path(self.path_exec_file, self.path_exec_file_py, self.path_project_dir)
                if exec_file_try == -1:
                    self.go_exit(event)
                elif exec_file_try == 0:
                    self.win.update()
                else:
                    if self.has_data_uri == "no":
                        self.project_dir = self.path_project_dir
                        self.output_dir = self.path_output_dir
                        self.exec_file = self.path_exec_file_py
                        self.data_url = ""
                        self.data_dir = ""
                        self.validate_success()

                    else:
                        # check data url
                        self.path_data_url = str(self.input_text_data_url.get())
                        display_message(self.scr, "data_url:{} ".format(self.path_data_url))
                        data_url_try = self.check_data_url(self.path_data_url)
                        if data_url_try == -1:
                            self.go_exit(event)
                        elif data_url_try == 0:
                            self.win.update()
                        else:
                            # check data dir
                            self.path_data_dir = str(self.input_text_data_dir.get())
                            display_message(self.scr, "data_dir: {}".format(self.path_data_dir))
                            data_path_try = self.check_data_path(self.path_data_dir, self.path_project_dir)

                            if data_path_try == -1:
                                self.go_exit(event)
                            elif data_path_try == 0:
                                self.win.update()
                            else:
                                self.project_dir = self.path_project_dir
                                self.output_dir = self.path_output_dir
                                self.exec_file = self.path_exec_file
                                self.data_url = self.path_data_url
                                self.data_dir = self.path_data_dir

                                self.validate_success()

    def validate_success(self):
        self.success.set("Validated successfully, press \'Convert\' button to continue")
        ttk.Entry(self.win, textvariable=self.success, width=500).grid(
            row=6, column=1, ipadx=5, ipady=5, padx=5, pady=5)
        self.quitButton.grid(row=7, ipadx=5, ipady=5, padx=5, pady=5)
        self.quitButton.bind('<Button-1>', self.go_convert)

    @staticmethod
    def check_data_path(dirname, workspace_dir=''):
        dir_path = dirname
        if dir_path == "":
            ans = messagebox.askokcancel("Data directory", "Data directory is empty.")
            if ans:
                return 0  # empty output
            else:
                return -1
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.abspath(os.curdir), dir_path)

        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass

        if dir_path.startswith(os.path.abspath(workspace_dir) + os.sep):
            return 1
        else:
            if messagebox.askretrycancel("Data Directory", "Data directory is NOT inside your project"):
                return 0
            else:
                return -1

    @staticmethod
    def check_data_url(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not re.match(regex, url):
            if not messagebox.askretrycancel("Data URL", "Invalid Data URL!"):
                return -1
            else:
                return 0
        else:
            return 1

    def go_exit(self, e):
        self.submitButton.unbind("<Button-1>")
        sys.exit(0)

    def go_convert(self, e):
        global project_dir
        global exec_file
        global output_dir
        global data_url
        global data_dir

        project_dir = self.project_dir
        exec_file = self.exec_file
        output_dir = self.output_dir
        data_url = self.data_url
        data_dir = self.data_dir

        # display_message(self.scr, "final project: {}".format(project_dir))
        # display_message(self.scr, "final file: {}".format(exec_file))
        # display_message(self.scr, "final output: {}".format(output_dir))
        # display_message(self.scr, "final data url: {}".format(data_url))
        # display_message(self.scr, "final data dir: {}".format(data_dir)
        #                 )
        self.submitButton.unbind("<Button-1>")
        self.quitButton.unbind("<Button-1>")

        self.do_convert()
        # self.win.destroy()
        # root.destroy()
        # w.deiconify()

    def do_convert(self):

        self.scr.place(x=75, y=380)

        convert2or(project_dir, output_dir, exec_file, data_url, data_dir, self.scr)

        def leave():
            window.destroy()

        close_button = Button(window, text="Close", font=("Arial Black", 12), command=leave)
        close_button.place(x=400, y=680, width=120, height=40)

    def check_project_path(self, dirname):
        dir_path = dirname
        if not os.path.isdir(dir_path):
            if not messagebox.askretrycancel("Project directory", "Project directory does not exist!"):
                return -1
            else:
                return 0
        else:
            convert2py(dir_path, self.scr)
            return 1

    @staticmethod
    def check_output_path(dirname, workspace_dir=''):
        dir_path = dirname
        if dir_path == "":
            ans = messagebox.askokcancel("Output directory", "Warning: output path is empty, no files will be output")
            if ans:
                return 2  # empty output
            else:
                return 0

        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.abspath(os.curdir), dir_path)

        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass

        if dir_path.startswith(os.path.abspath(workspace_dir) + os.sep):
            return 1
        else:
            if messagebox.askretrycancel("Output Directory", "Output directory is NOT inside your project"):
                return 0
            else:
                return -1


def check_file_path(exe_file_path, path_exec_file_py, workspace_dir):
    file_path = path_exec_file_py
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.path.abspath(os.curdir), file_path)

    if (os.path.isfile(file_path) or os.path.isfile(exe_file_path)) and (
            file_path[-3:] == ".py" or file_path[-6:] == ".ipynb"):

        if file_path.startswith(os.path.abspath(workspace_dir) + os.sep):
            return 1
        else:
            if messagebox.askretrycancel("Entry-point File",
                                         "Entry-point file is outside project directory"):
                return 0
            else:
                return -1
    else:
        if messagebox.askretrycancel("Entry-point File",
                                     "Entry-point file is Neither a python file Nor an Ipython file"):
            return 0
        else:
            return -1


def convert2or(workspace_dir, output_path, exec_file_name, data_uri, data_path, scr):
    """
        Wrap and convert python3 '.py' files into an file that can be uploaded
        as a task by Nebula AI Orion Platform.
    """
    try:
        entry_filename = os.path.splitext(os.path.basename(exec_file_name))[0]
    except Exception as e:
        # display_message('Invalid arguments, {}'.format(e))
        err = 'Invalid arguments, {}'.format(e)
        display_error(scr, err)
        sys.exit(1)

    else:
        # Generate requirements.txt
        try:
            p = subprocess.Popen(["pip3", "install", "pipreqs"])
            p.wait()
            time.sleep(1)
            import pipreqs
        except ImportError as e:
            err = 'pipreqs installation failed: {}'.format(e)
            display_error(scr, err)
            # raise RuntimeError('pipreqs installation failed: {}'.format(e))
            sys.exit(1)
        else:
            time.sleep(1)
            try:
                p = subprocess.Popen(["pipreqs", "--force", workspace_dir])
                p.wait()
                time.sleep(2)

                # fix the bug raising from 'tensorflow', 'tensorflow_gpu'
                filename = os.path.join(workspace_dir, "requirements.txt")

                rw_file(filename, matplotlib="matplotlib", tensorflow_gpu="", tensorflow="tensorflow-gpu")
                remove_empty_lines(filename)
                # display_message("Generated 'requirements.txt' successfully!")
                txt = "Generated 'requirements.txt' successfully!"
                display_message(scr, txt)

            except Exception as e:
                err = "Generating 'requirements.txt' failed: {}".format(e)
                display_error(scr, err)
                sys.exit(1)
                # raise RuntimeError("Generating 'requirements.txt' failed: {}".format(e))
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
                    txt = "Generated 'params.json' successfully!"
                    display_message(scr, txt)

                except Exception as e:
                    err = "Generating 'params.json' failed: {}".format(e)
                    display_error(scr, err)
                    # sys.exit(1)
                    raise IOError("Generating 'params.json' failed: {}".format(e))

                else:
                    time.sleep(2)
                    try:
                        zip_folder_path = os.path.join(workspace_dir, os.pardir, "NBAI_task_files")

                        if not os.path.exists(zip_folder_path):
                            os.makedirs(zip_folder_path)

                        output_filename = str(entry_filename) + "_orion.zip"
                        zip_folder(workspace_dir, os.path.join(zip_folder_path, output_filename), scr)
                        txt = "Zipped files successfully!"
                        display_message(scr, txt)

                        display_message(scr, "Task has been converted successfully!")
                        display_message(scr, "This task is saved at: {}".format(
                            os.path.normpath(os.path.join(zip_folder_path, output_filename))))

                    except Exception as e:
                        err = "Zipping files failed: {}".format(e)
                        display_error(scr, err)
                        # sys.exit(1)
                        raise RuntimeError('Zipping files failed: {}'.format(e))
                    else:
                        try:
                            os.remove(os.path.join(workspace_dir, "params.json"))
                            os.remove(os.path.join(workspace_dir, "requirements.txt"))
                        except Exception as e:
                            err = 'Removing files failed: {}'.format(e)
                            display_error(scr, err)
                            # sys.exit(1)
                            raise RuntimeError('Removing files failed: {}'.format(e))


def display_message(scr, txt):
    scr.insert(END, '{} \n'.format(txt), "msg")
    scr.tag_config('msg', foreground='green')
    scr.see(END)
    scr.update()


def display_error(scr, err):
    scr.insert(END, '{} \n'.format(err), "err")
    scr.tag_config('err', foreground='red')
    scr.see(END)
    scr.update()


def get_files(folder, ext='.ipynb'):
    file_list = []
    for root_dir, dirs, files in os.walk(folder):
        for f in files:
            if f.endswith(ext):
                file_list.append(os.path.join(root_dir, f))
    return file_list


def convert2py(folder, scr):
    """
    Convert Jupyter Notebook '.ipynb' files to python3 '.py' files.
    """

    # parse converter arguments
    files = get_files(os.path.abspath(folder))
    try:
        s = subprocess.Popen(["pip3", "install", "nbconvert"])
        s.wait()
        time.sleep(1)
        import nbconvert
    except ImportError as e:
        err = 'nbconvert installation failed: {}'.format(e)
        display_error(scr, err)
        raise RuntimeError(err)
    try:
        p = list()
        for i in range(len(sys.argv) - 1):
            p.append(subprocess.Popen(["jupyter", "nbconvert", "--to", "python", files[i]]))
            p[i].wait()
        display_message(scr, 'Converted files successfully!')

    except Exception as e:
        err_message = "Converting files failed: {}".format(e)
        display_error(scr, err_message)
        raise RuntimeError(err_message)


def zip_folder(folder_path, output_path, scr):
    base_dir = os.path.abspath(folder_path)
    try:
        with zipfile.ZipFile(output_path, "w",
                             compression=zipfile.ZIP_DEFLATED) as zf:
            base_path = os.path.normpath(base_dir)
            for dirpath, dirnames, filenames in os.walk(base_dir):
                dirnames[:] = [d for d in dirnames if not d[0] == '.'
                               and "__pycache__" not in dirnames
                               and "venv" not in dirnames]
                for dir_name in sorted(dirnames):
                    path = os.path.normpath(os.path.join(dirpath, dir_name))
                    zf.write(path, os.path.relpath(path, base_path))

                filenames = [f for f in filenames if not f[0] == '.']
                for f_name in filenames:
                    path = os.path.normpath(os.path.join(dirpath, f_name))
                    if os.path.isfile(path):
                        filename, file_extension = os.path.splitext(f_name)
                        if str(file_extension) != ".ipynb":
                            zf.write(path, os.path.relpath(path, base_path))
    except Exception as message:
        display_error(scr, message)
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
            lines = [line.replace(line[:], "".join([v, "\n"]))
                     if "".join([k, "=="]) in line.lower() else line for line in fp]

            fp.seek(0)
            fp.truncate()
            fp.writelines(lines)


if __name__ == '__main__':
    project_dir = ""
    exec_file = ""
    output_dir = ""
    data_url = ""
    data_dir = ""

    window = Tk()
    gui = GUI(window)
    window.mainloop()
