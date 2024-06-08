from pypdf import PdfReader 
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
import time


def saveSummary(dictInfo,filename):
	with open(filename, "w") as outfile: 
		json.dump(dictInfo, outfile,indent=4)

def GenerateQuerry(model,dictInfo):
	prompt = f"Generate a search query for this information , the querry should be spesfic and try to cover the Tecnecalities and implimentations methods.\
	  Note provide only the query nothing more\
		{dictInfo} "
	responce = model.generate_content(prompt)
	return responce.text

def SearchTheWeb(URL,query,SEARCHKEY,CX):
	params = {"key":SEARCHKEY,"cx":CX,"q":query}
	responce = requests.get(URL,params=params)
	return responce.text

def process(text):
	keys = ["problem","requirments","Tec"]
	parts = text.split("--")
	text_dict = dict(zip(keys,list(map(lambda x:x.split(":")[1],parts))))
	return text_dict 

def extract(model,text):
	prompt = f"extract the problem that we are working on,requirments from this text and the Tec that i need to use your responce should be like this \
		Problem:\
			--requirments:\
				--Tec:\
					Note each requirment need to be seprated with / and don't add any additional points '{text}' "
	responce = model.generate_content(prompt)
	responce_dict = process(responce.text)
	return responce_dict

def ReadDoc(file_name):
	reader = PdfReader(file_name)
	file = ""

	for page in reader.pages:
		text = page.extract_text()
		file+="\n"+text
	return file

def GetItem(items):
	links = []
	for item in items:
		links.append(item["link"])
	return links


def ScrapData(TOKEN,links):
	for link in links:
		targetUrl = urllib.parse.quote(link)
		url = "http://api.scrape.do?token={}&url={}".format(TOKEN, targetUrl)
		response = requests.request("GET", url)
		if response.status_code ==200:
			html = response.text
			soup = BeautifulSoup(html, features="html.parser")

			for script in soup(["script", "style"]):
				script.extract()    

			text = soup.get_text()
			lines = (line.strip() for line in text.splitlines())
			chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
			text = '\n'.join(chunk for chunk in chunks if chunk)
			with open("info.txt","a") as f: 
				f.write(text)
			time.sleep(1)




def GeneratePlan(model,file_name,UserSol="i will build a manging system for electrical consumtion for smart house"):
	sample_file = genai.upload_file(path=file_name,
						display_name="Informations")
	
	prompt = f"Generate an Execution plan using this for this propsssed solution using this file . Note you are output should\
		 be profissional and in document format {UserSol} "
	responce = model.generate_content([sample_file,prompt])
	return responce.text

def main():
	load_dotenv()
	KEY = os.getenv("api")
	SEARCHKEY = os.getenv("search_key")
	TOKEN = os.getenv("token")
	CX = os.getenv("cx")
	URL = f"https://www.googleapis.com/customsearch/v1"
	Save=False
	file_name = "req.pdf"
	genai.configure(api_key=KEY)

	model = genai.GenerativeModel('gemini-1.5-pro')
	
	text = ReadDoc(file_name)
	print("Step 1- finished")
	responce = extract(model,text)
	if Save==True:
		saveSummary(responce,"summary.json")
	query = GenerateQuerry(model,responce["problem"])
	print("Step 2- finished")
	with open("queries.txt","a") as f:
		f.write(query)
	Searchdata = SearchTheWeb(URL,query,SEARCHKEY,CX) 
	print("Step 3- finished")
	SearchData = json.loads(Searchdata)
	
	saveSummary(SearchData,"searchData.json")
	
	items = SearchData["items"]
	links = GetItem(items)
	print("Step 4- finished")
	ScrapData(TOKEN,links)

	print("Step 5- finished")
	UserSolution = input("What is you propsed Solution: ")
	result = GeneratePlan(model,"info.json",UserSolution)
	print(result)
	print("Step 6- finished")
	
	
	



if __name__=="__main__":
	main()