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
import random
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

def get_response_prueba(pregunta,respuesta):
    return openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt_prueba(pregunta,respuesta),
                temperature=0.6,
            ).choices[0].text

def generate_prompt(pregunta):
    return """Soy un chatbot de real Jadrín botánico, puedo contertar las preguntas sobre las plantas y sobre el jardñin botánico.

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

visita1Plants=["Granado","Tejo","Almez","Pino del Himalaya","Pavonia","Quillay","Caboa americana"]
visita1Plants1=["Punica granatum","taxtus baccata","celtis australis","Pinus wallichiana","pavonia hastata","quillaja saponaria","swietenia mahagoni"]
respuesta=[]
list_plants=[]
nombres=[]
respuestasCorrectas=[]

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
         mapLocation=location1[name1.index(planta_asked.lower())]
         dispatcher.utter_message(attachment = get_location(mapLocation.split(",")[0]) )
#         dispatcher.utter_message(mapLocation.split(",")[0])
#         dispatcher.utter_message(get_location(mapLocation.split(",")[0]))
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

class ActionIniciarVisita1(Action):

     def name(self):
         return "action_iniciar_visita_1"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
         if(tracker.get_slot("is_visita_guiada")=='0'):
             dispatcher.utter_message("Visita guiada simple iniciada. En la izquierda de la entrada de Puerta Norte del Real Jardín Botánico está el Granado o Punica granatum. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.1"))
#             dispatcher.utter_message(attachment = "map="+"40.412209"+","+"-3.691701" )
             return[SlotSet("is_visita_guiada", "1")]
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
#             dispatcher.utter_message(attachment = "map="+"40.412209"+","+"-3.691701" )
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
#             dispatcher.utter_message(attachment = "map="+"40.412209"+","+"-3.691701" )
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

class ActionConfirmarLlegada(Action):

     def name(self):
         return "action_confirmar_llegada"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         nplanta=tracker.get_slot("is_visita_guiada")
         dispatcher.utter_message("¿Ya estás al lado de "+plants[ord(nplanta)-49]+", y pasar a la siguiente planta de la visita?")
         return[]

class ActionAvanzarVisita(Action):

     def name(self):
         return "action_avanzar_visita"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         result="0"
         nplanta=tracker.get_slot("is_visita_guiada")
         if(nplanta=="1"):
             result="2"
             dispatcher.utter_message("Ahora sigue recto para llegar al Tejo o taxtus baccata. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.3"))
         elif(nplanta=="2"):
             result="3"
             dispatcher.utter_message("Ahora gira a la derecha para llegar al Almez o celtis australis. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.4"))
         elif(nplanta=="3"):
             result="4"
             dispatcher.utter_message("Ahora sigue un poco mas a la izquierda para llegar al Pino del Himalaya o Pinus wallichiana. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.8"))
         elif(nplanta=="4"):
             result="5"
             dispatcher.utter_message("Ahora sigue recto hasta llegar al Paseo de Carlos III y girar a la izquierda hasta pasar por el Paseo Alto de Gómez Ortega y delante esta Pavonia o pavonia hastata. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.9"))
         elif(nplanta=="5"):
             result="6"
             dispatcher.utter_message("Mirando al lago a tu izquierda está Quillay o quillaja saponaria. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("e.5"))
         elif(nplanta=="6"):
             result="-1"
             dispatcher.utter_message("Ahora sigue recto para llegar al Caboa americana o swietenia mahagoni. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("v.2"))
         elif(nplanta=="-1"):
             result='0'
             dispatcher.utter_message("Ya has terminado la visita, ha sido un placer ayudarte.")
             return[SlotSet("is_visita_guiada", "0"),FollowupAction(name="action_ask_prueba")]
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
             result='-1'
             dispatcher.utter_message("Finalmente, sigue camiando hacia el oeste un poco más y verás a aesculus x carnea briotii o castaño de Indias rojo. Avisame cuando estés.")
             dispatcher.utter_message(attachment = get_location("c.3"))

         return[SlotSet("is_visita_guiada", result),FollowupAction(name="action_listen")]


