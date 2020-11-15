# Hack112
Resnik 4 Team Hack112 Project

# make sure to zip the directory before submission!


Welcome to StudyBuddy! Your very own personal study buddy! StudyBuddy has two functionalities: An analytics mode, and a buddy mode. 

The analytics mode uses a Perceptron Machine Learning Classifier to determine which areas of studying are most impactful. It first initializes this through self calibration when the user reports their style of learning. Your percentages and educational data are displayed on the analytics page.

The Buddy mode utilizes openCV to monitor the user as they study. A "focus percentage" is calculated at the end of every study session, and this is fed back into the machine learning pipeline in order to update the user's analytics.

The following modules are required:
Cv2
numPy
Tinker
Pickle
PIL
Dataclasses
Joblib
Sklearn
Dlib
pip install GazeTracking
To run this application, use main.py. If you are on a Mac, make sure you are running with root permissions on vsCode.
