'''
----------------- Sistemas distribuidos ---------------
Flores Nava Aurelio
García Reyna Diego Juan Manuel Salvador
Lugo Zabala Maximiliano
Monciváis Aguilar Cesar
Montejano Quirino Isay
Pérez Cornejo Héctor Alejandro
Rodríguez Burnes Daniel
Villegas Castro Froylan
---------------------------------
'''

# Crear y manejar excepciones
from fastapi import FastAPI, HTTPException, UploadFile, File, Body
from typing import Optional
# Para crear la estructura de los datos
from pydantic import BaseModel
# Conexión a MongoDB 
from motor import motor_asyncio
# Manejo de fechas
from datetime import date, datetime, timedelta
from bson import ObjectId
# Integración con AWS
import boto3

# Configuración de la conexión con MongoDB
# Ubicación de la conexión de MongoDB
MONGO_URI = 'mongodb://localhost:27017'
# Ejecutar el cliente de base de datos
client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client['biblioteca']

autor_collection = db['autor']
bibliotecario_collection = db['bibliotecario']
lector_collection = db['lector']
libro_collection = db['libro']
prestamo_collection = db['prestamo']

# Configuración de AWS
# Excepción para cuando no tenemos credenciales de AWS
from botocore.exceptions import NoCredentialsError

# Definir el servicio y la región de AWS
s3 = boto3.client("s3", region_name = "us-east-2")

# Crear otro bucket
def crear_bucket(name, region="us-east-2"):
    try:
        if region == 'us-east-1':
            s3.create_bucket(Bucket=name)
        else:
            s3.create_bucket(
                Bucket=name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"El bucket {name} se ha creado")
    except NoCredentialsError:
        print("Las credenciales de AWS no se encontraron")
    except Exception as e:
        print(f"El bucket no se creó: {str(e)}")

bucket = 'sd-biblioteca'

#crear_bucket(bucket, 'us-east-2')

# Añadir objetos a un bucket de S3
def subir_objetos(file: UploadFile, bucket, object_name=None):
    if object_name is None:
        object_name = file.filename
    try:
        # Subir el archivo directamente desde el objeto UploadFile
        s3.upload_fileobj(file.file, bucket, object_name)
        # Generar y retornar la URL de S3
        return f"https://{bucket}.s3.amazonaws.com/{object_name}"
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciales de AWS no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo a S3: {str(e)}")

    
# Eliminar objeto de un bucket S3
def eliminar_objeto(bucket, object_name):
    try:
        s3.delete_object(Bucket=bucket, Key=object_name)
        return f'El objeto {object_name} fue eliminado de {bucket}'
    except s3.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Objeto no encontrado en S3")
    except NoCredentialsError:
        raise HTTPException(status_code=403, detail="Credenciales de AWS no encontradas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar objeto: {str(e)}")



# Objeto para interactuar con la API
app = FastAPI()

# Modelos de datos utilizando Pydantic para validar la estructura de entrada
class Autores(BaseModel):
    nombre: str
    apellido: str
    biografia: str

class Bibliotecarios(BaseModel):
    nombre: str
    apellido: str
    correo: str

class Libros(BaseModel):
    titulo: str
    autor_id: str
    descripcion: str
    imagen_portada: Optional[str] = None
    inventario: bool

class Lectores(BaseModel):
    nombre: str
    apellido: str
    correo: str

class Prestamos(BaseModel):
    lector_id: str
    libro_id: str
    bibliotecario_id: str
    fecha_prestamo: Optional[datetime] = None
    fecha_devolucion: Optional[datetime] = None
    foto_credencial: Optional[str] = None


# -------------------------------- AUTORES --------------------------------

# Obtener todos los autores
@app.get('/autor/')
async def get_autor():
    autores = await autor_collection.find().to_list(None)
    for autor in autores:
        autor['_id'] = str(autor['_id'])
    return autores

# Obtener autor por ID
@app.get('/autor/{atr_id}')
async def get_autor_id(atr_id):
    autores = await autor_collection.find().to_list(None)
    for aut in autores:
        if atr_id == str(aut['_id']):  
            aut['_id'] = str(aut['_id']) 
            return aut

# Crear un autor
@app.post('/autor/')
async def crear_autor(autor: Autores):
    await autor_collection.insert_one(autor.dict())
    return{
        'message': "El autor se añadió exitosamente"
    }

# Actualizar autor por ID
@app.put('/autor/{atr_id}')
async def actualizar_autor(atr_id, atr: Autores):
    autores = await autor_collection.find().to_list(None)
    for _atr in autores:
        if str(_atr['_id']) == atr_id:
            await autor_collection.update_one(_atr, {'$set': atr.dict()})
            return{
                'message': f'El autor con ID {atr_id} se actualizó exitosamente'
            }

# Eliminar autor por ID
@app.delete('/autor/{atr_id}')
async def borrar_autor(atr_id: str):
    result = await autor_collection.delete_one({"_id": ObjectId(atr_id)})
    if result.deleted_count:
        return {'message': 'El autor ha sido eliminado'}
    raise HTTPException(status_code=404, detail="Autor no encontrado")

