import tensorflow
from tensorflow import keras
from keras import layers as ls
import numpy as np


image_height = 256
image_width = 256
batch_size = 32
sets_path = "./learning_sets"
model_path="./IR.model"
train_new_model=True

class ImageRecognizer():
	def __init__(self):
		if train_new_model == True:
			# deklarowanie setów treningowych i testowych
			self.trainset = keras.utils.image_dataset_from_directory(sets_path, validation_split=0.2, subset="training",seed=0, image_size=(image_height, image_width),batch_size=batch_size)
			self.testset = keras.utils.image_dataset_from_directory(sets_path, validation_split=0.2,subset="validation", seed=0,image_size=(image_height, image_width),batch_size=batch_size)
			self.class_names = self.trainset.class_names
			self.trainset = self.trainset.cache().shuffle(1000).prefetch(buffer_size=tensorflow.data.AUTOTUNE)
			self.testset = self.testset.cache().prefetch(buffer_size=tensorflow.data.AUTOTUNE)
			#tworzenie modelu
			self.model = keras.models.Sequential()
			self.model.add(ls.Rescaling(1. / 255, input_shape=(image_height, image_width, 3)))
			self.model.add(ls.Conv2D(16, (3,3), activation='relu'))
			self.model.add(ls.MaxPooling2D((2,2)))
			self.model.add(ls.Conv2D(32, (3,3), activation='relu'))
			self.model.add(ls.MaxPooling2D((2,2)))
			self.model.add(ls.Conv2D(64, (3,3), activation='relu'))
			self.model.add(ls.MaxPooling2D(2,2))
			self.model.add(ls.Flatten())
			self.model.add(ls.Dense(128, activation='relu'))
			self.model.add(ls.Dense(2))
			#kompilacja modelu
			self.model.compile(optimizer='adam',loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),metrics=['accuracy'])
			#epochowanie
			self.model.fit(self.trainset,validation_data=self.testset,epochs=10)
			self.model.save(model_path)
		else:
			self.class_names = ("bombs","stones")
			self.model = tensorflow.keras.models.load_model(model_path)

	def recognize(self,image_path):
		#wybor obrazu do rekognizacji
		image = keras.utils.load_img(image_path, target_size=(image_height, image_width))
		image_array = keras.utils.img_to_array(image)
		image_array = tensorflow.expand_dims(image_array, 0)
		#predykcja
		prediction = self.model.predict(image_array)
		classification = tensorflow.nn.softmax(prediction[0])
		#wynik predykcji
		print("Image: ",image_path," is classified as: ",format(self.class_names[np.argmax(classification)])," with: ", 100 * np.max(classification), " accuracy")
		return format(self.class_names[np.argmax(classification)])