# This files contains your custom actions which can be used to run
# custom Python code.
#
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
import random
import openai

openai.api_key = "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"

def get_response(pregunta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(pregunta),
                temperature=0.6,
            ).choices[0].text

def get_similar_response(pregunta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt_similar(pregunta),
                temperature=0.6,
            ).choices[0].text

def get_response_prueba(pregunta,respuesta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt_prueba(pregunta,respuesta),
                temperature=0.6,
            ).choices[0].text

def generate_prompt(pregunta):
    return """Contesta la pregunta.

Pregunta:  ¿A que familia pertenece Abies Alba?
Respuesta: Abies alba es una especie arbórea de la familia de las pináceas.
Pregunta: ¿Hasta cuantos metros de altura puede llegar?
Respuesta: Puede alcanzar los 60 metros de altura.
Pregunta: {}
Respuesta: """.format(
        pregunta
    )

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

#plants=["Granado","Tejo","Almez","Pino del Himalaya","Pavonia","Quillay","Caboa americana"]
#plants1=["Punica granatum","taxtus baccata","celtis australis","Pinus wallichiana","pavonia hastata","quillaja saponaria","swietenia mahagoni"]
respuesta=[]
list_plants=[]
nombres=[]
respuestasCorrectas=[]
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
         list_plants.append(tracker.get_slot("plant_name"))
#         dispatcher.utter_message(planta_asked+" está en "+location1[name1.index(planta_asked.lower())])
         
         dispatcher.utter_message("map="+"40.410786"+","+"-3.690956")
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

class ActionAnswerPlantFam(Action):

     def name(self):
         return "action_answer_plant_fam"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         planta_asked=tracker.get_slot("plant_name")
         list_plants.append(planta_asked)
         dispatcher.utter_message(planta_asked+" es de la familia "+fam1[name1.index(planta_asked.lower())])

         return []

class ActionAskVisita(Action):

     def name(self):
         return "action_ask_visita"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("¿Quieres iniciar la visita?")

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

class ActionIniciarVisita(Action):

     def name(self):
         return "action_iniciar_visita"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         if(tracker.get_slot("is_visita_guiada")=='0'):
             dispatcher.utter_message("Visita iniciada.")
             
             return[SlotSet("is_visita_guiada", "1")]
         else:
             dispatcher.utter_message("Ya has iniciado la visita.")
             return[]

class ActionRegistrarNombres(Action):

     def name(self):
         return "action_registrar_nombres"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         nombres=tracker.get_slot("nombres").split(",")
         stringaux=""
         for i in nombres:
            i=i.replace(",y "," ").strip()
            respuestasCorrectas.append(chr(65+random.randint(0,2)))
            stringaux=stringaux+i+", "
         dispatcher.utter_message(stringaux+" verdad?")
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
         nprueba=int(tracker.get_slot("is_prueba"))
         if nprueba < len(nombres):
             respuesta.append(tracker.get_slot("respuesta"))
             dispatcher.utter_message(nombres[nprueba]+", esta pregunta es para tí: \n"+get_response_prueba(random.choice(list_plants),respuestasCorrectas[nprueba]))
             return[SlotSet("is_prueba", str(nprueba+1))]
         elif nprueba ==len(nombres) :
             string1=""
             for i in range(len(respuesta)):
                  if respuesta[i] !=respuestasCorrectas[i]:
                       string1=string1+nombres[i]+" se ha equivocado, la respuesta correcta es:"+respuestasCorrectas[i]+". "
             if string1 =="":
                  dispatcher.utter_message("Enohabuena! todas vuestras respuestas son correctas.")
             else:
                  dispatcher.utter_message(string1)
             return[SlotSet("is_prueba", "0")]

class ActionListaPlantas(Action):

     def name(self):
         return "action_lista_plantas"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         dispatcher.utter_message("Esta son las plantas registradas: "+list_plants)




