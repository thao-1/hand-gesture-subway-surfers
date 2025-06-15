# Hand Gesture Temple Run Controller

This project is used to control Temple Run using hand gestures captured through your webcam. It uses MediaPipe for hand tracking and PyAutoGUI for game control.

## Requirements

- Python 3.7 or higher
- Webcam
- Temple Run game (PC version)

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv temple_run_env

# On Windows:
temple_run_env\Scripts\activate

# On macOS/Linux:
source temple_run_env/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Make sure Temple Run is running and in focus
2. Run the controller:
```bash
python hand_gesture_controller.py
```

## Controls

- Swipe Left: Move left in the game
- Swipe Right: Move right in the game
- Swipe Up: Jump
- Swipe Down: Slide/roll
- Make Fist: Alternative jump command
- Press 'q' to quit

## Tips for Better Detection

1. Keep your hand in the center of the camera view
2. Make clear, deliberate gestures
3. Avoid rapid movements
4. Ensure good lighting
5. Keep background simple

## Troubleshooting

### Camera Issues
- Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` or `cv2.VideoCapture(2)`
- Check if other applications are using the camera

### Gesture Detection Issues
- Adjust lighting
- Move closer/farther from camera
- Run the calibration mode (uncomment lines in main)

### Game Control Issues
- Make sure Temple Run window is active and in focus
- Check if the game uses different key bindings
- Adjust the action_cooldown if actions are too fast/slow

### PyAutoGUI Security Error (macOS)
- Give Python accessibility permissions
- Go to System Preferences > Security & Privacy > Accessibility

## Customization

You can adjust the following parameters in the code:
- `swipe_threshold`: Minimum pixel movement for swipe detection (default: 30)
- `action_cooldown`: Time between actions in seconds (default: 0.3)
- Key bindings in the `perform_game_action()` method

## Features

- Real-time hand tracking with MediaPipe
- Gesture smoothing to prevent false positives
- Visual feedback with hand landmark drawing
- Calibration mode for sensitivity adjustment
- Robust fist detection algorithm 