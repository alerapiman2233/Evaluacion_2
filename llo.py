import os
import requests
from faker import Faker

# Configuración
API_KEY = os.getenv("API_KEY")  # asegúrate de exportar tu API_KEY en la VM
BASE_URL = "http://library.demo.local/api/v1/books"

# Si tu API usa Bearer token
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

fake = Faker()

# Crear y enviar 50 libros aleatorios
for i in range(50):
    libro = {
        "id": 8 + i,  # id único para evitar duplicados
        "title": fake.sentence(nb_words=4),
        "author": fake.name(),
        "isbn": fake.isbn10(separator="")
    }
    response = requests.post(BASE_URL, json=libro, headers=headers)
    if response.status_code in (200, 201):
        print(f"✅ Libro {i+1} agregado correctamente")
    else:
        print(f"❌ Error al agregar libro {i+1}: {response.status_code} -> {response.text}")

# Listar todos los libros, ordenados por autor, incluyendo ISBN

print("\n📚 Listando todos los libros ordenados por autor...")

all_books = []
limit = 50
offset = 0

while True:
    params = {
        "includeISBN": "true",
        "limit": limit,
        "offset": offset,
        "sort": "author"  # Cambia si tu API usa otro parámetro para ordenar
    }

    resp = requests.get("http://library.demo.local/api/v1/books?includeISBN=true", params=params)

    if resp.status_code != 200:
        print("❌ Error al listar libros:", resp.status_code)
        print("Respuesta:", resp.text)
        break

    books = resp.json()
    if not books:
        break

    all_books.extend(books)
    offset += limit

# Mostrar libros
print(f"\n📖 Total de libros listados: {len(all_books)}")
for libro in all_books:
    print(f"ID: {libro.get('id')} | Autor: {libro.get('author')} | Título: {libro.get('title')} | ISBN: {libro.get('ISBN')}")




import requests

API_KEY = "3368c6a9-eb8b-4bfb-8fc1-82097d595929"
BASE_URL = "https://graphhopper.com/api/1/route"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"

def formatear_numero(num):
    return f"{num:.2f}"

def geocodificar(lugar):
    """Convierte un nombre de lugar a coordenadas (lat,lon) usando GraphHopper."""
    params = {"q": lugar, "limit": 1, "key": API_KEY}
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code != 200:
        print(f"Error en geocodificación: {response.status_code}")
        return None

    data = response.json()
    if not data["hits"]:
        print(f"No se encontraron coordenadas para '{lugar}'.")
        return None

    lat = data["hits"][0]["point"]["lat"]
    lon = data["hits"][0]["point"]["lng"]
    return f"{lat},{lon}"

def obtener_ruta(origen, destino):
    params = {
        "point": [origen, destino],
        "locale": "es",
        "key": API_KEY,
        "instructions": "true",
        "calc_points": "true"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error al obtener la ruta: {response.status_code}")
        print(response.text)  # <-- útil para depurar
        return None

    return response.json()

def imprimir_instrucciones(ruta):
    print("\nInstrucciones del viaje:")
    for leg in ruta["paths"]:
        for instr in leg["instructions"]:
            texto = instr["text"]
            distancia = formatear_numero(instr["distance"] / 1000)  # km
            tiempo = formatear_numero(instr["time"] / 60000)  # minutos
            print(f"- {texto} (Distancia: {distancia} km, Tiempo: {tiempo} min)")

def main():
    print("=== Software de Geolocalización con GraphHopper ===")
    while True:
        origen_nombre = input("Ingrese la ubicación de origen (o 's' para salir): ").strip()
        if origen_nombre.lower() in ("s", "salir"):
            print("Saliendo del programa. ¡Hasta luego!")
            break

        destino_nombre = input("Ingrese la ubicación de destino (o 's' para salir): ").strip()
        if destino_nombre.lower() in ("s", "salir"):
            print("Saliendo del programa. ¡Hasta luego!")
            break

        print("Buscando coordenadas...")
        origen = geocodificar(origen_nombre)
        destino = geocodificar(destino_nombre)

        if not origen or not destino:
            print("No se pudieron obtener coordenadas válidas. Intente con otro lugar.")
            continue

        print("Calculando la ruta, por favor espere...")
        ruta = obtener_ruta(origen, destino)
        if ruta:
            imprimir_instrucciones(ruta)
        else:
            print("No se pudo obtener la ruta. Intente de nuevo.")

if __name__ == "__main__":
    main()
