# United Nations Project on Mobility

Background
----------------------
Employees periodically have reformation of their work places. These reformation of new work places for employees are formed according to three of their preferred work places and the score thay have accumulated.

Problem
----------------------
The reformation of new work places to each employee must be a valid reformation according to the constraints. Employees with higher score is given a higher probability to be assigned to work places according to there preferrences. There must be as many possible reformation within the given employees.

Approach
----------------------
Record all the existing cycles and the scores from each vertices relatd to the cycle within the given graph through DFS. Score of a cycle is calculated by the existing number of vertices in the total graph to the power of the score assigned to the current vertex related to the current cycle.

Building Executable File
----------------------
1. cd src
2. pyinstaller -F -w main.py