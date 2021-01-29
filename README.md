# Fasta_EasySplit V2.0
A python3 script to easily and safely split a fasta file into multiple parts

##USAGE:

  -h, --help    ---> show this help message and exit
  
  -f FASTA_FILE, --fas FASTA_FILE    ---> Fasta file to split [REQUIRED]
                        
  -s SPLIT_LEVEL, --split SPLIT_LEVEL    ---> Number of files to generate (int > 1) [REQUIRED]
                        
          
          
The output will be SPLIT_LEVEL files with an ordered number extension (file.fasta.1, file.fasta.2, etc.)

This program first have to count the sequence in the fasta file. If you are on a POSIX system, the program will use subprocess to launch a grep and a wc command (which is very fasta and low memory requirement) to count the sequence. If you are on a Windows system (or any system that don't support grep or wc), the program will use an internal counting method which takes more time.

Also note the this program will NOT import the file into memory, so it can be used on very large files.

This is a very useful program for HPC processing 

