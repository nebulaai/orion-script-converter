# Orion-Script-Converter Version 0.0.1


### A python package to convert python3 project files into a NBAI task that can be executed by Nebula AI Worker.
  
This package includes two commands:
```
- convert2py: Convert Jupyter Notebook '.ipynb' files into python3 '.py' files.
    
- convert2or: Warp and convert python3 project files into a NBAI task that can be uploaded directly via NBAI Orion Platform
     and executed by Nebula AI Worker.

```
    

### Requirements
- IPython 7.3.0 
- Python 3.5.2

  (tested versions)

### Installation

```
    $ pip3 install git+https://github.com/nebulaai/orion-script-converter.git  
    or
    $ pip install git+https://github.com/nebulaai/orion-script-converter.git  
    
```

**Note:** Depending on your system installation, you may need to use 'pip install git+https: ...', 
instead of 'pip3 install git+https: ...'. Also, you may need to add 'sudo' at the beginning of this command.

 
### Package Info

It is helpful to verify your installation: 

```
    $ pip3 show convert2orion  
```

output response:


```
    $ pip3 show convert2orion  
```


$ cd my_project
$ convert2py <filename1.ipynb, [filename.ipynb ...]>


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



