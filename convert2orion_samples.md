
# Samples of converting AI models to Nenula AI tasks 
Created by weigang Li

This tutorial aims to facilitate Nebula AI users to convert their 
projects into Nebula AI tasks using real examples.

### How does it work? 
As Nebula AI User, only three steps you need to do:

1. Convert your AI project into a Nebula AI task(a '.zip' file).
2. Upload this task via Orion Platform and have it executed by a Nebula AI Worker.
3. Download the result. 


### Installation 
Install the 'convert2orion' package:

```
    $ pip3 install git+https://github.com/nebulaai/orion-script-converter.git  
    or
    $ pip install git+https://github.com/nebulaai/orion-script-converter.git  
    
    Note:
    Depending on your system, you may need to use 'pip install git+https: ...', 
    instead of 'pip3'. Also, you may need to add 'sudo' at the beginning of this command.
    
```
check the package information(optional)
```
    $ pip3 show convert2orion 
     
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

### Example 1: Mnist
Overview: This is an image process model. 

Model Input: MNIST dataset embedded in tensorflow.

Model Output: Generated handwritten digital images. For testing purpose, training epoch was set to 10.


##### Step 1: Convert AI project into a Nebula AI task. 

Supposing this project is saved on the local disk at '/home/testuser/dcgan',
enter this project folder and type the 'convert2or' command.

```
$ cd /home/testuser/dcgan/
$ convert2or
```

As prompted, necessary parameters need to be defined as the following: 
```
(Required) Project path:
        (Press 'Enter' or '.' for the current directory, '..' 
        for the parent directory of the current folder):     # press 'Enter' or '.' for the current folder
     
    (Required) Entry-point file path(executable file path): DCGAN_Demon.py   
    # 'DCGAN_Demon.py' is the entry_point file 
     
    Data configuration:
        Do you have external data(data stored outside your project database)
        that needs to be downloaded from a specific uri (y/n)? n   # no external data
 
    Path for the task results(project output directory): mnist
        # output_path is '/home/testuser/dcgan/mnist'        
        # the output files will be saved in this output_path that can be downloaded by Nebula AI User.
```
The response looks like:

```      
    INFO: Successfully saved requirements file in /home/testuser/dcgan/./requirements.txt
    Generated 'requirements.txt' successfully!
    Generated 'params.json' successfully!
    Zipped files successfully!
```
       
After this step done successfully, a "task_files" folder is created 
on the same hierarchical path level as your project folder(sibling folders).  
The *'entry_point filename_orion.zip'* file inside this "task_files" folder
is the converted Nebula AI task ready to be uploaded via Nebula Orion Platform and executed by Nebula AI Worker.
    
In this example, the converted task file is: 
  
```
    $ cd ../task_files
    $ ls
   
    DCGAN_Demon_orion.zip
``` 

##### Step 2: Upload this task via Orion Platform and have it executed by a Nebula AI Worker. 
[Sign in as Nebula AI User](https://nbai.io/dashboard/#/login)


##### Step 3: Download the result.

Besides your own output files defined in the 'output_path' when you input above, 
other two log files will be also included for your convenience and debugging purpose:

1. NBAI_script.log: This log file records the execution progress. It looks like:
```
time="2019-04-01 13:17:44" level=INFO msg="Welcome to Nebula AI Worker: 
        Worker id: (0xE40c23cbEc97Ab0a63378954b827c04841C68370), 
        Task id: (0x69F8F1A68C608Bf4B27F4Dd85e9A1Ac3d8cb67a3)"
time="2019-04-01 13:17:44" level=INFO msg="Starts to download task script..."
time="2019-04-01 13:17:45" level=INFO msg="Script downloaded successfully."
time="2019-04-01 13:17:46" level=INFO msg="Starts to install packages from 'requirements.txt'..."
time="2019-04-01 13:17:55" level=INFO msg="Packages installed successfully."
time="2019-04-01 13:17:55" level=INFO msg="Starts to execute script..."
time="2019-04-01 13:20:25" level=INFO msg="Script is executed"
time="2019-04-01 13:20:25" level=INFO msg="The result of 
        Task (0x69F8F1A68C608Bf4B27F4Dd85e9A1Ac3d8cb67a3) has been executed by 
        Worker (0xE40c23cbEc97Ab0a63378954b827c04841C68370)."

