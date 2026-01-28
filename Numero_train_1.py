# ===============================
# 1. IMPORTAR LIBRERÍAS
# ===============================
import numpy as np
import matplotlib.pyplot as plt
from mnist import MNIST
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# ===============================
# 2. CARGAR MNIST DESDE IDX
# ===============================
ruta_mnist = "mnist_data/"   # <-- CAMBIA ESTA RUTA

mndata = MNIST(ruta_mnist)

x_train, y_train = mndata.load_training()
x_test, y_test = mndata.load_testing()

# Convertir a numpy arrays
x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)

print("Train:", x_train.shape, y_train.shape)
print("Test :", x_test.shape, y_test.shape)

# ===============================
# 3. PREPROCESAMIENTO
# ===============================

# Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# Dar forma para CNN (N, 28, 28, 1)
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)

# ===============================
# 4. CREAR MODELO CNN
# ===============================
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D((2,2)),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D((2,2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(10, activation='softmax')
])

# ===============================
# 5. COMPILAR MODELO
# ===============================
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ===============================
# 6. ENTRENAR RED
# ===============================
model.fit(
    x_train,
    y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.1
)

# ===============================
# 7. EVALUAR MODELO
# ===============================
loss, acc = model.evaluate(x_test, y_test)
print(f"\nPrecisión en test: {acc*100:.2f}%")

# ===============================
# 8. PROBAR UNA IMAGEN
# ===============================
index = 10

imagen = x_test[index]
pred = model.predict(imagen.reshape(1,28,28,1))
numero = np.argmax(pred)

print("Número real:", y_test[index])
print("Número detectado:", numero)

plt.imshow(imagen.reshape(28,28), cmap='gray')
plt.title(f"Detectado: {numero}")
plt.axis('off')
plt.show()

# ===============================
# 9. GUARDAR MODELO
# ===============================
model.save("modelo_mnist_idx.h5")
print("Modelo guardado correctamente")
