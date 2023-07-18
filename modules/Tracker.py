import cv2


def create_tracker(tracker_type):
    if tracker_type == 'KCF':
        return cv2.TrackerKCF_create()
    elif tracker_type == 'CSRT':
        return cv2.TrackerCSRT_create()
    elif tracker_type == 'MIL':
        return cv2.TrackerMIL_create()
    elif tracker_type == 'BOOSTING':
        return cv2.TrackerBoosting_create()
    elif tracker_type == 'MEDIANFLOW':
        return cv2.TrackerMedianFlow_create()
    elif tracker_type == 'MOSSE':
        return cv2.TrackerMOSSE_create()

