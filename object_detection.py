import cv2
from ultralytics import YOLO
import datetime
import collections
import os
import csv

def live_detection():
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt') 

    # COCO classes for drinks/containers: 39 (bottle), 41 (cup),73 Bags
    # If you are using a custom model, you might just want to count everything,
    # in which case you can remove the `classes=TARGET_CLASSES` argument below.
    TARGET_CLASSES = [39, 41,73] 

    # Note: Using index 1 since you changed it in your local file. 
    # Change back to 0 if 1 doesn't open the correct camera.
    print("Opening webcam...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Webcam opened! Press 'q' to quit.")

    # --- State variables for event tracking ---
    is_event_active = False
    tracked_ids_in_event = set()
    total_products_out = 0
    # We look at the last 15 frames (approx 0.5s) to detect a quick grab
    recent_counts = collections.deque(maxlen=15) 
    log_file = "product_log.csv"

    # Initialize log file with header if it doesn't exist
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Action", "Quantity_Changed", "Total_Session_Out"])
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "SESSION_START", 0, 0])

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Use object tracking to follow the product until it leaves the frame.
        # agnostic_nms=True ensures that a single physical object is only detected as one class.
        results = model.track(frame, persist=True, stream=True, classes=TARGET_CLASSES, agnostic_nms=True, verbose=False)

        current_frame_count = 0
        annotated_frame = frame
        current_frame_ids = set()
        
        for result in results:
            annotated_frame = result.plot()
            current_frame_count = len(result.boxes) # Count the number of detected boxes
            if result.boxes.id is not None:
                current_frame_ids.update(result.boxes.id.int().cpu().tolist())

        # Smooth the count to prevent flickering
        recent_counts.append(current_frame_count)
        
        # Once we have enough frames in our buffer
        if len(recent_counts) == recent_counts.maxlen:
            # Check how many frames see at least 1 product
            nonzero_count = sum(1 for c in recent_counts if c > 0)
            
            # If at least half the frames see a product, we consider an event "Active"
            if nonzero_count >= (recent_counts.maxlen * 0.5):
                is_event_active = True
                
                # Keep track of all unique products seen during this single grab
                tracked_ids_in_event.update(current_frame_ids)
                    
            else:
                # The frame is mostly empty (event finished)
                if is_event_active:
                    products_grabbed = len(tracked_ids_in_event)
                    
                    # Fallback just in case tracking failed but YOLO detected boxes
                    if products_grabbed == 0 and max(recent_counts) > 0:
                        products_grabbed = max(recent_counts)

                    if products_grabbed > 0:
                        total_products_out += products_grabbed
                        
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"[{timestamp}] ALERT: {products_grabbed} product(s) GRABBED & REMOVED! (Total Out: {total_products_out})")
                        
                        with open(log_file, "a", newline="") as f:
                            writer = csv.writer(f)
                            # We log the session's cumulative total out in the 4th column
                            writer.writerow([timestamp, "PRODUCT_OUT", products_grabbed, total_products_out])
                    
                    # Reset event state for the next customer
                    is_event_active = False
                    tracked_ids_in_event.clear()

        # --- Display Information on the Window ---
        # Show Current Status
        status_text = "Status: ACTIVE GRAB!" if is_event_active else "Status: WAITING..."
        color = (0, 0, 255) if is_event_active else (0, 255, 0)
        cv2.putText(annotated_frame, status_text, (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        
        # Show unique tracked products in current event
        current_grab_count = len(tracked_ids_in_event)
        cv2.putText(annotated_frame, f"Current Grab Count: {current_grab_count}", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    
        # Show Total Session Out
        cv2.putText(annotated_frame, f"Session Total Out: {total_products_out}", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow('Live Vending Machine Drink Detection', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    live_detection()
