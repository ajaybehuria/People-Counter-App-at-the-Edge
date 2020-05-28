# Project Write-Up

You can use this document as a template for providing your project write-up. However, if you
have a different format you prefer, feel free to use it as long as you answer all required
questions.

## Explaining Custom Layers

The process behind converting custom layers involves many different options for the user. The easiest way to convert custom layers in the model optimizer is to add them as extensions. Depeding on model type, theres many other options as well for custom layer support.

Some of the potential reasons for handling custom layers are the various uses of them. Custom layers can be an essential part of your model because of how much they may add to it. Not taking care of custom layers makes your model somewhat incomplete as it has unsupported layers.

## Comparing Model Performance

My method(s) to compare models before and after conversion to Intermediate Representations
were trial and error. I used the TensorFlow Model Zoo, so I had many available models with statistics available. 

The difference between model accuracy pre- and post-conversion was more noticable than I thought. The model optimizer definitely made a difference. I have used these models in the past and can see improvement with the model optimizer. Clearing up unnecessary aspects was more effective than I thought.

The size of the model pre- and post-conversion was also significant. The pre-conversion model was never too big of a problem, but the optimizer did have an impact and the post-conversion model is definitely preferable.

The inference time of the model pre- and post-conversion was crucial. Time difference between the pre- and post- conversion was the best part of the Model Optimizer. It increases speed by a hefty margin with my model. I believe this to be the most important feature of the model optimizer.

## Assess Model Use Cases

Some of the potential use cases of the people counter app are for demand prediction, customer count averaging, demographics, and various other averages and statistics.

Each of these use cases would be useful because they can give an idea of what to expect to foster readiness and preperation. For example, if multiple customers have their eye on the same product, you can sell more of that product. This is only one benefit of many.

## Assess Effects on End User Needs

Lighting, model accuracy, and camera focal length/image size have different effects on a
deployed edge model. The potential effects of each of these are as follows, they can severely affect statistics. If the model provides incorrect data, it could throw all the benefits or all the plans you had for the model out the window. 
## Model Research

[This heading is only required if a suitable model was not found after trying out at least three
different models. However, you may also use this heading to detail how you converted 
a successful model.]

In investigating potential people counter models, I tried each of the following three models:

- Model 1: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
  
- Model 2: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...

- Model 3: [Name]
  - [Model Source]
  - I converted the model to an Intermediate Representation with the following arguments...
  - The model was insufficient for the app because...
  - I tried to improve the model for the app by...
