# This files contains your custom actions which can be used to run
# custom Python code.
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import csv
import os
import json
import random
import requests
import openai

openai.api_key = ""

def get_response(pregunta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(pregunta),
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            ).choices[0].text

def get_similar_response(pregunta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt_similar(pregunta),
                temperature=0.6,
            ).choices[0].text

def generate_prompt_similar(pregunta):
    return """Genera una frase del mismo significado.

Frase: {}
Respuesta: """.format(
        pregunta
    )

def generate_prompt_prueba(pregunta,respuesta):
    return """Genera una pregunta de tipo test sobre propiedades de {} con el siguiente formato y que la respuesta correcta sea la {}:

"¿Cuál es la planta que pertenece a la familia de Ulmaceae? 
           A. Celtis autralis   B. Quillay  C. Tejo
¿Cuatos metros puede alcanzar Quercus frainetto? 
           A. 10 m  B. 20 m  C. 30 m
¿Que planta tiene  los flores precoces, agrupadas en inflorescencias de hasta 30 flores?
           A. Taxus cuspidata  B. Ulmus minor  C. Quercus ilex ballota"
: """.format(
        pregunta,respuesta
    )
#

nombres=[]

coordenadas=[["c.1","map=40.412209,-3.691701"],
    ["c.2","map=40.412157,-3.692182"],
    ["c.3","map=40.411877,-3.691632"],
    ["c.4","map=40.411824,-3.692110"],
    ["c.5","map=40.411540,-3.691553"],
    ["c.6","map=40.411499,-3.692038"],
    ["c.7","map=40.411222,-3.691476"],
    ["c.8","map=40.411174,-3.691954"],
    ["c.9","map=40.410870,-3.691403"],
    ["c.10","map=40.410802,-3.691887"],
    ["c.11","map=40.410549,-3.691332"],
    ["c.12","map=40.410494,-3.691809"],
    ["c.13","map=40.410229,-3.691256"],
    ["c.14","map=40.410162,-3.691732"],
    ["c.15","map=40.409896,-3.691181"],
    ["c.16","map=40.409838,-3.691696"],
    ["e.0","map=40.410114,-3.690296"],
    ["e.1","map=40.410347,-3.690310"],
    ["e.2","map=40.410681,-3.690378"],
    ["e.3","map=40.410994,-3.690454"],
    ["e.4","map=40.411348,-3.690540"],
    ["e.5","map=40.411665,-3.690604"],
    ["e.6","map=40.411998,-3.690683"],
    ["e.7","map=40.411950,-3.691089"],
    ["e.8","map=40.411611,-3.691010"],
    ["e.9","map=40.411295,-3.690938"],
    ["e.10","map=40.410943,-3.690859"],
    ["e.11","map=40.410624,-3.690790"],
    ["e.12","map=40.410295,-3.690715"],
    ["e.13","map=40.410010,-3.690651"],
    ["f.1","map=40.412108,-3.690421"],
    ["f.2","map=40.412016,-3.690181"],
    ["f.3","map=40.411999,-3.689901"],
    ["f.4","map=40.411798,-3.689804"],
    ["f.5","map=40.411798,-3.690013"],
    ["f.6","map=40.411720,-3.690191"],
    ["f.7","map=40.411676,-3.690331"],
    ["f.8","map=40.411549,-3.690156"],
    ["f.9","map=40.411564,-3.689794"],
    ["f.10","map=40.411440,-3.689699"],
    ["f.11","map=40.411442,-3.689928"],
    ["f.12","map=40.411375,-3.690206"],
    ["f.13","map=40.411250,-3.689933"],
    ["f.14","map=40.411094,-3.690166"],
    ["f.15","map=40.411071,-3.689886"],
    ["f.16","map=40.411098,-3.689641"],
    ["f.17","map=40.410949,-3.689686"],
    ["f.18","map=40.410907,-3.689991"],
    ["f.19","map=40.410723,-3.690101"],
    ["f.20","map=40.410660,-3.689993"],
    ["f.21","map=40.410700,-3.689794"],
    ["f.22","map=40.410767,-3.689556"],
    ["f.23","map=40.410565,-3.689554"],
    ["f.24","map=40.410424,-3.689851"],
    ["f.25","map=40.410369,-3.690043"],
    ["f.26","map=40.411881,-3.689626"],
    ["f.27","map=40.410767,-3.689379"],
    ["pu","map=40.410926,-3.689226"],
    ["tol.1","map=40.410476,-3.689326"],
    ["tol.2","map=40.410392,-3.689521"],
    ["tol.3","map=40.410392,-3.689521"],
    ["plat.1","map=40.412224,-3.691400"],
    ["plat.3","map=40.411928,-3.691333"],
    ["plat.5","map=40.411583,-3.691256"],
    ["plat.9","map=40.410917,-3.691105"],
    ["plat.11","map=40.410600,-3.691043"],
    ["plat.13","map=40.410267,-3.690986"],
    ["plat.15","map=40.409981,-3.690908"],
    ["v.1","map=40.412221,-3.690791"],
    ["v.2","map=40.412237,-3.691161"],
    ["ap.5","map=40.410368,-3.689275"],
    ["ap.6","map=40.410080,-3.689721"],
    ["ap.7","map=40.409883,-3.689590"],
    ["ap.8","map=40.409829,-3.690439"],
    ["alf12","map=40.411926,-3.689049"]]

