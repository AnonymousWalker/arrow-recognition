import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class_labels = ['up', 'down', 'left', 'right', 'up-left', 'up-right', 'down-left', 'down-right']
# class_labels = ['up', 'down', 'left', 'right']

# Define the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_labels), activation='softmax')  # number of classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Load and preprocess your dataset using ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1.0/255, validation_split=0.2)
train_generator = train_datagen.flow_from_directory(
    'training-data/2.0',
    target_size=(28, 28),
    color_mode='grayscale',
    batch_size=32,
    class_mode='categorical',
    subset='training',
    classes=class_labels
)
validation_generator = train_datagen.flow_from_directory(
    'test-data/2.0',
    target_size=(28, 28),
    color_mode='grayscale',
    batch_size=32,
    class_mode='categorical',
    subset='validation',
    classes=class_labels
)

# Train the model
model.fit(train_generator, validation_data=validation_generator, epochs=10)

# Save the trained model
model.save('trained-model/v2.0-gray.h5')
