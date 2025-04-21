import cv2
import numpy as np
import time

# --- STEP 1: Load Video ---
video_path = "C:/Users/mbat/OneDrive/Desktop/kml file/video.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Cannot open video file:", video_path)
    exit()

frame_list = []
resize_width = 640  # Resize width
resize_height = 360  # Resize height
frame_skip_interval = 5  # Number of frames to skip (set this to desired interval, e.g., 5 means every 5th frame)

frame_count = 0  # Counter to track frame number
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total number of frames in the video

# --- STEP 2: Extract and Resize Frames Using GPU ---
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Skip frames based on the interval
    if frame_count % frame_skip_interval == 0:
        # Upload frame to GPU
        gpu_frame = cv2.cuda_GpuMat()
        gpu_frame.upload(frame)
        
        # Resize the frame on the GPU
        gpu_resized = cv2.cuda.resize(gpu_frame, (resize_width, resize_height))
        
        # Download the resized frame back to CPU
        resized_frame = gpu_resized.download()
        frame_list.append(resized_frame)

        # --- Live Preview --- 
        cv2.imshow("Live Preview - Resized Frame", resized_frame)
        
        # --- Progress Status --- 
        progress = (frame_count / total_frames) * 100
        print(f"Processing frame {frame_count}/{total_frames} - {progress:.2f}% completed", end='\r')

    frame_count += 1

    # Exit if the user presses the 'q' key (optional)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

# Print completion time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\n✅ Extracted and resized {len(frame_list)} frames (skipping every {frame_skip_interval}-th frame).")
print(f"Time taken: {elapsed_time:.2f} seconds")

# --- STEP 3: Feature Detection on GPU ---
orb = cv2.cuda.ORB_create()  # Create GPU ORB feature detector
keypoints_list = []
descriptors_list = []

for frame in frame_list:
    # Upload the frame to GPU for feature detection
    gpu_frame = cv2.cuda_GpuMat()
    gpu_frame.upload(frame)
    
    # Detect keypoints and compute descriptors on GPU
    keypoints, descriptors = orb.detectAndCompute(gpu_frame, None)
    
    keypoints_list.append(keypoints)
    descriptors_list.append(descriptors)

# --- STEP 4: Feature Matching ---
# Using a descriptor matcher (on GPU)
matcher = cv2.cuda.DescriptorMatcher_createBFMatcher(cv2.NORM_HAMMING)
matches_list = []

for i in range(1, len(frame_list)):
    # Match descriptors between consecutive frames
    matches = matcher.match(descriptors_list[i-1], descriptors_list[i])
    matches_list.append(matches)

# --- STEP 5: Image Stitching ---
# Now that you have matched keypoints and descriptors, you can use OpenCV's regular stitching algorithm

stitcher = cv2.Stitcher_create() if int(cv2.__version__.split('.')[0]) >= 4 else cv2.createStitcher()
status, pano = stitcher.stitch(frame_list)

if status == cv2.Stitcher_OK:
    cv2.imwrite("panorama_result.jpg", pano)
    print("✅ Panorama saved as 'panorama_result.jpg'")
    cv2.imshow("Panorama", pano)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("❌ Panorama stitching failed. Error code:", status)

cv2.destroyAllWindows()
