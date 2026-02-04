from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

LABEL_CLASSES = ["book", "bottle"]

def run_yolo(camera_url):
    cap = cv2.VideoCapture(camera_url)
    print("✅ YOLO AI module started")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.5, verbose=False)
        annotated_frame = frame.copy()

        if results and results[0].boxes is not None:
            boxes = results[0].boxes

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]

                # Draw box for ALL objects
                cv2.rectangle(
                    annotated_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Draw label ONLY for book & bottle
                if class_name in LABEL_CLASSES:
                    cv2.putText(
                        annotated_frame,
                        class_name,
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

        cv2.imshow("YOLO Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
