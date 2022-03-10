import os
import openai

openai.api_key = #API KEY HERE

pre="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\n"
print("I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\n")

while 1:
	newQ=input("Q: ")

	pre=pre+"Q: "+newQ+"\nA:"

	response = openai.Completion.create(
  		engine="text-davinci-001",
  		prompt=pre+"\nA:",
  		temperature=0,
  		max_tokens=100,
  		top_p=1,
  		frequency_penalty=0.0,
  		presence_penalty=0.0,
  		stop=["\n"]
		)
	print("A:"+response.choices[0].text+"\n")

	pre= pre+"A:"+response.choices[0].text+"\n\n"
	
	


