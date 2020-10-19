#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion 
import math
from time import *
from DDR.msg import err
pub=None
rate=0
dist=[]
theta=0
set_ang=0
ierr_ang=0
derr_ang=0
prev_err_ang=0
pub2=None
def _dist():
#TO SET INF TO 0 AND GET THE MAX DIST
   global dist
   for i in range(len(dist)):
     if math.isinf(dist[i]):
       dist[i]=0
   return max(dist)           
def laser_clbk(msg):
#CALL BACK FUNCTION OF LASER SUBSCRIBER
   global dist
   dist.append(msg.ranges[360])
def odom_clbk(msg):
#CALL BACK FUNCTION FOR ODOMETRY SUBSCRIBER
   global theta,ax1,cur_time
   orientation_q = msg.pose.pose.orientation
   orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
   (roll, pitch, theta) = euler_from_quaternion (orientation_list)
def line_control():
#A PID CONTROLLER FOR LINE CONTROL [ Kp=10 | Ki=1e-5 | Kd=1000 ]
   global theta,set_ang,ierr_ang,derr_ang,rate,prev_err_ang,pub2
   v=Twist()
   v.linear.x=0
   err_ang=set_ang-theta
   ierr_ang+=err_ang
   derr_ang=err_ang-prev_err_ang
   t=err()
   t.x=float(err_ang)
   pub2.publish(t)
   print(math.fabs(err_ang))
   if math.fabs(err_ang)>(math.pi/1800):
     v.linear.x=0
     v.angular.z=10*err_ang+0.00001*ierr_ang+1000*derr_ang  
     pub.publish(v)
     rate.sleep()
     prev_err_ang=err_ang
     return 0
   else:
     prev_err_ang=err_ang
     return 1
def main():
   global pub,rate,theta,dist,set_ang,pub2
   rospy.init_node('move_farthest',anonymous=True)
   pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
   rate=rospy.Rate(1000)
   sub1=rospy.Subscriber('/ddr/laser/scan',LaserScan,laser_clbk)
   sub2=rospy.Subscriber('/odom',Odometry,odom_clbk)
   pub2=rospy.Publisher('/ddr/errors',err,queue_size=10)
   v=Twist()
   v.angular.z=1
   old_time=time()
   while time()-old_time<8:
     pub.publish(v)
     rate.sleep()
   _max=_dist()
   while round(dist[-1],0)!=round(_max,0): # rounding off to compensate LOSS in laser scan
     pub.publish(v)
     rate.sleep()
   v.angular.z=0
   pub.publish(v)
   set_ang=theta
   print(set_ang)
   while dist[-1]>0.4:
     state=line_control()
     if state==1:
       v.linear.x=0.3
       pub.publish(v)
       rate.sleep()
     else:
       v.linear.x=0
   v.angular.z=0         
   v.linear.x=0
   pub.publish(v)
   sleep(1)
if __name__=='__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass
