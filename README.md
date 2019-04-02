# Orion-Script-Converter


### A python package to convert python3 project into a NBAI task that can be executed by Nebula AI Worker.

This package will warp and convert your AI project into a NBAI task. 
The sub-folders and files inside your project folder will be assumed 
as part of your source codes and will be converted to a '.zip' file, excluding:
   * hidden folders(e.g. '.git' or '.idea' folder) 
   * python '__pycache__' folder
   * Jupyter Notebook '.ipynb' files
   
This package includes two commands:
```
- convert2or: Warp and convert python3 project files into a NBAI task that can be uploaded
 directly via NBAI Orion Platform and executed by Nebula AI Worker.
    
- convert2py: Convert Jupyter Notebook '.ipynb' files into python3 '.py' files.
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

**Note:** 

Depending on your system, you may need to use 'pip install git+https: ...', 
instead of 'pip3'. Also, you may need to add 'sudo' at the beginning of this command.

 
### Package Info

It is helpful to verify your installation: 

```
    $ pip3 show convert2orion  
```

output response:


```
    ---
    Metadata-Version: 1.0
    Name: convert2orion
    Version: 0.0.1
    Summary: Warp and convert Python3 project files into a NBAI task 
             that can be uploaded directly via NBAI Orion Platform and executed by Nebula AI Worker.
    Home-page: https://github.com/nebulaai/orion-script-converter
    Author: Eric Pang
    Author-email: UNKNOWN
    License: MIT
    Location: /home/hp/.local/lib/python3.5/site-packages
    Requires: pipreqs, nbconvert
    Classifiers:
    Entry-points:
      [console_scripts]
      convert2or = converter.converter:convert2or
      convert2py = converter.converter:convert2py
  
```

### How to use

- For project in Python3:

```
    $ cd my_project   
    my_project$ convert2or
``` 

  **Note:**

    - Enter your project
    - Type command 'convert2or'
    
        Input parameters according to the prompt:
        1. 
        (Required) Project path: 
	    (Press 'Enter' or '.' for the current directory, '..' for the parent directory of the current folder): 
        
        Input the Python3 project path, either relative path or absolute path. 
        'Enter' or '.' represents the current folder(default) and the '..' means the parent folder 
        of the current path.
        
        2.
        (Required) entry-point file path(executable file path):
        
        Input the name of entry-point file. This path should inside the Project path.
        
        3.
        Data configuration: 
	        Do you have external data(data stored outside your project database)
	        that needs to be downloaded from a specific uri (y/n)?
	        
        Set data configuration. If 'y', the following two inputs prompt. Otherwise, this step will skip.
        
            External data uri:  
            
            Input the data uri to get your external data
            
            Path to save the downloaded data within your project:
            
            Input the path(inside your project) to save your downloaded external data.  
            
        4. 
        Path for the task results(project output directory):
        
            Your project output directory holds your output files. 
            If you have such a directory in your project, input it here. 
            Otherwise, there will be no output files.
            
        5. A NBAI task will be created and saved in the 'task_files' folder 
           which is a sibling folder of your project. 

        
- For project in Jupyter Notebook:

    You have two ways to convert your Jupyter Notebook '.ipynb' files into a Python3 '.py' file:
    
    1. In your Jupyter Notebook workspace, open a '.ipynb' file, select File -> Download as | Python, 
    a '.py' with the same file name will create.
    
    2. Use the following command
```
    $ cd my_project   
    my_project$ convert2py <filename1.ipynb, [filename.ipynb ...]>     # for multi-file conversion
```

### Help
- Get help

`$ convert2py -h`
`$ convert2or -h`

- Get package information

`$ pip3 show convert2orion`

- Remove this package

`$ pip3 uninstall convert2orion`

### Samples
[Tutorial using real AI projects](./convert2orion_samples.md)

