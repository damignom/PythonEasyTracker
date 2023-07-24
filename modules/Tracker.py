import cv2


class Tracker:
    def __init__(self, tracker_type='BOOSTING'):
        self.bbox = None
        self.success = None
        self.tracker_type = tracker_type
        self.tracker = None
        self.fps = None

    def create_tracker(self, frame, bbox):
        if self.tracker_type == 'BOOSTING':
            self.tracker = cv2.legacy.TrackerBoosting().create()
        elif self.tracker_type == 'MIL':
            self.tracker = cv2.legacy.TrackerMIL.create()
        elif self.tracker_type == 'KCF':
            self.tracker = cv2.legacy.TrackerKCF().create()
        elif self.tracker_type == 'TLD':
            self.tracker = cv2.legacy.TrackerTLD.create()
        elif self.tracker_type == 'MEDIANFLOW':
            self.tracker = cv2.legacy.TrackerMedianFlow().create()
        elif self.tracker_type == 'GOTURN':
            self.tracker = cv2.TrackerGOTURN().create()
        elif self.tracker_type == 'CSRT':
            self.tracker = cv2.TrackerCSRT().create()
        elif self.tracker_type == 'MOSSE':
            self.tracker = cv2.legacy.TrackerMOSSE().create()
        else:
            raise ValueError('Invalid tracker type specified.')

        self.tracker.init(frame, bbox)

    def update(self, frame):
        self.success, self.bbox = self.tracker.update(frame)
        return self.success, self.bbox

    def getTrackingState(self):
        if self.success:
            return "Tracking"
        else:
            return "Failure"










