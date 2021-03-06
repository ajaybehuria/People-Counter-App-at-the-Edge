"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import sys
import time
import socket
import json
import cv2
import math

import logging as log
import paho.mqtt.client as mqtt

from argparse import ArgumentParser
from inference import Network

# MQTT server environment variables
HOSTNAME = socket.gethostname()
IPADDRESS = socket.gethostbyname(HOSTNAME)
MQTT_HOST = IPADDRESS
MQTT_PORT = 3001
MQTT_KEEPALIVE_INTERVAL = 60

def build_argparser():
    """
    Parse command line arguments.
    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.55,
                        help="Probability threshold for detections filtering"
                        "(0.55 by default)")
    return parser


def connect_mqtt():
    # Connect to the MQTT server
    ### TODO: Connect to the MQTT client ###
    client = mqtt.Client()
    client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    return client

def draw_outputs(frame, result, frames_undetected, true_count):
        current_count = 0  
        for obj in result[0][0]:
            
            if obj[2] > prob_threshold:
                xmin = int(obj[3] * initial_w)
                ymin = int(obj[4] * initial_h)
                xmax = int(obj[5] * initial_w)
                ymax = int(obj[6] * initial_h)
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)
                current_count +=1
                true_count+=1
            else:
                frames_undetected+=0.01
        return frame, current_count, frames_undetected, true_count

def infer_on_stream(args, client):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    model=args.model
    video_file=args.input    
    extension=args.cpu_extension
    device=args.device
    
    # Flag for the input image
    single_img_flag = False

    start_time = 0
    cur_request_id = 0
    last_count = 0
    total_count = 0
    frames_undetected = 0
    true_count = 0
    
    # Load the model through `infer_network` 
    n, c, h, w = infer_network.load_model(model, device, extension)[1]

    # Handle the input stream
    if video_file == 'CAM': # Check for live feed
        input_stream = 0

    elif video_file.endswith('.jpg') or video_file.endswith('.bmp') :    # Check for input image
        single_img_flag = True
        input_stream = args.input

    else:     # Check for video file
        input_stream = args.input
        assert os.path.isfile(video_file), "Specified input file doesn't exist"
    
    # Get and open video capture
    cap = cv2.VideoCapture(video_file)
    cap.open(video_file)
        
    total_count = 0  
    duration = 0
    
    global initial_w, initial_h, prob_threshold
    prob_threshold = args.prob_threshold
    initial_w = cap.get(3)
    initial_h = cap.get(4)
    
    ### TODO: Load the model through `infer_network` ###
    ### TODO: Handle the input stream ###
    ### TODO: Loop until stream is over ###
    # Loop until stream is over
    while cap.isOpened():
        ### TODO: Read from the video capture ###
        # Read from the video capture
        flag, frame = cap.read()
        if not flag:
            break
        key_pressed = cv2.waitKey(60)
        ### TODO: Pre-process the image as needed ###
        # Pre-process the image as needed
        # Start async inference
        image = cv2.resize(frame, (w, h))
        # Change data layout from HWC to CHW
        image = image.transpose((2, 0, 1))
        image = image.reshape((n, c, h, w))
        ### TODO: Start asynchronous inference for specified request ###
        # Start asynchronous inference for specified request
        inf_start = time.time()
        infer_network.async_inference(cur_request_id, image)
        
        color = (92,23,232)
        ### TODO: Wait for the result ###
        # Wait for the result
        if infer_network.wait(cur_request_id) == 0:
            ### TODO: Get the results of the inference request ###
            det_time = time.time() - inf_start
            ### TODO: Extract any desired stats from the results ###
            ### TODO: Calculate and send relevant information on ###
            # Get the results of the inference request 
            result = infer_network.get_output(cur_request_id)
            
            # Draw Bounting Box
            frame, current_count, frames_undetected, true_count = draw_outputs(frame, result, frames_undetected, true_count)
            if true_count > 0:
                frames_undetected = 0
                true_count+=1
            if true_count > 1:
                true_count = 0
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###            
            # Printing Inference Time 
            inf_time_message = "Inference time: {:.3f}ms".format(det_time * 1000)
            cv2.putText(frame, inf_time_message, (15, 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            
            # Calculate and send relevant information 
            if  current_count > last_count : 
                start_time = time.time()
                total_count = total_count + current_count - last_count
                client.publish("person", json.dumps({"total": total_count}))            
            
            if current_count < last_count and int(time.time() - start_time) >2 : # Average Time
                duration = int(time.time() - start_time) 
                client.publish("person/duration", json.dumps({"duration": duration}))
           
                 ### Topic "person/duration": key of "duration" ###
            ### TODO: Send the frame to the FFMPEG server ###
            client.publish("person", json.dumps({"count": current_count})) # People Count
            txt = "Frames since Last Detection: %d" %frames_undetected
            cv2.putText(frame, txt, (15, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, color, 1)
            last_count = current_count

            if key_pressed == 27:
                break

        # Send the frame to the FFMPEG server
        sys.stdout.buffer.write(frame)  
        sys.stdout.flush()
        
        #Save the Image
        if single_img_flag:
            cv2.imwrite('output_image.jpg', frame)
        ### TODO: Write an output image if `single_image_mode` ###
        cv2.imwrite('output_image.jpg', frame)
    cap.release()
    cv2.destroyAllWindows()
    client.disconnect()
    infer_network.clean()

def main():
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    client = connect_mqtt()
    # Perform inference on the input stream
    infer_on_stream(args, client)


if __name__ == '__main__':
    main()
    exit(0)
