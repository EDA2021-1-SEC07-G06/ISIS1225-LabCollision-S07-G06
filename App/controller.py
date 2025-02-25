"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
# TODO: importaciones para medir tiempo y memoria
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del Catálogo de libros

def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# ======================================
# Funciones para la carga de datos
# ======================================


def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    # TODO: modificaciones para medir el tiempo y memoria
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadBooks(catalog)
    loadTags(catalog)
    loadBooksTags(catalog)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory


def loadBooks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'GoodReads/books.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        model.addBook(catalog, book)


def loadTags(catalog):
    """
    Carga todos los tags del archivo e indica al modelo
    que los adicione al catalogo
    """
    tagsfile = cf.data_dir + 'GoodReads/tags.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for tag in input_file:
        model.addTag(catalog, tag)


def loadBooksTags(catalog):
    """
    Carga la información que asocia tags con libros en el catalogo
    """
    booktagsfile = cf.data_dir + 'GoodReads/book_tags.csv'
    input_file = csv.DictReader(open(booktagsfile, encoding='utf-8'))
    for booktag in input_file:
        model.addBookTag(catalog, booktag)

# ======================================
# Funciones de consulta sobre el catálogo
# ======================================


def getBestBooks(catalog, number):
    """
    Retorna los mejores libros según su promedio
    """
    bestbooks = model.getBestBooks(catalog, number)
    return bestbooks


def countBooksByTag(catalog, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    return model.countBooksByTag(catalog, tag)


def booksSize(catalog):
    """
    Numero de libros cargados al catalogo
    """
    return model.booksSize(catalog)


def authorsSize(catalog):
    """
    Numero de autores cargados al catalogo
    """
    return model.authorsSize(catalog)


def tagsSize(catalog):
    """
    Numero de tags cargados al catalogo
    """
    return model.tagsSize(catalog)


def getBooksByAuthor(catalog, authorname):
    """
    Retorna los libros de un autor
    """
    authorinfo = model.getBooksByAuthor(catalog, authorname)
    return authorinfo


def getBooksByTag(catalog, tagname):
    """
    Retorna los libros que han sido marcados con
    una etiqueta
    """
    books = model.getBooksByTag(catalog, tagname)
    return books


def getBooksYear(catalog, year):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    # TODO: modificaciones para medir el tiempo y memoria
    books = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    books = model.getBooksByYear(catalog, year)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return books, delta_time, delta_memory


def sortBooksByYear(catalog, year, fraction, rank):
    """
    Retorna los libros que fueron publicados
    en un año ordenados por rating
    """
    # TODO: modificaciones para medir el tiempo y memoria
    # respuesta por defecto
    books = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    books = model.sortBooksByYear(catalog, year, fraction, rank)

    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el proceso para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return books, delta_time, delta_memory

# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    time.process_time()
    return float(time.perf_counter()*1000)
    


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