```
2. NBAI_output.log: This log file records the screen output during execution.
When there is no screen output, this file will be an empty file. It looks like:

```
Downloading data from https://s3.amazonaws.com/img-datasets/mnist.npz

    8192/11490434 [..............................] - ETA: 37s
  106496/11490434 [..............................] - ETA: 8s 
  458752/11490434 [>.............................] - ETA: 3s
  614400/11490434 [>.............................] - ETA: 3s
 1515520/11490434 [==>...........................] - ETA: 1s
 2367488/11490434 [=====>........................] - ETA: 1s
 2891776/11490434 [======>.......................] - ETA: 1s
 3383296/11490434 [=======>......................] - ETA: 0s
 3973120/11490434 [=========>....................] - ETA: 0s
 4235264/11490434 [==========>...................] - ETA: 0s
 4718592/11490434 [===========>..................] - ETA: 0s
 5120000/11490434 [============>.................] - ETA: 0s
 5505024/11490434 [=============>................] - ETA: 0s
 5939200/11490434 [==============>...............] - ETA: 0s
 6356992/11490434 [===============>..............] - ETA: 0s
 6750208/11490434 [================>.............] - ETA: 0s
 7168000/11490434 [=================>............] - ETA: 0s
 7593984/11490434 [==================>...........] - ETA: 0s
 8011776/11490434 [===================>..........] - ETA: 0s
 8445952/11490434 [=====================>........] - ETA: 0s
 8830976/11490434 [======================>.......] - ETA: 0s
 9281536/11490434 [=======================>......] - ETA: 0s
 9609216/11490434 [========================>.....] - ETA: 0s
