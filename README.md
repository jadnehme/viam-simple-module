# Module simple-module 

The function of this module is to provide a determination of wether a person was detected in a given camera. If a person was detected the module will return 1 other wise it will return 0 in the attribute person_detected 

## Model jadorg:simple-module:simple-detection

The model makes use of existing vision models that recognize objects. If an object is of the class person above the certainty entered in the configuration the model will return 1 otherwise it will return 0.

### Configuration

simple-module simply relies on existing modules to use camera vision and to categories the images. To use this module, one needs to: 
- follow the instructions to [add a camera from the Viam Registry]([https://docs.viam.com/operate/reference/components/camera/webcam/#:~:text=Navigate%20to%20the%20CONFIGURE%20tab,your%20camera%20and%20click%20Create.](https://docs.viam.com/operate/reference/components/camera/webcam/)
- follow the instrution to add a vision service from the Viam Registry. An example of tutorial can be found in the configure your services section of the [detection tutorial](https://docs.viam.com/tutorials/projects/send-security-photo/)
-  Install simple-module from the [registry](https://app.viam.com/registry)
- Add the vision service sersor you installed as a dependency
- Update the attribute template below to configure this model.

 
#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `camera` | string  | Required  | camera is the name of a camera component running on your machine which you want to use |
| `sensor` | string | Required  | sensor Camera is the name of the vision component running on your machine which you want to use|
| `detection_confidence` | float | Optional  | between 0 and 1, certainty accepted to determine a person is in frame |


#### Example Configuration

```json
{
  "camera": <string>,
  "detection_confidence": <float>,
  "sensor": <string>,
}
```