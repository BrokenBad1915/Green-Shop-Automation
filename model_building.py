# import os
# from PIL import Image
# import numpy as np
# import pandas as pd
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler, LabelEncoder

# # Step 1: Load and preprocess data
# data = []
# labels = []
# path = os.path.join(os.getcwd(), 'image_data')

# for i in os.listdir(path):
#     label = i
#     for j in os.listdir(os.path.join(path, i)):
#         img = Image.open(os.path.join(os.path.join(path, i), j))
#         arr = np.array(img).reshape(-1)
#         data.append(arr)
#         labels.append(label)

# data = np.array(data)
# x = pd.DataFrame(data)

# # Step 2: Encoding categorical variable
# label_encoder = LabelEncoder()
# labels_encoded = label_encoder.fit_transform(labels)
# x['label'] = labels_encoded

# # Step 3: Dimensionality reduction
# pca = PCA(0.99)
# trans_data = pca.fit_transform(x.drop(columns=['label']))  # Dropping 'label' column before applying PCA

# # Step 4: Scaling (recommended for PCA)
# scaler = StandardScaler()
# trans_data_scaled = scaler.fit_transform(trans_data)

# # Step 5: Convert to DataFrame with dummy variables (if necessary)
# # No need for dummy variables since 'label' is already numerical after encoding

# # Step 6: Print transformed data and shape
# # print(pd.DataFrame(trans_data_scaled))  # Print transformed data
# # print(trans_data_scaled.shape)         # Print shape of transformed data

import os
from PIL import Image
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import cv2

# Load and preprocess data
data = []
labels = []
path = os.path.join(os.getcwd(), 'image_data')

for i in os.listdir(path):
    label = i
    for j in os.listdir(os.path.join(path, i)):
        img = Image.open(os.path.join(os.path.join(path, i), j))
        img = img.resize((100, 100))  # Resize images to a fixed size
        arr = np.array(img)
        data.append(arr)
        labels.append(label)

data = np.array(data)
labels = np.array(labels)

# Convert labels to categorical format
label_dict = {'Apple': 0, 'Orange': 1, 'Banana': 2}
labels_encoded = np.array([label_dict[label] for label in labels])
labels_categorical = to_categorical(labels_encoded)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(data, labels_categorical, test_size=0.2, random_state=42)

# CNN model architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Predictions
y_pred = model.predict(X_test)

# Decode predictions and actual labels
predicted_labels = np.argmax(y_pred, axis=1)
actual_labels = np.argmax(y_test, axis=1)

# Print predicted and actual labels
for i in range(len(predicted_labels)):
    print(f"Predicted: {predicted_labels[i]}, Actual: {actual_labels[i]}")

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

