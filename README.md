# train_sim

This is a Python train system using Pygame. It currently involves trains travelling along tracks from station to station, often stopped by signals to prevent collision. The signals 

## Prerequisites
Ensure you have Python 3 and Pygame installed.


## Running
Ensure you have the following files downloaded in the same folder:
- Track.py
- TrackNode.py
- Train.py
- train_sim.py

Run
```
python3 train_sim.py
```

## Usage
Currently, the main interactive element is the signals. Signals can be automatic or manual - hover over them to find out which they are set to.

To change whether signals are automatic or manual, right-click them. While signals are set to manual, you can left-click them to change their colour between red (to stop trains) or green (to allow trains to pass through).

Signals can also be linked together so that when they are set to automatic, if one signal is red, all of them will turn red until they can turn green again.

You can also hover over stations to find out their names, and hover over trains to see the train's name and where it is headed.
