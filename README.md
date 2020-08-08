# Image Captioning

## Dataset Preparation
* Clone this repsoitory using 
  ```bash 
  git clone https://github.com/lucasace/Image_Captioning.git 
  ```
* Download the Flickr8k Image and Text dataset from ![here](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip) and ![here](https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip) respectively
* Unzip both the dataset and text files and place it inside the repository folder

## I want to train the model
To train the model simply run
```bash
python3 main.py --type train --checkpoint_dir <checkpointdir> --cnnmodel <cnnmodel> --image_folder <imagefolder location> --caption_file <location to token,txt> --feature_extraction <True or False> -- batch_size <batchsize>
```
* The checkpoint dir is the place where your model checkpoints are going to be saved.
* cnnmodel is either inception or vgg16,default is inception
* imagefolder is location of the folder with all the images
* caption_file is Location to 'Flickr8k.token.txt'
* feature_extraction - True or False,default is True
  * True if you havent extracted the image features
  * False if you have already extracted the image features
  This is saves time and memory when training again 
 * batch_size batch_size of training and validation default is 128
 
 ## Testing the model
 ```bash
python3 main.py --type test --checkpoint_dir <checkpointdir> --cnnmodel <cnnmodel> --image_folder <imagefolder location> --caption_file <location to token,txt> --feature_extraction <True or False>
```
* Download the checkpoints from ![here](https://drive.google.com/drive/u/1/folders/1-VJXewV_Da9TNLrNpwORY5EY0_slxT1g) or you can use your own checkpoints
* All arguments are same as in training model
 
 ## I just want to caption
 
 ```bash
 python3 main.py --type caption --checkpoint_dir <checkpointdir> --cnnmodel <cnnmodel> --caption_file <location to token,txt>
 ```
 * Download the checkpoints from ![here](https://drive.google.com/drive/u/1/folders/1-VJXewV_Da9TNLrNpwORY5EY0_slxT1g)
    * Note these are inception checkpoints and not for vgg16. Vgg16 weights will be available shortly
 * captionfile is required to make the vocabulary
 
 ## Custom dataset
  if you want to train it on a custom dataset kindly make changes in the dataset.py folder to make it suitable for your dataset
  
 ## Results
 |Model Type|CNN_Model|Bleu_1|Bleu_2|Bleu_3|Bleu_4|Metoer|
 | --- | --- | --- | --- | --- | --- | --- |
 |Encoder-Decoder|Inception_V3|60.12|51.1|48.13|39.5|25.8|
 | |VGG16| | | | | |
 
 Here are some of the results:
 
 ## References
 * O. Vinyals, A. Toshev, S. Bengio and D. Erhan, "Show and tell: A neural image caption generator," 2015 IEEE Conference on Computer Vision and Pattern Recognition (CVPR), Boston, MA, 2015, pp. 3156-3164, doi: 10.1109/CVPR.2015.7298935.
 * Tensorflow documentation on Image Captioning
 * ![Machine Learning Mastery](https://machinelearningmastery.com/develop-a-deep-learning-caption-generation-model-in-python/) for dataset
 * ![RNN lecture by Standford University](https://www.youtube.com/watch?v=6niqTuYFZLQ&t=1731s)
