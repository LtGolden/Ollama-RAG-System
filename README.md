# Ollama-RAG-System
This is a simple program that uses a locally hosted ollama model to give you answers based on documentation you provide. You fill a file full of PDFs you want your AI to use as a reference, point it to that file with this program, and it will use those references when answering your questions

#Performance/Limitations
This RAG system only supports PDFs, but that could be easily changed if you need to change it
The main reason I am even bothering to post this is this version contains caching, so you could have huge amounts of PDF files, but after the first run of this program(which will take a while), you will have a snappy AI. On first setup it reads through and divides all those files, and caches the paths, so that it can view them very quickly at a later time.

#Using the Program
To use the program, you will have to do 3 things after downloading.
1. Type in where your file full of PDFs is located where it says "YOUR FILE LOCATION HERE" in the code.
2. Type in which ollama model you are running in the code where it says "YOUR MODEL HERE".
3. Open a command window, type cd "Whatever file the program is in", and type python pyrag22.py, and then hit enter
