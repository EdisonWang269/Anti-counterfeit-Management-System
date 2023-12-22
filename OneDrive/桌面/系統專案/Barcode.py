import cv2

class Barcode:

    delay = 1
    camera_id = 0

    @staticmethod
    def scan():
        cap = cv2.VideoCapture(Barcode.camera_id)
        barcode_detector = cv2.barcode_BarcodeDetector()
        barcode = ""

        while True:
            ret_cap, frame = cap.read()
            frame = cv2.flip(frame, 1)

            if ret_cap:
                cv2.imshow('window', frame)
                retval, _, _ = barcode_detector.detectAndDecode(frame)

            if len(retval.strip()) != 0:
                barcode = retval.strip()
                break

            if cv2.waitKey(Barcode.delay) == ord('q'):
                break
        
        cap.release()
        return barcode
