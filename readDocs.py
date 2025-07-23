from pypdf import PdfReader 
from dotenv import load_dotenv
import os
import google.generativeai as genai
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
import gradio as gr
load_dotenv()

class MindGather:
	def __init__(self):
		KEY = os.getenv("api")
		genai.configure(api_key=KEY)
		self.model = genai.GenerativeModel('gemini-1.5-pro')
		

	def saveSummary(self,dictInfo,filename):
		with open(filename, "w") as outfile: 
			json.dump(dictInfo, outfile,indent=4)

	def GenerateQuerry(self,dictInfo):
		prompt = f"Generate a search query for this information , the querry should be spesfic and try to cover the Tecnecalities and implimentations methods.\
		Note provide only the query nothing more\
			{dictInfo} "
		responce = self.model.generate_content(prompt)
		return responce.text

	def SearchTheWeb(self,URL,query,SEARCHKEY,CX):
		params = {"key":SEARCHKEY,"cx":CX,"q":query}
		responce = requests.get(URL,params=params)
		return json.loads(responce.text)

	def process(self,text):
		keys = ["problem","requirments","Tec"]
		parts = text.split("--")
		text_dict = dict(zip(keys,list(map(lambda x:x.split(":")[1],parts))))
		return text_dict 

	def extract(self,text):
		prompt = f"extract the problem that we are working on,requirments from this text and the Tec that i need to use your responce should be like this \
			Problem:\
				--requirments:\
					--Tec:\
						Note each requirment need to be seprated with / and don't add any additional points '{text}' "
		responce = self.model.generate_content(prompt)
		responce_dict = self.process(responce.text)
		return responce_dict

	def ReadDoc(self,file_name):
		reader = PdfReader(file_name)
		file = ""

		for page in reader.pages:
			text = page.extract_text()
			file+="\n"+text
		return file

	def GetItem(self,items):
		links = []
		for item in items:
			links.append(item["link"])
		return links


	def ScrapData(self,TOKEN,links):
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
				with open("info.txt","a",encoding='utf-8') as f: 
					f.write(text)
				time.sleep(1)




	def GeneratePlan(self,UserSol):
		file_name="info.txt"
		sample_file = genai.upload_file(path=file_name,
							display_name="Informations")
		
		prompt = f"using the document and Based on the proposed solution, generate a detailed and technical plan for implementation. The plan should include:\
			Specific technologies or methodologies to be used.\
			A phased approach with clear milestones and deliverables.\
			A breakdown of the tasks involved in each phase.\
			Consideration of any technical constraints or requirements mentioned in the cahier de charge.\
			How the findings from the research phase can be incorporated into the plan.\
			Identification of any uncertainties or unknowns in the proposal, along with suggestions for addressing them.\
			Contingency plans to mitigate potential risks or challenges.\
			proposed Solution :  {UserSol} "
		responce = self.model.generate_content([sample_file,prompt])
		return responce.text

	def Ui(self):

		iface =  gr.Interface(fn=self.GeneratePlan,
							inputs= gr.components.Textbox(lines=7, label="Enter your text"),
							outputs=gr.components.Text(),
							title="MindForge")
		iface.launch()
		

	def main(self):
		
		KEY = os.getenv("api")
		SEARCHKEY = os.getenv("search_key")
		TOKEN = os.getenv("token")
		CX = os.getenv("cx")
		URL = f"https://www.googleapis.com/customsearch/v1"
		Save=False
		file_name = "req.pdf"
		
		
		text = self.ReadDoc(file_name)
		print("Step 1- finished")
		responce = self.extract(text)
		if Save==True:
			self.saveSummary(responce,"summary.json")
		query = self.GenerateQuerry(responce["problem"])
		print("Step 2- finished")
		with open("queries.txt","a") as f:
			f.write(query)
		SearchData = self.SearchTheWeb(URL,query,SEARCHKEY,CX) 
		print("Step 3- finished")
		self.saveSummary(SearchData,"searchData.json")
		if "items" in SearchData.keys():
			items = SearchData["items"]
			links = self.GetItem(items)
			print("Step 4- finished")
			self.ScrapData(TOKEN,links[:2])

			print("Step 5- finished")
			self.Ui()
			print("Step 6- finished")



if __name__=="__main__":
	MindGather().main()