10100736/11490434 [=========================>....] - ETA: 0s
10444800/11490434 [==========================>...] - ETA: 0s
10919936/11490434 [===========================>..] - ETA: 0s
11247616/11490434 [============================>.] - ETA: 0s
11493376/11490434 [==============================] - 1s 0us/step
2019-04-01 13:18:01.015257: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2019-04-01 13:18:01.076250: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:898] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2019-04-01 13:18:01.076574: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1356] Found device 0 with properties: 
name: GeForce GTX 1070 major: 6 minor: 1 memoryClockRate(GHz): 1.797
pciBusID: 0000:01:00.0
totalMemory: 7.93GiB freeMemory: 6.81GiB
2019-04-01 13:18:01.076587: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1435] Adding visible gpu devices: 0
2019-04-01 13:18:01.252052: I tensorflow/core/common_runtime/gpu/gpu_device.cc:923] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-04-01 13:18:01.252083: I tensorflow/core/common_runtime/gpu/gpu_device.cc:929]      0 
2019-04-01 13:18:01.252090: I tensorflow/core/common_runtime/gpu/gpu_device.cc:942] 0:   N 
2019-04-01 13:18:01.252221: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1053] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 6572 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1070, pci bus id: 0000:01:00.0, compute capability: 6.1)
2019-04-01 13:18:01.337330: W tensorflow/core/framework/allocator.cc:101] Allocation of 188160000 exceeds 10% of system memory.
WARNING:tensorflow:Deprecation Warning: create_summary_file_writer was renamed to create_file_writer
[2K
[2K
Time taken for epoch 1 is 16.73725652694702 sec
[2K
[2K
Time taken for epoch 2 is 14.104169130325317 sec
[2K
[2K
Time taken for epoch 3 is 13.913076639175415 sec
[2K
[2K
Time taken for epoch 4 is 13.954521894454956 sec
[2K
[2K
Time taken for epoch 5 is 14.022923469543457 sec
[2K
[2K
Time taken for epoch 6 is 14.140827417373657 sec
[2K
[2K
Time taken for epoch 7 is 14.047441244125366 sec
[2K
[2K
Time taken for epoch 8 is 14.34998631477356 sec
[2K
[2K
Time taken for epoch 9 is 14.30287480354309 sec
[2K
[2K
Time taken for epoch 10 is 14.158042907714844 sec
[2K
[2K

``` 

### Example 2: Word2vec

Overview: This is an word2vec training model. It assigns a specific vector for each word in vocabulary. 

Model Input: Text data of 100 mb size downloaded from a specific url.

Model Output: The trained word2vec library.


##### Step 1: Convert AI project into a Nebula AI task. 
Supposing this project is saved on the local disk at '/home/testuser/word2vec',
enter this project folder and type the 'convert2or' command.

```
$ cd /home/testuser/word2vec/
$ convert2or
```
```
    (Required) Project path:
    (Press 'Enter' or '.' for the current directory, '..' for the parent directory of the current folder):
    # press 'Enter' or '.' for the current folder
    
    (Required) Entry-point file path(executable file path): word2vec_basic.py        
    # 'word2vec_basic.py' is the entry_point file 
    
    Data configuration:
        Do you have external data(data stored outside your project database)
        that needs to be downloaded from a specific uri (y/n)? y    # has external data
 
        External data uri: http://mattmahoney.net/dc/text8.zip      # external data download url                
 
        Path to save the downloaded data within your project: datadir     # local saving path for the external data 
 
    Path for the task results(project output directory): log  
    # output_path is '/home/testuser/word2vec/log'        
    # the output files will be saved in this output_path that can be downloaded by AI user.
    
```
The response looks like:  

```       
    INFO: Successfully saved requirements file in /home/testuser/word2vec/./requirements.txt
    Generated 'requirements.txt' successfully!
    Generated 'params.json' successfully!
    Zipped files successfully!
```

The task is named as 'word2vec_basic_orion.zip', also in the "task_files" folder.
    
##### Step 2: Upload this task via Orion Platform and have it executed by a Nebula AI Worker
[Sign in as Nebula AI User](https://nbai.io/dashboard/#/login)


##### Step 3: Download the result.
The downloaded results:

1. NBAI_script.log:
```
time="2019-03-29 13:51:31" level=INFO msg="Welcome to Nebula AI Worker: 
        Worker id: (0xa9722f52559eE32136807A15E07808A6DDd4248A), 
        Task id: (0x180Fa0079510ABec5829dcACdC5bDcCde9009216)"

time="2019-03-29 13:51:31" level=INFO msg="Starts to download task script..."
time="2019-03-29 13:51:31" level=INFO msg="Script downloaded successfully."
time="2019-03-29 13:51:32" level=INFO msg="Starts to install packages from 'requirements.txt'..."
time="2019-03-29 13:51:38" level=INFO msg="Packages installed successfully."
time="2019-03-29 13:51:38" level=INFO msg="Starts to download data resource..."
time="2019-03-29 13:51:49" level=INFO msg="Data resource downloaded successfully."
time="2019-03-29 13:51:49" level=INFO msg="Starts to execute script..."
time="2019-03-29 13:53:04" level=INFO msg="Script is executed"
time="2019-03-29 13:53:04" level=INFO msg="The result of 
        Task (0x180Fa0079510ABec5829dcACdC5bDcCde9009216) has been executed by 
        Worker (0xa9722f52559eE32136807A15E07808A6DDd4248A)."

```
2. NBAI_output.log: 

```
2019-03-29 13:51:58.935655: I tensorflow/core/platform/cpu_feature_guard.cc:140] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
2019-03-29 13:51:59.065577: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1356] Found device 0 with properties: 
name: GeForce GTX 1080 Ti major: 6 minor: 1 memoryClockRate(GHz): 1.6705
pciBusID: 0000:02:00.0
totalMemory: 10.92GiB freeMemory: 10.56GiB
2019-03-29 13:51:59.188321: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1356] Found device 1 with properties: 
name: GeForce GTX 1080 Ti major: 6 minor: 1 memoryClockRate(GHz): 1.6705
pciBusID: 0000:65:00.0
totalMemory: 10.91GiB freeMemory: 10.29GiB
2019-03-29 13:51:59.306523: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1356] Found device 2 with properties: 
name: GeForce GTX 1080 Ti major: 6 minor: 1 memoryClockRate(GHz): 1.6705
pciBusID: 0000:66:00.0
totalMemory: 10.92GiB freeMemory: 10.56GiB
2019-03-29 13:51:59.308180: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1435] Adding visible gpu devices: 0, 1, 2
2019-03-29 13:51:59.887832: I tensorflow/core/common_runtime/gpu/gpu_device.cc:923] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-03-29 13:51:59.887875: I tensorflow/core/common_runtime/gpu/gpu_device.cc:929]      0 1 2 
2019-03-29 13:51:59.887882: I tensorflow/core/common_runtime/gpu/gpu_device.cc:942] 0:   N Y Y 
2019-03-29 13:51:59.887886: I tensorflow/core/common_runtime/gpu/gpu_device.cc:942] 1:   Y N Y 
2019-03-29 13:51:59.887890: I tensorflow/core/common_runtime/gpu/gpu_device.cc:942] 2:   Y Y N 
2019-03-29 13:51:59.888265: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1053] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 10220 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1080 Ti, pci bus id: 0000:02:00.0, compute capability: 6.1)
2019-03-29 13:51:59.985336: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1053] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:1 with 9958 MB memory) -> physical GPU (device: 1, name: GeForce GTX 1080 Ti, pci bus id: 0000:65:00.0, compute capability: 6.1)
2019-03-29 13:52:00.091344: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1053] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:2 with 10220 MB memory) -> physical GPU (device: 2, name: GeForce GTX 1080 Ti, pci bus id: 0000:66:00.0, compute capability: 6.1)
Data size 17005207
Initialized and begin training
Average loss at STEPS  0.0 % :  281.6107482910156
Average loss at STEPS  5.0 % :  143.49468838500977
Average loss at STEPS  10.0 % :  81.76093859100342
Average loss at STEPS  15.0 % :  60.24954637622833
Average loss at STEPS  20.0 % :  46.08434648561477
Average loss at STEPS  25.0 % :  35.58919999504089
Average loss at STEPS  30.0 % :  31.680071479320524
Average loss at STEPS  35.0 % :  25.19672976732254
Average loss at STEPS  40.0 % :  21.584625477313995
Average loss at STEPS  45.0 % :  19.174549116134642
Average loss at STEPS  50.0 % :  16.20298972415924
Average loss at STEPS  55.0 % :  15.113323912143708
Average loss at STEPS  60.0 % :  13.351690188407899
Average loss at STEPS  65.0 % :  12.257497084617615
Average loss at STEPS  70.0 % :  11.501127092838287
Average loss at STEPS  75.0 % :  10.322887999534608
Average loss at STEPS  80.0 % :  9.817020177841187
Average loss at STEPS  85.0 % :  8.631774385929107
Average loss at STEPS  90.0 % :  8.138056858778
Average loss at STEPS  95.0 % :  8.270061221122742
training done
trainng time:  57.315256118774414
Start plotting
plotting time:  6.2 seconds
Plot saved.

```

### Example 3: QuantAI
Overview: This is a prediction model. 

Model Input: USDT_ETH data fetched from [poloniex.com](https://www.poloniex.com).

Model Output: 
1. Prediction of the next 4 periods (300 seconds per period) in '.json' format.  
2. Images of the result in '.png' format.

##### Step 1: Convert AI project into a Nebula AI task.  

Supposing this project is saved on the local disk at '/home/testuser/QuantAI',
enter this project folder and type the 'convert2or' command.
```
$ cd /home/testuser/QuantAI/
$ convert2or

(Required) Project path:
        (Press 'Enter' or '.' for the current directory, '..' 
        for the parent directory of the current folder):     # press 'Enter' or '.' for current folder
     
    (Required) Entry-point file path(executable file path): main.py   # 'main.py' is the entry_point file 
     
    Data configuration:
        Do you have external data(data stored outside your project database)
        that needs to be downloaded from a specific uri (y/n)? n   # no external data
 
    Path for the task results(project output directory): Results
        # output_path is '/home/testuser/QuantAI/Results'        
        # the output files will be saved in this output_path that can be downloaded by AI user.
```
        
output is similar to the following:
```      
    INFO: Successfully saved requirements file in /home/testuser/QuantAI/./requirements.txt
    Generated 'requirements.txt' successfully!
    Generated 'params.json' successfully!
    Zipped files successfully!
```

The task is named as 'main_orion.zip', in the "task_files" folder.
    
##### Step 2: Upload this task via Orion Platform and have it executed by a Nebula AI Worker
[Sign in as Nebula AI User](https://nbai.io/dashboard/#/login)


##### Step 3: Download the result.
The downloaded results:

1. NBAI_script.log: This log file records the execution progress. It looks like:
```
time="2019-03-29 13:49:23" level=INFO msg="Welcome to Nebula AI Worker: 
        Worker id: (0xE40c23cbEc97Ab0a63378954b827c04841C68370), 
        Task id: (0x4915619f5641ca99FC40B5337E028113E4020431)"
time="2019-03-29 13:49:23" level=INFO msg="Starts to download task script..."
time="2019-03-29 13:49:23" level=INFO msg="Script downloaded successfully."
time="2019-03-29 13:49:24" level=INFO msg="Starts to install packages from 'requirements.txt'..."
time="2019-03-29 13:49:38" level=INFO msg="Packages installed successfully."
time="2019-03-29 13:49:38" level=INFO msg="Starts to execute script..."
time="2019-03-29 13:49:55" level=INFO msg="Script is executed"
time="2019-03-29 13:49:55" level=INFO msg="The result of 
        Task (0x4915619f5641ca99FC40B5337E028113E4020431) has been executed by 
        Worker (0xE40c23cbEc97Ab0a63378954b827c04841C68370)."

```
2. NBAI_output.log: No screen output, empty file.
 