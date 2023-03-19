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

#
#

plants=["Granado","Tejo","Almez","Pino del Himalaya","Pavonia","Quillay","Caboa americana"]
plants1=["Punica granatum","taxtus baccata","celtis australis","Pinus wallichiana","pavonia hastata","quillaja saponaria","swietenia mahagoni"]
respuesta=[" "," "," "]

#leer csv

name1 = []
fam1 = []
location1 = []

with open("./actions/datos.csv", newline='') as csvfile:
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
         
#         dispatcher.utter_message(planta_asked+" está en "+location1[name1.index(planta_asked.lower())])
         
         dispatcher.utter_message("map="+"40.410786,-3.690956")
         return []

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
             dispatcher.utter_message("Visita iniciada. \nEn la izquierda de la entrada esta el Granado o Punica granatum. Avisame cuando estés.")
             return[SlotSet("is_visita_guiada", "1")]
         else:
             dispatcher.utter_message("Ya has iniciado la visita.")
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
         
         
         if nprueba =="0" :
             dispatcher.utter_message("¿Cuál es la planta que pertenece a la familia de Ulmaceae? \nA. Celtis autralis   B. Quillay  C. Tejo")
             return[SlotSet("is_prueba", "1")]

         elif nprueba =="1" :

             respuesta[0]=tracker.get_slot("respuesta")
             dispatcher.utter_message("¿Cuál es la planta que pertenece a la familia de Taxaceae? \nA. Celtis autralis   B. Almez  C. Swietenia mahagoni")
             return[SlotSet("is_prueba", "2")]

         elif nprueba =="2" :

             respuesta[1]=tracker.get_slot("respuesta")
             dispatcher.utter_message("¿Cuál es la planta que pertenece a la familia de Rutaceae? \nA. Quillaja saponaria   B. Granado  C. Tejo")
             return[SlotSet("is_prueba", "3")]
         elif nprueba =="3" :
             
             respuesta[2]=tracker.get_slot("respuesta")
             if (respuesta[0].lower()=='a' and respuesta[1].lower()=='b' and respuesta[2].lower()=='b'):
                   dispatcher.utter_message("Enohabuena! todas tus respuestas son correctas.")
             else:
                  dispatcher.utter_message("Alguna de tus respuestas es incorrecta.")
             return[SlotSet("is_prueba", "0")]

class ActionListaPlantas(Action):

     def name(self):
         return "action_lista_plantas"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         lista=""

         for i in range(len(name1)):
            lista=lista +name1[i]+", "
         dispatcher.utter_message("Esta son las plantas registradas: "+lista)

class ActionConfirmarLlegada(Action):

     def name(self):
         return "action_confirmar_llegada"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         nplanta=tracker.get_slot("is_visita_guiada")
         dispatcher.utter_message("¿Ya estás al lado de "+plants[ord(nplanta)-49]+"?")
         return[]

class ActionLlegadaConfirmada(Action):

     def name(self):
         return "action_llegada_confirmada"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         nplanta=tracker.get_slot("is_visita_guiada")
         return[SlotSet("is_visita_guiada", chr(ord(nplanta))),SlotSet("plant_llegada", plants[ord(nplanta)-49]),FollowupAction(name="action_avanzar_visita")] 

class ActionAvanzarVisita(Action):

     def name(self):
         return "action_avanzar_visita"


     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         nplanta=tracker.get_slot("is_visita_guiada")
         plantallegada=tracker.get_slot("plant_llegada")
         if(nplanta=="1" and (plantallegada.lower()==plants[0].lower() or plantallegada.lower()==plants1[0].lower())):
             result="2"
             dispatcher.utter_message("Ahora sigue recto para llegar al Tejo o taxtus baccata. Avisame cuando estés.")
         elif(nplanta=="2" and (plantallegada.lower()==plants[1].lower() or plantallegada.lower()==plants1[1].lower())):
             result="3"
             dispatcher.utter_message("Ahora gira a la derecha para llegar al Almez o celtis australis. Avisame cuando estés.")
         elif(nplanta=="3" and (plantallegada.lower()==plants[2].lower() or plantallegada.lower()==plants1[2].lower())):
             result="4"
             dispatcher.utter_message("Ahora sigue un poco mas a la derecha para llegar al Pino del Himalaya o Pinus wallichiana. Avisame cuando estés.")
         elif(nplanta=="4" and (plantallegada.lower()==plants[3].lower() or plantallegada.lower()==plants1[3].lower())):
             result="5"
             dispatcher.utter_message("Ahora sigue recto hasta llegar al Paseo de Carlos III y girar a la izquierda hasta pasar por el Paseo Alto de Gómez Ortega y delante esta Pavonia o pavonia hastata. Avisame cuando estés.")
         elif(nplanta=="5" and (plantallegada.lower()==plants[4].lower() or plantallegada.lower()==plants1[4].lower())):
             result="6"
             dispatcher.utter_message("Mirando al lago a tu izquierda está Quillay o quillaja saponaria. Avisame cuando estés.")
         elif(nplanta=="6" and (plantallegada.lower()==plants[5].lower() or plantallegada.lower()==plants1[5].lower())):
             result="7"
             dispatcher.utter_message("Ahora sigue recto para llegar al Caboa americana o swietenia mahagoni. Avisame cuando estés.")
         elif(nplanta=="7" and (plantallegada.lower()==plants[6].lower() or plantallegada.lower()==plants1[6].lower())):
             result='0'
             dispatcher.utter_message("Ya has terminado la visita, ha sido un placer ayudarte.")
             return[SlotSet("is_visita_guiada", "0"),FollowupAction(name="action_ask_prueba")]
         elif(nplanta=="0"):
             dispatcher.utter_message("No has iniciado la visita.")
             return[FollowupAction(name="action_ask_prueba")]
        
         return[SlotSet("is_visita_guiada", result),FollowupAction(name="action_listen")]
         



