## Calibration

- Step 1 — Enable calibration mode

In hand_tracking.py find the get_all_angles function and add this temporary print line after relative_dist is calculated:

python
print(f"{finger}: {relative_dist:.4f}")

- Step 2 — Find your open hand values

Run the script and hold your hand fully open and flat in front of the camera. Note the values printing for each finger, these are your maximum distances.

- Step 3 — Find your closed hand values

Make the tightest fist you can and note the values printing for each finger, these are your minimum distances.

- Step 4 — Update the calibration values

In hand_tracking.py find these dictionaries and replace with your measured values:

python
finger_max = {
    "thumb":  0.7260,  # your open thumb value
    "index":  0.8515,  # your open index value
    "middle": 0.9379,  # your open middle value
    "ring":   0.8,     # your open ring value
    "pinky":  0.65,    # your open pinky value
}

finger_min = {
    "thumb":  0.2013,  # your closed thumb value
    "index":  0.3214,  # your closed index value
    "middle": 0.2909,  # your closed middle value
    "ring":   0.2562,  # your closed ring value
    "pinky":  0.2065,  # your closed pinky value
}

- Step 5 — Remove the temporary print line

Delete the calibration print line you added in Step 1.

- Step 6 — Verify calibration

Run the script and confirm:

Open hand  = all fingers read close to 0°
Tight fist = all fingers read close to 180°

Tips

Keep your hand at a consistent distance from the camera during calibration
Good lighting gives more consistent readings
If a finger feels unresponsive its min and max values are probably too close together — spread them further apart
The thumb is the trickiest finger, if it feels off try adjusting its values independently first

