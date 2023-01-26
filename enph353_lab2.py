# -*- coding: utf-8 -*-
"""ENPH353_Lab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17c8Hxi_vKlTI5ex1yA2uZZGoHpRYHHJl
"""

from numpy.lib.function_base import median
import cv2
from google.colab.patches import cv2_imshow
import numpy as np

# Opens/captures the video to allow access to frames, and so on
vid = cv2.VideoCapture("/content/sample_data/raw_video_feed.mp4")

width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Initialize where you output/write the final edited frames to
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output = cv2.VideoWriter('output_video_feed.mp4', fourcc, 20.0, (width, height), isColor=True)

while True:
    ret, frame = vid.read()

    if ret:

      # Change the video frame into gray scale
      # Filter each video frame by looking at surrounding pixel neighbours and determining
      # whether or not to change the pixel color
      gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      median_filtered_frame = cv2.medianBlur(thresholded_frame, 3)

      # Change the video frame into black and white
      _, thresholded_frame = cv2.threshold(median_filtered_frame, 128, 255, cv2.THRESH_BINARY)

      # Determine the edges and centerpoint of the line using the last 30 rows of the frame
      edges = cv2.Canny(thresholded_frame[height-30:,:], 100, 200)
      _, non_zero_x = np.nonzero(edges)
      center_x = int(np.mean(non_zero_x))

      # Place a red ball on the line's centerpoint near the bottom
      frame = cv2.circle(frame, (center_x, height-35), 30, (0, 0, 255), -1)

      output.write(frame)
    
    # Stop reading frames once video has been fully ran
    if not ret:
      break   

    # Stop reading frames if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

output.release()
vid.release()
cv2.destroyAllWindows()