def get_location(location):
    for i in coordenadas:
        if i[0]== location or i[0]+"." in location:
            return i[1]

    return ""
def get_image(plant):
    response = requests.get("https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles="+plant)
    j=response.json()
    page=list(j["query"]["pages"].values())
    return page[0]["original"]["source"]
def get_summary(plant):
    response = requests.get("https://es.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="+plant)
    j=response.json()
    page=list(j["query"]["pages"].values())
    return page[0]["extract"]
#leer csv

name1 = []
fam1 = []
location1 = []

with open("actions/datos.csv", newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        name1.append(row[0])
        fam1.append(row[1])
        location1.append(row[2])



class ActionAnswerPlantLocation(Action):

     def name(self):
         return "action_answer_plant_location"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         planta_asked=tracker.get_slot("plant_name")
         mapLocation=location1[name1.index(planta_asked.lower())]
         dispatcher.utter_message(attachment = get_location(mapLocation.split(",")[0]) )
         return []

class ActionRandomPlanta(Action):

     def name(self):
         return "action_random_planta"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         dispatcher.utter_message(text =random.choice(name1))
         return []

class ActionResponderGPT3(Action):

     def name(self):
         return "action_responder_GPT3"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         message=tracker.latest_message['text']
         dispatcher.utter_message(get_response(message))
#         dispatcher.utter_message(message)
         return[]

class ActionResponderWikipedia(Action):

     def name(self):
         return "action_responder_wikipedia"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         message=tracker.latest_message['text']
         planta_asked=tracker.get_slot("plant_name")
         dispatcher.utter_message(image = get_image(planta_asked))
         dispatcher.utter_message(get_summary(planta_asked))
         return[]

class ActionAnswerPlantFam(Action):

     def name(self):
         return "action_answer_plant_fam"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         planta_asked=tracker.get_slot("plant_name")
         dispatcher.utter_message(planta_asked+" es de la familia "+fam1[name1.index(planta_asked.lower())])

         return []

class ActionAskVisita(Action):

     def name(self):
         return "action_ask_visita"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         dispatcher.utter_message("La visita guiada se trata de una ruta popular del jardín en la que te iré diciendo ubicaciones de la plantas populares. Existen tres tipos de visitas guiadas:")
         dispatcher.utter_message("La visita guiada simple incluye las siete plantas más interesantes del jardín.")
         dispatcher.utter_message("La visita guiada completa atraviesa casi todos los lugares del jardín.")
         dispatcher.utter_message("La visita guiada casual es intermediario de las dos anteriores.")
         dispatcher.utter_message("¿Cual es la visita guiada que desea?")
         return []

class ActionActualizarDatos(Action):

     def name(self):
         return "action_actualizar_datos"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         import scrap

         return []

class ActionAskPrueba(Action):

     def name(self):
         return "action_ask_prueba"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("¿Quieres iniciar una pequeña prueba sobre las plantas que has visitado?")

         return []

class ActionTerminarVisita(Action):

     def name(self):
         return "action_terminar_visita"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Visita guiada terminada.")
         nvisita=tracker.get_slot("is_visita_guiada")
         if(nvisita.startswith("1")):
             return[SlotSet("is_prueba", "100"),SlotSet("is_visita_guiada", "0"), FollowupAction(name="action_ask_prueba")]
         if(nvisita.startswith("2")):
             return[SlotSet("is_prueba", "200"),SlotSet("is_visita_guiada", "0"), FollowupAction(name="action_ask_prueba")]
         if(nvisita.startswith("3")):
             return[SlotSet("is_prueba", "300"), SlotSet("is_visita_guiada", "0"),FollowupAction(name="action_ask_prueba")]
         return []

class ActionIniciarVisita1(Action):

     def name(self):
         return "action_iniciar_visita_1"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         if(tracker.get_slot("is_visita_guiada")=='0'):
             dispatcher.utter_message("Visita guiada simple iniciada. En la izquierda de la entrada de Puerta Norte del Real Jardín Botánico está el Granado o Punica granatum. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.1"))
             return[SlotSet("is_visita_guiada", "101")]
         else:
             dispatcher.utter_message("Ya habías iniciado la visita guiada..")
             return[]

