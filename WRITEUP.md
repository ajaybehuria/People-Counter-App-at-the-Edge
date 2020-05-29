# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Explaining Custom Layers

The process behind converting custom layers mainly involves using an extension template to execute custom layers within a model. First, you have to generate the Extension Template Files. This can be done with the model extension generator. Then, you must create an IR File which contains the customer layer which can be done with the model optimizer. After that, edit the CPU extension and you can run your model. This worked for me.

Custom layers in a model can be vital, as they can help models operate at a higher level of abstraction. They pose various benefits in contrast to not having them. It is worth the additional effort as they can be perfect built to fit any situation.

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations were through trial and error. First I got each model using wget from the Tensorflow model zoo. Then using tar I extracted the contents. From here, you can do initial tests and take measurements. Then use the model optimizer for conversion. After that you can take more measurements for post-conversion. 

The difference between model accuracy pre- and post-conversion was that the post-conversion model had trouble tracking moving people rather than idle people. This wasn't too big of a deal for the pre-conversion model.

The size of the model pre- and post-conversion wasn't too different. The size of the .pb file was 19MB while the size of the .bin file was 18MB. So there is a 1MB difference after conversion

The inference time of the model pre- and post-conversion also was very similar. The inference time for the converted model was around 30-31 ms. For the .pb file it was around the same speed give or take a few. 

## Assess Model Use Cases

Some of the potential use cases of the people counter app are for demand prediction, customer count averaging, demographics, and various other averages and statistics.

Each of these use cases would be useful because they can give an idea of what to expect to foster readiness and preperation. For example, if multiple customers have their eye on the same product, you can sell more of that product. This is only one benefit of many.

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows, they can severely affect statistics. If the model provides incorrect data, it could throw all the benefits or all the plans you had for the model out the window. 
## Model Research

Using the model optimizer I successfully converted this Tensorflow model

In investigating potential people counter models, I tried out different models to which I found the most effective one



- Model: SSD Lite MobileNet V2 Coco Tensorflow Model  http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz 
  - I obtained the model by using the wget function with the link above to obtain the tar folder
  
  - Then to extract contents I used tar-xvf
  
  - I converted the model to an Intermediate Representation with the following arguments python /opt/intel/openvino/deployment_tools/model_optimizer/mo.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --reverse_input_channels --tensorflow_use_custom_operations_config
  
  - The model was insufficient for the app because of the unsupported layers, it also sometimes double-counted due to the limited accuracy
  
  - I tried to improve the model for the app by decreasing the confidence threshold which definietly improved the result and made the statistics more accurate
  
