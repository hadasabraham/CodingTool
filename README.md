# CodingTool
Coding Tool for Technion
The GUI of the tool was developed with PyQt5, PySide2.

# Running The App

First, install python 3.8.6. This is the version best compatible with some of the other libraries we use.

Install the following (pip install):

* PyQt5
* PySide2

Compile the Clustering-Correcting-Code algorithm:

the CCC algorithm is a .cpp file so in order to compile it you need to run the following lines : 

    g++ -std=c++0x -O3 -g3 -c -fmessage-length=0 -o "SourceCode\main.o" "SourceCode\main.cpp" 
    g++ -o CCC.exe "SourceCode\main.o"

this is the path you need to be on in order to compile it:

algorithms\clustering-correcting-codes-master

for your convenience this there is a **compile.bat** file that runs those commands (relevant for windows users).

Then run the app:

    python main.py
or

    python3 main.py

**Notice**: the project needs to be saved or run on a path **without spaces**

