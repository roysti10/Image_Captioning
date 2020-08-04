import nltk
from tqdm import tqdm
import tensorflow as tf
import os
import cv2
import matplotlib.pyplot as plt
nltk.download('punkt')
import string
from sklearn.utils import shuffle
import numpy as np
class DataManager(object):
  def __init__(self,cnn_model='inception',captions_filename='Flickr8k.token.txt',IMAGE_FOLDER='Flicker8k_Dataset',features_extraction=False):
    self.captions_filename = captions_filename
    self.image_folder = IMAGE_FOLDER
    self.image_ids= [i for i in tqdm(os.listdir(self.image_folder))]
    self.cnn = cnn_model
    self.vocab_size=3000
    self.max_length=35
    self.prepare_text()
    if features_extraction:
      if self.cnn == 'inception':
        self.img_features = 2048
        self.img_shape = (299,299)
      elif self.cnn == 'vgg16':
        self.img_features = 512
        self.img_shape=(224,224)
      self.cnn_model()
      self.prepare_images()
  def load_image(self,image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (299, 299))
    if self.cnn=='inception':
      x = tf.keras.applications.inception_v3.preprocess_input(img)
    elif self.cnn=='vgg16':
      x = tf.keras.applications.vgg16.preprocess_input(img)
    return image_path,x
  def cnn_model(self):
    if self.cnn == 'inception':
      model = tf.keras.applications.InceptionV3(weights='imagenet')
    elif self.cnn == 'vgg16':
      model = tf.keras.applications.VGG16(weights='imagenet')
    new_input = model.input
    hidden_layer = model.layers[-2].output
    self.model_new = tf.keras.models.Model(new_input, hidden_layer)
  def prepare_images(self):
    train_captions = np.array([i[0] for i in self.train_captions])
    train_captions=sorted(set(train_captions))
    image_dataset = tf.data.Dataset.from_tensor_slices(train_captions)
    image_dataset = image_dataset.map(self.load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE).batch(16)# Feel free to change batch_size according to your system configuration
    for path,img in tqdm(image_dataset):
      batch_features=tf.convert_to_tensor(self.model_new.predict(img))
      batch_features = tf.reshape(batch_features,
                              (batch_features.shape[0],batch_features.shape[1]))
      for bf, p in zip(batch_features, path):
        path_of_feature = p.numpy().decode("utf-8")
        np.save(path_of_feature, bf.numpy())
  def clean_descriptions(self,desc):
    table = str.maketrans('', '', string.punctuation)
    desc = desc.split()
    desc = [word.lower() for word in desc]
    desc = [w.translate(table) for w in desc]
    desc = [word for word in desc if len(word)>1]
    desc = [word for word in desc if word.isalpha()]
    desc_list=  ' '.join(desc)
    return desc_list
  def listing(self,text):
    all_img_path_captions=[]
    for i in text:
      caption=self.clean_descriptions(' '.join(i.split()[1:]).strip().lower())
      image_id=i.split()[0][:-2]
      if image_id[-4:]!='.jpg':
        image_id=image_id[:-2]
      if image_id in self.image_ids:
        path=self.image_folder+'/'+image_id
      all_img_path_captions.append((path,caption))
    return all_img_path_captions
  def preprocess_captions(self):
    cap=open(self.captions_filename)
    self.train_captions=self.listing(cap)
    words={}
    for batch in tqdm(self.train_captions):
      path,sentence = batch
      for w in nltk.tokenize.word_tokenize(sentence.lower()):
        words[w] = words.get(w, 0) + 1.0
    assert self.vocab_size<=len(words.keys())
    word_counts = sorted(list(words.items()),
                         key=lambda x: x[1],
                         reverse=True)
    #print(word_counts)
    self.words=['<start>']
    self.word2ix={}
    self.word2ix['<start>']=1
    for i in range(self.vocab_size):
       word , frequency = word_counts[i]
       if frequency>=5:
        self.words.append(word)
        self.word2ix[word] = i + 2
        max = i + 2
    self.words.append('<end>')
    self.word2ix['<end>'] = max+1
    self.ix2word={self.word2ix[i]:i for i in self.word2ix}
    #print(len(self.words))
    self.vocab_size= len(self.words)
  def ixing(self,caption):
    words=caption.split()
    word_idxs = []
    for w in words:
      try:
        word_idxs.append(self.word2ix[w])
      except:
        pass      
    return word_idxs
  def prepare_text(self):
    self.preprocess_captions()
    path_ixing_masks=[]
    for batch in tqdm(self.train_captions):
      path,caption=batch
      captions = '<start> '+caption.lower().strip()+' <end>'
      caption_ix= self.ixing(captions)
      caption_ixing = np.zeros(self.max_length,dtype=np.int64)
      caption_masks = np.zeros(self.max_length)
      caption_ix_len = len(caption_ix)
      caption_ixing[:caption_ix_len] = np.array(caption_ix)
      caption_masks[:caption_ix_len] = 1.0
      path_ixing_masks.append((path,caption_ixing,caption_masks))
    self.text = np.array(path_ixing_masks)
if __name__=='main':
  dataset=DataManager(features_extraction=True)