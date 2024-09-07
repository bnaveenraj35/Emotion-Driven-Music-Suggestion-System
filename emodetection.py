

def turn_on_camera_and_return_emotion():
    import cv2
    import random

    # Define emotion labels
    emotion_labels = ['anger', 'calm', 'happy', 'sad']
    # Start video capture
    cap = cv2.VideoCapture(0)

    # Keep track of start time
    start_time = cv2.getTickCount()

    while True:
        _, frame = cap.read()
        cv2.imshow('Camera', frame)

        # Check if 5 seconds have elapsed and break out of the loop
        current_time = cv2.getTickCount()
        elapsed_time = (current_time - start_time) / cv2.getTickFrequency()
        if elapsed_time >= 2:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Return a random emotion label
    return random.choice(emotion_labels)


