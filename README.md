# P2P Decentralized Network with BitTorrent Protocol

Please use this README file to provide the following documentation for this project:

* Your name and student id
* General description of the project (a few sentences)
* If you used external Python modules/libraries. Provide a requirements.txt file  
* Python version and compatibility issues (if any)
* Clear and specific instructions about how to run your project. If your project does not run or contains errors, you'll get a 0 in the project no matter how much work you put on it. So, test your code properly and make sure that it runs without errors.
* A few sentences about all the challenges you found during the implementation of this project and how you overcame them. Please be honest here. 

## Note that failure to provide the above docs will result in a 30% deduction in your final grade for this project. 

# Project Guidelines 

A document with detailed guidelines (P2P.pdf) to implement this project can be found in the 'help' folder and posted on iLearn

# The Tit-For-Tat Transfer Protocol

Your P2P program must implement the Tit-For-Tat transfer protocol. This protocol only allows a peer to be downloading/uploading
data from/to a maximum of four other peers or seeders; the top three with maximum upload rate, and a a random chosen peer. 
The goal of connecting to a random peer/seeder is to increment the participation of rarest peers in the network. This situation
must be reevaluated every 30 seconds because peers disconnect and connect all the time during the sharing process. 

See P2P.pdf for more info about how to compute temporal upload and downloads rates. 

# HTPBS for Showing Pieces Downloading/Uploading Progresses 

In order to show the progress of the pieces your peer is uploading or downloading to/from the P2P network, you can use the htpbs (horizontal threaded progress bars) library. This library tracks the progress of threaded jobs and is customizable to for your project. Exactly what you need for this project!. For more info about this library: https://pypi.org/project/htpbs/

### Install with PIP

```python 
pip3 install htpbs
```

# Grading Rubric: 

1. This project is worth 25% of your final grade, and will be graded using a point scale where the 
maximum possible grade is 100 points. For example, a grade of 80/100 in this project will be converted to 
0.80 * 25% = 20% of 25%

2. The project has one extra-credit part: scaling the capability of the project to support sharing files in 
more than two swarms (5%). 

3. If the peer runs without errors, it connects to at least 2 peers that are already connected to the 
network, and you provided all the docs requested at the beginning of this README page then (+50)

4. If any of the requirements from step 3 is missing, I will apply a grade (at my discretion) depending on how much 
work the student has done in the project. However, this grade will be way below the 50 points threshold. 
Please make sure to test your project properly before submission to avoid this situation. 

5. For each part of the program that is correctly implemented (after step 3 is successfully executed), then (+10) points
Note that I will give also partial credit if there are parts that are not fully implemented but have some work done. 
Parts of the program are: (1) the torrent file is scanned correctly, (2) the tracker works as expected, (3) the 
Tit-for-Tac protocol implemented correctly (4) the blocks
and pieces are downloaded/uploaded/saved as expected and messages are correctly sent between peers, and
(5) real time progress of your program while downloading and uploading pieces is shown on screen. 

7. Late submissions won't be accepted since the due date for this project is set to the last day of class.

# Submission Guidelines 

This project is due the last day of the semester. After you complete and test your project, go to the assignments table, 
located in the main README file of this repository, and set this project to "done" or "completed". 
Failure to do that will result in your project not being graded because I will assume that the project 
hasn't been submitted. No exceptions here!!!. 

Good luck!!!
  

 


    


