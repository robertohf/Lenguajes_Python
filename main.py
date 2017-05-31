from flask import Flask, jsonify, request
import googlemaps, json, requests, base64
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def ejercicio1(origen, destino):
    gmaps = googlemaps.Client(key='AIzaSyBmelZAhVTODrw_gjtueTuHEs9Aka_z9nM')

    directions_result = gmaps.directions(origen,destino)

    json_result = directions_result[0]['legs'][0]['steps']

    lat = []
    lng = []    

    for x in xrange(len(json_result)):
        lat.append(str(directions_result[0]['legs'][0]['steps'][x]['start_location']['lat']))
        lng.append(str(directions_result[0]['legs'][0]['steps'][x]['start_location']['lng']))
        lat.append(str(directions_result[0]['legs'][0]['steps'][x]['end_location']['lat']))
        lng.append(str(directions_result[0]['legs'][0]['steps'][x]['end_location']['lng']))

    return lat,lng


def ejercicio2(origen):
    gmaps = googlemaps.Client(key='AIzaSyBmelZAhVTODrw_gjtueTuHEs9Aka_z9nM')

    geocode_result = gmaps.geocode(origen)

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    place_result = gmaps.places_nearby((lat,lng),500,type='restaurant')

    json_result = place_result['results']

    nombre = []
    lat = []
    lng = [] 

    for x in xrange(len(json_result)):
        nombre.append(place_result['results'][x]['name'])
        lat.append(str(place_result['results'][x]['geometry']['location']['lat']))
        lng.append(str(place_result['results'][x]['geometry']['location']['lng']))

    return nombre,lat,lng


def ejercicio4(bmp_name, alto, ancho):

    img = Image.open(bmp_name)

    width, height = img.size

    factorW = width/ancho
    factorH = height/alto

    newW = int(width/factorW)
    newH = int(height/factorH)

    newImage = Image.new('RGB',(newW,newH))
    pixels = newImage.load()

    for x in range(newW):
        for y in range(newH):
            pixels = img.getpixel((x*factorW,y*factorH))
            newImage.putpixel((x,y),(pixels))   


    newImage.save(bmp_name)

    with open(bmp_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string


def ejercicio3(bmp_name):

    img = Image.open(bmp_name)

    width, height = img.size

    newImage = Image.new('RGB', (width,height))
    pixels = newImage.load()

    for x in range(width):
        for y in range(height):
            pixels = img.getpixel((x,y))
            R,G,B = pixels

            average = (R+G+B)/3

            R = average
            G = average
            B = average

            newPixels = R,G,B 

            newImage.putpixel((x,y),(newPixels))


    newImage.save(bmp_name)

    with open(bmp_name, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string



def base64ToImage(name, data):

    im = Image.open(BytesIO(base64.b64decode(data)))

    bmp_name = name 

    im.save(bmp_name, 'BMP')

    return bmp_name


@app.route('/ejercicio1', methods=['POST'])
def post_ejercicio1():
    try:
        origen = request.json['origen']
        destino = request.json['destino']
    except:
        err={
            "Error": "no se especifico origen"
        }
        return jsonify(err), 400


    lat,lng = ejercicio1(origen,destino)

    res = {};
    for x in xrange( 0, len( lat ) ):
        res[x] = {
            "lat": lat [x],
            "lng": lng[x]
        }

    gmaps={
        "rutas": res,
    }

    return jsonify(gmaps), 201

@app.route('/ejercicio2', methods=['POST'])
def post_ejercicio2():
    try:
        origen = request.json['origen']
    except:
        err={
            "Error": "no se especifico origen"
        }
        return jsonify(err), 400

    nombre,lat,lng = ejercicio2(origen)

    
    res = {};
    for x in xrange( 0, len( nombre ) ):
        res[nombre[x]] = {
            "lat": lat[x],
            "lng": lng[x]
        }

    gmaps={
        "restaurantes": res
    }
    return jsonify(gmaps), 201

@app.route('/ejercicio3', methods=['POST'])
def post_ejercicio3():
    try:
        nombre = request.json['nombre']
        data = request.json['data']
    except:
        err={
            "Error": "no se especifico origen"
        }
        return jsonify(err), 400

    bmp_name = base64ToImage(nombre,data)
    data = ejercicio3(bmp_name)

    imagen={
    "nombre": nombre,
    "data": data 
    }

    return jsonify(imagen), 201

@app.route('/ejercicio4', methods=['POST'])
def post_ejercicio4():
    try:
        nombre = request.json['nombre']
        data = request.json['data']
        tamano = request.json['tamano']
        alto = request.json['tamano']['alto']
        ancho = request.json['tamano']['ancho']
    except:
        err={
            "Error": "no se especifico origen"
        }
        return jsonify(err), 400

    bmp_name = base64ToImage(nombre, data)
    ejercicio4(bmp_name, alto, ancho)

    imagen={
    "nombre": nombre,
    "data": data
    }

    return jsonify(imagen), 201  

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)
