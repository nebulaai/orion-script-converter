# Jupyter Notebook Converter 


### A python package to convert Jupyter Notebook ".ipynb" files into regular python ".py" files

Except converting file format, 
it will also create 'requirements.txt' and 'params.json' files. 
Then, it will zip all the files within your workspace to the folder 'taskFiles'
which can be uploaded directly to Orion platform.

### Requirements
- IPython 7.3.0 
- Python 3.5.2

  (tested versions)

### How to run

Simple and easy to run, like usual pip package installation. 

```
    $ cd workspace
    $ pip3 install git+https://github.com/nebulaai/orion-script-converter.git
    $ convert2py <filename1.ipynb, [filename.ipynb ...]>

```

- Enter your workspace. 
- Use the above commands to install Jupyter Notebook Converter package.

    **Note:** For the second command, 'pip3 install git+https: ...', 
    you may need to change it as 'pip install git+https: ...' depending on your pip command.
    
- After this package installed, you can use 'convert2py filename1.ipynb, filename2.ipynb, ...' 
to convert multiple '.ipynb' files into its corresponding '.py' files.
 
    **Note:** The first argument, 'filename1.ipynb' is required and executable. It is the entry-point of your project.
    
- All the files in your workspace folder(except '.ipynb' files) will be zipped
 as 'filename1_orion.zip' and saved in the folder 'task_files' which can be uploaded directly to Orion platform.
 
 
### Help
- Get help

`$ convert2py -h`

- Get package information

`$ pip3 show convert2py  or $ pip show convert2py`


- Remove this package

`$ pip3 uninstall convert2py or $ pip uninstall convert2py`