# -------------------------------- BIBLIOTECARIOS --------------------------------

# Obtener todos los bibliotecarios
@app.get('/bibliotecario/')
async def get_bibliotecario():
    bibliotecarios = await bibliotecario_collection.find().to_list(None)
    for bibliotecario in bibliotecarios:
        bibliotecario['_id'] = str(bibliotecario['_id'])
    return bibliotecarios

# Obtener bibliotecario por ID
@app.get('/bibliotecario/{bib_id}')
async def get_bibliotecario_id(bib_id):
    bibliotecarios = await bibliotecario_collection.find().to_list(None)
    for bib in bibliotecarios:
        if bib_id == str(bib['_id']):  
            bib['_id'] = str(bib['_id']) 
            return bib

# Crear un bibliotecario
@app.post('/bibliotecario/')
async def crear_bibliotecario(bibliotecario: Bibliotecarios):
    await bibliotecario_collection.insert_one(bibliotecario.dict())
    return{
        'message': "El bibliotecario se añadió exitosamente"
    }

# Actualizar bibliotecario por ID
@app.put('/bibliotecario/{bib_id}')
async def actualizar_bibliotecario(bib_id, bib: Bibliotecarios):
    bibliotecarios = await bibliotecario_collection.find().to_list(None)
    for _bib in bibliotecarios:
        if str(_bib['_id']) == bib_id:
            await bibliotecario_collection.update_one(_bib, {'$set': bib.dict()})
            return{
                'message': f'El bibliotecario con ID {bib_id} se actualizó exitosamente'
            }

# Eliminar bibliotecario por ID
@app.delete('/bibliotecario/{bib_id}')
async def borrar_bibliotecario(bib_id: str):
    result = await bibliotecario_collection.delete_one({"_id": ObjectId(bib_id)})
    if result.deleted_count:
        return {'message': 'El bibliotecario ha sido eliminado'}
    raise HTTPException(status_code=404, detail="Bibliotecario no encontrado")

# -------------------------------- LIBROS --------------------------------

# Obtener todos los libros
@app.get('/libro/')
async def get_libros():
    libros = await libro_collection.find().to_list(None)
    for libro in libros:
        libro['_id'] = str(libro['_id'])
    return libros

# Obtener libro por ID
@app.get('/libro/{lib_id}')
async def get_libro_id(lib_id):
    libros = await libro_collection.find().to_list(None)
    for lib in libros:
        if lib_id == str(lib['_id']):
            lib['_id'] = str(lib['_id'])
            return lib

# Añadir un libro
@app.post('/libro/')
async def añadir_libro(libro: Libros, file: UploadFile = File(None)):
    # Validar autor_id como ObjectId y verificar si el autor existe en la base de datos
    try:
        autor_id = ObjectId(libro.autor_id)
    except:
        raise HTTPException(status_code=400, detail="ID del autor debe ser un ID válido")
    
    autor = await autor_collection.find_one({"_id": autor_id})
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    # Si se proporciona una imagen, subirla a S3
    if file:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
        try:
            object_name = f"Libros/{file.filename}"
            url = subir_objetos(file, bucket, object_name)
            libro.imagen_portada = url  
        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="No se encontraron credenciales de AWS.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Insertar el libro en la base de datos
    libro_data = libro.dict()
    libro_data["autor_id"] = autor_id
    await libro_collection.insert_one(libro_data)
    return libro
            

@app.put('/libro/{lib_id}')
async def actualizar_libro(lib_id: str, lib: Libros, file: UploadFile = File(None)):
    # Validar y convertir lib_id a ObjectId
    try:
        libro_id = ObjectId(lib_id)
    except:
        raise HTTPException(status_code=400, detail="ID del libro debe ser un ObjectId válido")

    # Verificar si el libro existe
    libro = await libro_collection.find_one({"_id": libro_id})
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Validar y convertir autor_id a ObjectId, y verificar si el autor existe
    try:
        autor_id = ObjectId(lib.autor_id)
    except:
        raise HTTPException(status_code=400, detail="ID del autor debe ser un ObjectId válido")

    autor = await autor_collection.find_one({"_id": autor_id})
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    # Si se proporciona un archivo de imagen, actualizar la imagen de portada en S3
    if file:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen.")
        object_name = f"Libros/{file.filename}"
        url = subir_objetos(file, bucket, object_name)
        lib.imagen_portada = url

    # Actualizar el libro en la base de datos
    libro_data = lib.dict()
    libro_data["autor_id"] = autor_id  # Asignar el ObjectId al campo autor_id
    await libro_collection.update_one({"_id": libro_id}, {'$set': libro_data})
    
    return {'message': f'El libro con ID {lib_id} se actualizó exitosamente'}

