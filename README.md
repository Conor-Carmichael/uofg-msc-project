# MSc Project for the University of Glasgow
## MSc in Data Science
A robotics simulation project for completion of the MSc Data Science program at the University of Glasgow.

For a description [will be updated following submission of project]
www.conorcarmichael.com/msc-project.html

Before I am able to refacto some code, using the repository may be a bit tricky.

You need to build openvslam (https://openvslam.readthedocs.io/en/master/installation.html), but also have the ros folder from this repository at openvslam/ros, the camera configurations in the openvslam/build/ folder, and in the base directory of the project all the python scripts.


Notes:
Until I have time to refactor some code, many file paths are dependent on my base file path. You will need to in many python files change "/home/conor/msc-project/"


Files to change:
- map_pipeline.py: line 61
- frames_to_mp4.py: line 8
- navigation_controller.py: line 120
- navigation_tracker.py: line 39
- navigate.launch: line 44
- aal_bot_processor.py: lines 17, 18, 19, 20, 45, 59