class ActionIniciarVisita2(Action):

     def name(self):
         return "action_iniciar_visita_2"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         if(tracker.get_slot("is_visita_guiada")=='0'):
             dispatcher.utter_message("Visita guiada completa iniciada. En la derecha de la entrada de Puerta Norte del Real Jardín Botánico está el fraxinus pennsylvanica o fresno rojo americano. Avisame cuando llegues")
             dispatcher.utter_message(attachment = get_location("c.2"))
             return[SlotSet("is_visita_guiada", "201")]
         else:
             dispatcher.utter_message("Ya habías iniciado la visita guiada..")
             return[]


class ActionIniciarVisita3(Action):

     def name(self):
         return "action_iniciar_visita_3"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         if(tracker.get_slot("is_visita_guiada")=='0'):
             dispatcher.utter_message("Visita guiada casual iniciada. En la derecha de la entrada de Puerta Norte del Real Jardín Botánico está el morus alba o morera blanca. Avísame cuando llegues por favor.")
             dispatcher.utter_message(attachment = get_location("c.4"))
             return[SlotSet("is_visita_guiada", "301")]
         else:
             dispatcher.utter_message("Ya habías iniciado la visita guiada..")
             return[]

class ActionRegistrarNombres(Action):

     def name(self):
         return "action_registrar_nombres"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         nombres.clear()
         for i in tracker.latest_message['entities']:
             nombres.append(i['value']) 
         
         dispatcher.utter_message(", ".join(nombres[0:-1])+" y "+nombres[-1]+" verdad?")
         random.shuffle(nombres)
         return[]
    
class ActionVerMapa(Action):

     def name(self):
         return "action_ver_mapa"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         dispatcher.utter_message("Aquí tienes un link para ver el mapa en datalle")
         dispatcher.utter_message(image = "https://rjb.csic.es/wp-content/uploads/2021/09/plano-accesible.png")
             
         return[]