# Eliminar libro por ID
@app.delete('/libro/{lib_id}')
async def borrar_libro(lib_id: str):
    libro = await libro_collection.find_one({"_id": ObjectId(lib_id)})

    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Si el libro tiene una imagen en S3, elimínala
    if libro.get('imagen_portada'):
        # Extrae el nombre del archivo de la URL de S3
        object_name = libro['imagen_portada'].split('/')[-1]
        eliminar_objeto(bucket, f"Libros/{object_name}")

    # Elimina el libro de MongoDB
    result = await libro_collection.delete_one({"_id": ObjectId(lib_id)})
    if result.deleted_count:
        return {'message': 'El libro y su portada han sido eliminados'}
    else:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

# -------------------------------- LECTORES --------------------------------

# Obtener todos los lectores
@app.get('/lector/')
async def get_lector():
    lectores = await lector_collection.find().to_list(None)
    for lector in lectores:
        lector['_id'] = str(lector['_id'])
    return lectores

# Obtener lector por ID
@app.get('/lector/{lec_id}')
async def get_lector_id(lec_id):
    lectores = await lector_collection.find().to_list(None)
    for lec in lectores:
        if lec_id == str(lec['_id']):  
            lec['_id'] = str(lec['_id']) 
            return lec

# Crear un lector
@app.post('/lector/')
async def crear_lector(lec: Lectores):
    await lector_collection.insert_one(lec.dict())
    return{
        'message': "El lector se añadió exitosamente"
    }

# Actualizar lector por ID
@app.put('/lector/{lec_id}')
async def actualizar_lector(lec_id, lec: Lectores):
    lectores = await lector_collection.find().to_list(None)
    for _lec in lectores:
        if str(_lec['_id']) == lec_id:
            await lector_collection.update_one(_lec, {'$set': lec.dict()})
            return{
                'message': f'El lector con ID {lec_id} se actualizó exitosamente'
            }

# Eliminar lector por ID
@app.delete('/lector/{lec_id}')
async def borrar_lector(lec_id: str):
    result = await lector_collection.delete_one({"_id": ObjectId(lec_id)})
    if result.deleted_count:
        return {'message': 'El lector ha sido eliminado'}
    raise HTTPException(status_code=404, detail="Lector no encontrado")

# -------------------------------- PRESTAMOS --------------------------------

# Obtener todos los prestamos
@app.get('/prestamo/')
async def get_prestamo():
    prestamos = await prestamo_collection.find().to_list(None)
    for prestamo in prestamos:
        prestamo['_id'] = str(prestamo['_id'])
    return prestamos

# Obtener prestamo por ID
@app.get('/prestamo/{pre_id}')
async def get_prestamo_id(pre_id):
    prestamos = await prestamo_collection.find().to_list(None)
    for pre in prestamos:
        if pre_id == str(pre['_id']):  
            pre['_id'] = str(pre['_id']) 
            return pre

@app.post('/prestamo/')
async def crear_prestamo(pre: Prestamos, file: UploadFile = File(...)):
    # Convertir los IDs de lector, libro y bibliotecario a ObjectId
    try:
        lector_id = ObjectId(pre.lector_id)
        libro_id = ObjectId(pre.libro_id)
        bibliotecario_id = ObjectId(pre.bibliotecario_id)
    except:
        raise HTTPException(status_code=400, detail="IDs deben ser válidos ObjectId")

    # Verificar si el libro existe y está en inventario
    libro = await libro_collection.find_one({"_id": libro_id})
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if not libro['inventario']:
        raise HTTPException(status_code=400, detail="Libro no disponible en inventario")

    # Actualizar inventario del libro
    await libro_collection.update_one({"_id": libro_id}, {"$set": {"inventario": False}})

    # Establecer las fechas de préstamo y devolución
    pre.fecha_prestamo = datetime.utcnow()
    pre.fecha_devolucion = pre.fecha_prestamo + timedelta(days=3)

    # Subir foto de credencial a S3
    imagen_url = subir_objetos(file, bucket, "Credenciales")
    pre.foto_credencial = imagen_url

    # Guardar el préstamo en la base de datos
    prestamo_data = pre.dict()
    prestamo_data.update({
        "lector_id": lector_id,
        "libro_id": libro_id,
        "bibliotecario_id": bibliotecario_id
    })
    await prestamo_collection.insert_one(prestamo_data)
    return {"message": "El préstamo se realizó exitosamente"}

@app.put('/prestamo/{pre_id}/devolver')
async def devolver_prestamo(pre_id: str):
    # Verificar si el préstamo existe
    try:
        prestamo_id = ObjectId(pre_id)
    except:
        raise HTTPException(status_code=400, detail="ID de préstamo debe ser un ObjectId válido")

    prestamo = await prestamo_collection.find_one({"_id": prestamo_id})
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    # Actualizar inventario del libro
    await libro_collection.update_one({"_id": prestamo['libro_id']}, {"$set": {"inventario": True}})

    # Eliminar el registro del préstamo en la base de datos
    await prestamo_collection.delete_one({"_id": prestamo_id})

    # Eliminar la foto de credencial en S3, si existe
    if prestamo.get('foto_credencial'):
        object_name = prestamo['foto_credencial'].split('/')[-1]
        eliminar_objeto(bucket, f"Credenciales/{object_name}")

    return {"message": "El préstamo ha sido devuelto y el libro está de nuevo en inventario"}
