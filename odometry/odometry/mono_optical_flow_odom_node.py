import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from tf2_msgs.msg import TFMessage
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge

class MonoOpticalFlowOdomNode(Node):
    def __init__(self):
        self.image_count = 0
        self.old_image = None
        self.new_image = None
        self.bridge = CvBridge()
        self.cam_body_tf = None

        self.declare_parameters(namespace = "", parameters=[
            ("body_id", "base_link"),
            ("cam_id", "camera")
        ])
        
        # Subscriptions
        self.camera_sub = self.create_subscription(
            Image,
            "/camera", # this will get remapped in launch file
            self.camera_sub_callback,
            10
        )

        self.tf_sub = self.create_subscription(
            TFMessage,
            "/tf_static",
            self.tf_sub_callback,
            10
        )

        # Publishers
        self.odom_pub = self.create_publisher(
            Odometry,
            "/odometry", # remap to whatever later
            10
        )

    def camera_sub_callback(self, image: Image):
        cv_image = self.bridge.imgmsg_to_cv2(image, desired_encoding="mono8")
        if self.image_count == 0:
            self.old_image = cv_image
        else:
            if self.image_count == 1:
                self.new_image = cv_image
            else:
                self.old_image = self.new_image
                self.new_image = cv_image
            
            # CALL ACTUAL ODOM FUNCTIONALITY HERE
        self.image_count += 1

    def tf_sub_callback(self, tf: TFMessage):
        for tf_stamped in tf.transforms:
            header = tf_stamped.header
            frame_id = header.frame_id
            child_frame_id = tf_stamped.child_frame_id
            if (frame_id == self.get_parameter("body_id") and child_frame_id == self.get_parameter("cam_id")):
                self.cam_body_tf = tf_stamped.transform
                break
        if (self.cam_body_tf is not None):
            self.destroy_subscription(self.tf_sub)

def main(args = None):
    rclpy.init(args=args)
    node = MonoOpticalFlowOdomNode
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()