class ActionPrueba(Action):

     def name(self):
         return "action_prueba"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         nprueba=tracker.get_slot("is_prueba")
         if nprueba =="100":
             respuesta=tracker.get_slot("respuesta")
             dispatcher.utter_message(nombres[0]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("Pinus wallichiana"))
             dispatcher.utter_message("A. Pinus wallichiana\nB. Celtis australis\nC. Taxus baccata")
             return[SlotSet("is_prueba", "101")]
         elif nprueba =="101":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="a":
                 dispatcher.utter_message(nombres[0]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Pinus wallichiana.")
             else:
                 dispatcher.utter_message(nombres[0]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es A. Pinus wallichiana.")
             dispatcher.utter_message(nombres[1%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("pavonia hastata"))
             dispatcher.utter_message("A. Taxus baccata\nB. Pavonia hastata\nC. Quillaja saponaria")
             return[SlotSet("is_prueba", "102")]
         elif nprueba =="102":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="b":
                 dispatcher.utter_message(nombres[1%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Pavonia hastata.")
             else:
                 dispatcher.utter_message(nombres[1%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es B. Pavonia hastata.")
             dispatcher.utter_message(nombres[2%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál de las imagenes es Swietenia mahagoni?")
             dispatcher.utter_message("A.")
             dispatcher.utter_message(image = get_image("Celtis laevigata"))
             dispatcher.utter_message("B.")
             dispatcher.utter_message(image = get_image("Swietenia mahagoni"))
             dispatcher.utter_message("C.")
             dispatcher.utter_message(image = get_image("picea abies"))
             return[SlotSet("is_prueba", "103")]
         elif nprueba =="103":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="b":
                 dispatcher.utter_message(nombres[2%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es B.")
             else:
                 dispatcher.utter_message(nombres[2%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es B.")
             dispatcher.utter_message(nombres[3%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("celtis laevigata"))
             dispatcher.utter_message("A. Taxus baccata\nB. Celtis laevigata\nC. Quillaja saponaria")
             return[SlotSet("is_prueba", "104")]
         elif nprueba =="104":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="b":
                 dispatcher.utter_message(nombres[3%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Celtis laevigata.")
             else:
                 dispatcher.utter_message(nombres[3%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es B. Celtis laevigata")
             dispatcher.utter_message(nombres[4%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál de las imagenes es Taxus baccata?")
             dispatcher.utter_message("A.")
             dispatcher.utter_message(image = get_image("quercus ilex"))
             dispatcher.utter_message("B.")
             dispatcher.utter_message(image = get_image("Taxus baccata"))
             dispatcher.utter_message("C.")
             dispatcher.utter_message(image = get_image("quercus suber"))
             return[SlotSet("is_prueba", "105")]
         elif nprueba =="105":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="b":
                 dispatcher.utter_message(nombres[4%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es B.")
             else:
                 dispatcher.utter_message(nombres[4%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es B.")
             dispatcher.utter_message("Prueba terminada. ¿Algo más en te puedo ayudar?")
             return[SlotSet("is_prueba", "0")]
         if nprueba =="200":
             respuesta=tracker.get_slot("respuesta")
             dispatcher.utter_message(nombres[0]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("Celtis occidentalis"))
             dispatcher.utter_message("A. Diospyros lotus\nB. Celtis occidentalis\nC. Taxus baccata")
             return[SlotSet("is_prueba", "201")]
         elif nprueba =="201":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="b":
                 dispatcher.utter_message(nombres[0]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Celtis occidentalis.")
             else:
                 dispatcher.utter_message(nombres[0]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es B. Celtis occidentalis.")
             dispatcher.utter_message(nombres[1%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("Juglans regia"))
             dispatcher.utter_message("A. Ginkgo biloba\nB. Abies nordmanniana\nC. Juglans regia")
             return[SlotSet("is_prueba", "202")]
         elif nprueba =="202":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="c":
                 dispatcher.utter_message(nombres[1%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Juglans regia.")
             else:
                 dispatcher.utter_message(nombres[1%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es C. Juglans regia.")
             dispatcher.utter_message(nombres[2%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál de las imagenes es Ginkgo biloba?")
             dispatcher.utter_message("A.")
             dispatcher.utter_message(image = get_image("celtis occidentalis"))
             dispatcher.utter_message("B.")
             dispatcher.utter_message(image = get_image("melia azedarach"))
             dispatcher.utter_message("C.")
             dispatcher.utter_message(image = get_image("Ginkgo biloba"))
             return[SlotSet("is_prueba", "203")]
         elif nprueba =="203":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="c":
                 dispatcher.utter_message(nombres[2%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es C.")
             else:
                 dispatcher.utter_message(nombres[2%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es C.")
             dispatcher.utter_message(nombres[3%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál es la planta que muestra en la imagen?")
             dispatcher.utter_message(image = get_image("Fraxinus latifolia"))
             dispatcher.utter_message("A. Taxus baccata\nB. Citrus aurantium\nC. Fraxinus latifolia")
             return[SlotSet("is_prueba", "204")]
         elif nprueba =="204":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="c":
                 dispatcher.utter_message(nombres[3%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es Fraxinus latifolia.")
             else:
                 dispatcher.utter_message(nombres[3%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es C. Fraxinus latifolia.")
             dispatcher.utter_message(nombres[4%len(nombres)]+", esta pregunta es para tí: \n"+"¿Cuál de las imagenes es Cercis chinensis?")
             dispatcher.utter_message("A.")
             dispatcher.utter_message(image = get_image("Cercis chinensis"))
             dispatcher.utter_message("B.")
             dispatcher.utter_message(image = get_image("Ulmus minor"))
             dispatcher.utter_message("C.")
             dispatcher.utter_message(image = get_image("Quercus suber"))
             return[SlotSet("is_prueba", "205")]
         elif nprueba =="205":
             respuesta=tracker.get_slot("respuesta")
             if respuesta.lower()=="a":
                 dispatcher.utter_message(nombres[4%len(nombres)]+", ¡enhorabuena! Efectivamente, la respuesta correcta es A.")
             else:
                 dispatcher.utter_message(nombres[4%len(nombres)]+", Lamentablemente la respuesta "+respuesta.upper()+" es incorrecta, la respuesta correcta es A.")
             dispatcher.utter_message("Prueba terminada. ¿Algo más en te puedo ayudar?")
             return[SlotSet("is_prueba", "0")]
         dispatcher.utter_message("error:action_prueba "+nprueba)
         return[]

class ActionListaPlantasInicial(Action):

     def name(self):
         return "action_lista_plantas_inicial"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         letra=tracker.get_slot("inicial_planta").lower()
         lista=[]
         for nombre in name1:
             e=nombre.split()[0]+" "+nombre.split()[1]
             if e not in lista and e.startswith(letra):
                 lista.append(e)
         if lista :
             dispatcher.utter_message("Estas son las plantas que empiezan con la letra '" +letra+ "' : " +", ".join(lista)+".")
         else:
             dispatcher.utter_message("No hay ninguna planta de la base de datos que empieza con la letra '"+letra+"'.")
         return[]




class ActionAvanzarVisita(Action):

     def name(self):
         return "action_avanzar_visita"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         result="0"
         nplanta=tracker.get_slot("is_visita_guiada")
         if(nplanta=="101"):
             result="102"
             dispatcher.utter_message("Ahora sigue recto para llegar al Tejo o taxus baccata. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.3"))
         elif(nplanta=="102"):
             result="103"
             dispatcher.utter_message("Ahora gira a la derecha para llegar al Almez o celtis australis. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.4"))
         elif(nplanta=="103"):
             result="104"
             dispatcher.utter_message("Ahora sigue un poco mas a la izquierda para llegar al Pino del Himalaya o Pinus wallichiana. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.8"))
         elif(nplanta=="104"):
             result="105"
             dispatcher.utter_message("Ahora sigue recto hasta llegar al Paseo de Carlos III y girar a la izquierda hasta pasar por el Paseo Alto de Gómez Ortega y delante esta Pavonia o pavonia hastata. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.9"))
         elif(nplanta=="105"):
             result="106"
             dispatcher.utter_message("Mirando al lago a tu izquierda está Quillay o quillaja saponaria. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.5"))
         elif(nplanta=="106"):
             result="107"
             dispatcher.utter_message("Ahora sigue recto para llegar al Caboa americana o swietenia mahagoni. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("v.2"))
         elif(nplanta=="107"):
             dispatcher.utter_message("Ya has terminado la visita, ha sido un placer ayudarte.")
             return[SlotSet("is_prueba", "100"),SlotSet("is_visita_guiada", "0"),FollowupAction(name="action_ask_prueba")]
         elif(nplanta=="0"):
             dispatcher.utter_message("No has iniciado la visita.")
             return[FollowupAction(name="action_ask_visita")]
         elif(nplanta=="201"):
             result='202'
             dispatcher.utter_message("Ahora sigue yendo hacia el sur para ver a punica granatum o granado. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.6"))
         elif(nplanta=="202"):
             result='203'
             dispatcher.utter_message("Seguiendo el camino hacia el sur cruzando por el Paseo de Carlos III podrás ver a taxus baccata o tejo negro. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.10"))
         elif(nplanta=="203"):
             result='204'
             dispatcher.utter_message("Seguiendo el camino hacia el sur hasta el ultimo bloque ansted de salir del jardín podrás ver a celtis bungeana. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.16"))
         elif(nplanta=="204"):
             result='205'
             dispatcher.utter_message("Ahora sigue el borde del jardín y hacia el este econtrarás a celtis occidentalis o almez americano. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.15"))
         elif(nplanta=="205"):
             result='206'
             dispatcher.utter_message("Ahora volviendo hacia el norte dos bloques y verás a diospyros lotus. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.11"))
         elif(nplanta=="206"):
             result='207'
             dispatcher.utter_message("Ahora si sigues yendo hacia el norte un poco mas y luego giras hacia el este cruzando por el Paseo Bajo de Gómez y Ortega, a tu mano derecha estará ulmus minor o olmo común. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.10"))
         elif(nplanta=="207"):
             result='208'
             dispatcher.utter_message("Ahora volviendo hacia el sur dos bloques y verás a juglans regia o nogal común. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.12"))
         elif(nplanta=="208"):
             result='209'
             dispatcher.utter_message("A la mano izquierda está el bloque donde hay la famosa planta de ginkgo biloba o ginkgo. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.1"))
         elif(nplanta=="209"):
             result='210'
             dispatcher.utter_message("Hacia el este, cruzando por el paseo de Multis, al rededor de la glorieta de los Tilos Sur está prunus lusitanica o laurel portugués. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("f.24"))
         elif(nplanta=="210"):
             result='211'
             dispatcher.utter_message("Hacia el norte, al rededor de la glorieta y estanque de Linneo está abies nordmanniana o abeto de Normandía. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("f.13"))
         elif(nplanta=="211"):
             result='212'
             dispatcher.utter_message("Sigue camiando hacia el norte y verás a fraxinus latifolia o fresno de Oregón. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("f.5"))
         elif(nplanta=="212"):
             result='213'
             dispatcher.utter_message("Caminar hacie el oeste y volviendo a cruzar por el paseo de Multis e ir hacia el norte verás a citrus aurantium o naranjo agrio. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.6"))
         elif(nplanta=="213"):
             result='214'
             dispatcher.utter_message("Sigue camiando hacia el oeste un poco más y verás a melia azedarach o cinamomo. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.7"))
         elif(nplanta=="214"):
             result='215'
             dispatcher.utter_message("Finalmente, sigue camiando hacia el oeste un poco más y verás a aesculus x carnea briotii o castaño de Indias rojo. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.3"))
         elif(nplanta=="215"):
             dispatcher.utter_message("Ya has terminado la visita, ha sido un placer ayudarte.")
             return[SlotSet("is_prueba", "200"),SlotSet("is_visita_guiada", "0"),FollowupAction(name="action_ask_prueba")]

         return[SlotSet("is_visita_guiada", result),FollowupAction(name="action_listen")]


