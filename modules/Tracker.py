import cv2


class Tracker:
    def __init__(self, tracker_type='BOOSTING'):
        self.tracker_type = tracker_type
        self.tracker = None

    def create_tracker(self, frame, bbox):
        if self.tracker_type == 'BOOSTING':
            self.tracker = cv2.TrackerBoosting_create()
        elif self.tracker_type == 'MIL':
            self.tracker = cv2.TrackerMIL_create()
        elif self.tracker_type == 'KCF':
            self.tracker = cv2.TrackerKCF_create()
        elif self.tracker_type == 'TLD':
            self.tracker = cv2.TrackerTLD_create()
        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.TrackerMedianFlow_create()
        elif self.tracker_type == 'GOTURN':
            self.tracker = cv2.TrackerGOTURN_create()
        elif self.tracker_type == 'CSRT':
            self.tracker = cv2.TrackerCSRT_create()
        elif self.tracker_type == 'MOSSE':
            self.tracker = cv2.TrackerMOSSE_create()
        else:
            raise ValueError('Invalid tracker type specified.')

        self.tracker.init(frame, bbox)

    def update(self, frame):
        success, bbox = self.tracker.update(frame)
        return success, bbox










