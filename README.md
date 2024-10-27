# Proyecto1-SD

## Instrucciones para ejecutar el código
1. **Configurar MongoDB**: Modificar la variable `MONGO_URI` en el archivo main.py para realizar la conexión a los datos de MongoDB
2. **Configurar AWS**: 
3. **Creación del bucket (opcional)**: En caso de no tener un bucket de AWS para el almacenamiento, es necesario escrbir un nombre en la variable `bucket`, descomentar la linea `crear_bucket` y ejecutar el código
4. **Ejecutar el servidor de FastAPI**: Para poder realizar las pruebas de el código es necesario ejecutar en terminal el comando `fastapi dev "nombre del archivo".py`

### Información almacenada en el bucket de AWS
![image](https://github.com/user-attachments/assets/e7769110-efb7-4c4f-a716-8e09b04fb870)

## Pruebas de la ejecución del código
### Autor
#### Información almacenda en MongoDB
![image](https://github.com/user-attachments/assets/3e3e76e4-033b-4afc-af16-85fa6882c9d8)

#### Crear
![image](https://github.com/user-attachments/assets/f5c166dc-4502-47ba-98c4-3a3ff4632a5a)

#### Leer
![image](https://github.com/user-attachments/assets/28ccb2ba-83e5-4e34-9ce9-de34a73f51c9)

#### Modificar
![image](https://github.com/user-attachments/assets/887fc03a-6c89-4f6a-9e1c-da739097dff1)
![image](https://github.com/user-attachments/assets/2827ce57-12a8-46eb-b012-611f930d43ff)

#### Eliminar
![image](https://github.com/user-attachments/assets/7dbd2e06-7e03-4abe-b7cc-45e2ce071ae9)
![image](https://github.com/user-attachments/assets/5d678d14-1e32-4345-ba92-77f90ce30176)

### Bibliotecario
#### Información almacenda en MongoDB
![image](https://github.com/user-attachments/assets/2321f28a-fed3-41d5-bd55-2fe22c0ff9ba)

#### Crear
![image](https://github.com/user-attachments/assets/4f84d92e-a197-47c6-9e08-c0be609860ae)
#### Leer
![image](https://github.com/user-attachments/assets/149b4922-496b-4e8e-a812-5764ce04e846)

#### Modificar
![image](https://github.com/user-attachments/assets/8a1c984e-9468-435b-9202-6918493cc657)
![image](https://github.com/user-attachments/assets/fd4abd97-602e-4271-8bd4-4ce3fdc43be2)

#### Eliminar
![image](https://github.com/user-attachments/assets/90e44810-4ce1-4162-bbd8-d4df909518c5)
![image](https://github.com/user-attachments/assets/9fed0560-3071-4403-9a7e-316a7ba8190d)

### Lector
#### Información almacenda en MongoDB
![image](https://github.com/user-attachments/assets/6946fff8-8c01-4484-a4e3-4ec562b2029c)

#### Crear
![image](https://github.com/user-attachments/assets/8c30e8d9-228e-41d4-94c1-9dc3844e086c)

#### Leer
![image](https://github.com/user-attachments/assets/c39106b9-8b7f-477c-b447-64ba6928fea6)

#### Modificar
![image](https://github.com/user-attachments/assets/1479cbda-311d-4b91-a2f1-7b19a01fe897)
![image](https://github.com/user-attachments/assets/eae2f09d-8704-458b-9d93-94d21a21ac51)

#### Eliminar
![image](https://github.com/user-attachments/assets/cf33f99c-1564-4290-baaa-e121ae2aa932)
![image](https://github.com/user-attachments/assets/d8696dc1-c08f-47ae-8115-3e29b9b132e3)

### Libro
#### Información almacenda en MongoDB
![image](https://github.com/user-attachments/assets/e82bfc26-ae8f-400e-b39c-f70dfe326a87)

#### Información almacenda en AWS
![image](https://github.com/user-attachments/assets/c0589d80-204f-481a-b6f8-a4fe25db3284)


#### Crear
![image](https://github.com/user-attachments/assets/5c3f9740-554e-4a64-8267-b571b8901a1b)
![image](https://github.com/user-attachments/assets/9ebbdecc-7166-4294-adf2-8310373c6fa6)

#### Leer
![image](https://github.com/user-attachments/assets/dc79a9cc-49cb-4b2e-b745-37e3bdc9efe8)

#### Modificar
![image](https://github.com/user-attachments/assets/ee05641f-46d7-4611-a96d-4948610a708d)
![image](https://github.com/user-attachments/assets/b15c1799-b2f6-4715-9963-146c314e7fc8)

#### Eliminar
![image](https://github.com/user-attachments/assets/14c18a66-650f-4419-a963-2cf0a24473f9)
![image](https://github.com/user-attachments/assets/7e1e9159-95cc-4c5b-acc8-6be15a28e115)
![image](https://github.com/user-attachments/assets/bf1e8d2e-0523-48ea-ae8d-3d0b293d7e3a)

### Prestamo
#### Información almacenda en MongoDB
![image](https://github.com/user-attachments/assets/9137734b-135d-457d-be56-40cddcdc5a87)

#### Información almacenda en AWS
![image](https://github.com/user-attachments/assets/4d5cc71a-3109-4de6-a338-0bb3b6f8f6da)

#### Crear
![image](https://github.com/user-attachments/assets/9270df27-e29b-46e7-a232-e8c4df37aefb)
![image](https://github.com/user-attachments/assets/9792b985-b702-4c4a-b0a2-5e75f5c153e0)
##### Libro en prestamo:
![image](https://github.com/user-attachments/assets/6bc92da5-ba85-4c56-9a66-256af05effd9)

#### Leer
![image](https://github.com/user-attachments/assets/27a95421-308e-442c-8ed0-6bfe19f39615)

#### Devolver
![image](https://github.com/user-attachments/assets/3670f196-e8d0-4a33-9ef7-e12f8ec2f537)
##### Libro devuelto y credencial eliminada
![image](https://github.com/user-attachments/assets/00e28c99-c1b5-44ec-b1b4-83c46810c107)
![image](https://github.com/user-attachments/assets/4638218c-7b4a-4021-a039-9dc0cb01b38b)
