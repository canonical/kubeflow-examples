#!/usr/bin/env python

import base64
import cv2
import json
import requests

# ROS
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy

class AI_kubeflow_demo:
    def __init__(self):
        self.inference_pub = rospy.Publisher('inference', Image, queue_size=1)
        self.image_sub = rospy.Subscriber('/camera/image_raw', Image, self.cb_image, queue_size=1, buff_size=10000000)
        server = rospy.get_param("/demo/server", "localhost")
        self.url = 'http://{}:9000/api/v0.1/predictions'.format(server)
        self.bridge = CvBridge()
        
    def cb_image(self, msg):
        files = {
            "mode": "RGB",
            "size": "640x480",
            "media": base64.b64encode(msg.data)
        }
        results = requests.post(self.url, files=files)
        res = json.loads(results.text)
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        for r in res:
            if r['score'] > 0.9:
                # print(f"Detected {r['label']} with confidence {round(r['score'], 3)} at location {r['box']}")
                start_point = (int(r['box'][0]), int(r['box'][1]))
                end_point = (int(r['box'][2]), int(r['box'][3]))
                # print(start_point)
                color = (255, 0, 0)
                thickness = 2
                cv2.rectangle(cv_image, start_point, end_point, color, thickness)
                cv2.putText(cv_image, r['label'], start_point, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1, cv2.LINE_AA)
        
        enference_image = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
        self.inference_pub.publish(enference_image)


if __name__ == '__main__':
    try:
        rospy.init_node('ai_kubeflow_demo', anonymous=True)
        ai_kubeflow_demo = AI_kubeflow_demo()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
