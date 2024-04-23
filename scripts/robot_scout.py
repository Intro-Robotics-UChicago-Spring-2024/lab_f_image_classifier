#!/usr/bin/env python3

import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from image_classifier import Net
import torchvision.transforms as transforms
import torch
import PIL

class Scout:

        def __init__(self):

                # set up ROS / cv bridge
                self.bridge = cv_bridge.CvBridge()

                # subscribe to the robot's RGB camera data stream
                self.image_sub = rospy.Subscriber('camera/rgb/image_raw',
                        Image, self.image_callback)

                self.cmd_vel_pub = rospy.Publisher('cmd_vel',
                        Twist, queue_size=1)

                self.twist = Twist()
                
                # use for image classifier
                self.classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
                self.net = Net()
                self.transform = transforms.Compose([transforms.ToTensor(), 
                                                     transforms.Resize((32, 32)), 
                                                     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
                
        def image_callback(self, msg):

                # converts the incoming ROS message to cv2 format and HSV (hue, saturation, value)
                image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                """
                TODO: Load the weights from the trained neural network. You might want to use load_state_dict(). 
                When you are loading the .pth file, make sure to include the full path.
                """
                
                #pass robot's camera footage into the neural network
                image_to_predict = self.transform(PIL.Image.fromarray(image))

                """
                TODO: pass the image_to_predict to the neural network. 
                Make sure the shape of the input to the neural network is correct. 
                """
                
                """
                TODO: Implement Robot Scout's behavior here!
                - Encountering a Cat: Scout's sensors detect an image of a cat. Instantly, Scout feels a surge of caution. 
                  To express its fear, Scout decides to move backward slowly, trying to create distance from the perceived threat.
                - Spotting a Dog: Another image appears, this time showing a dog. 
                  Scout recognizes it's a different animal but isn't sure whether to be excited or wary. 
                  To show its excitement, Scout decides to spin in a joyful circle.
                - Seeing Something Else Sometimes, Scout's camera captures images that don't resemble cats or dogs. 
                  When this happens, Scout simply pauses, observing its surroundings but choosing not to move until the next image is processed.
                """

                # show the debugging window
                cv2.imshow("window", image)
                cv2.waitKey(3)

if __name__ == '__main__':

        rospy.init_node('robot_scout')
        robot_scout = Scout()
        rospy.spin()