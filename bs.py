from bs4 import BeautifulSoup
import requests
import time
import ConfigParser

# Url's List Input File
UrlInputFile = "/home/ngratnakumar/webscrape/g2crowd.txt"

# Configuration File
Config_File = '/home/ngratnakumar/webscrape/conf.d/extract-elements.conf'
config = ConfigParser.ConfigParser()
config.readfp(open(Config_File))

def extractVals(obj):
	iList=[]
	for i in obj: 
		iList.append(i.text)
	return iList

def extractLinkVals(obj):
	iList=[]
	for i in obj: 
		iList.append(i["href"])
	return iList

def loadExtractRulesConfiguration(soup):
	rulesSections=config.sections()
	rowData = []
	for ruleNo in rulesSections:
		rowData.append(parseRules(ruleNo,soup))
	print(rowData)

def parseRules(ruleNo,soup):
	requiredField	=	config.get(ruleNo,'requiredField')
	if requiredField:
		extractElementName		=	config.get(ruleNo,'extractElementName')
		elementName				=	config.get(ruleNo,'elementName')
		elementAttribute		= 	config.get(ruleNo,'elementAttribute')
		elementAttributeValue	=	config.get(ruleNo,'elementAttributeValue')
		elementAttributeType	=	config.get(ruleNo,'elementAttributeType')
		fieldList = buildSoupElement(soup,extractElementName,elementName,elementAttribute,elementAttributeValue,elementAttributeType)
	else:
		fieldList = "NA"
	return fieldList	
	
	
def buildSoupElement(soup,extractElementName,elementName,elementAttribute,elementAttributeValue,elementAttributeType):
	fieldObject = soup.find_all(elementName, attrs={elementAttribute : elementAttributeValue})
	if elementAttributeType == "link":
		fieldData	=	extractLinkVals(fieldObject)
	else:
		fieldData	=	extractVals(fieldObject)
	return str(fieldData)

def get_data(nurl,cnt):
	try:
		url = str(nurl).strip()
		r  = requests.get("http://" +url)
		data = r.text
		soup = BeautifulSoup(data)
		loadExtractRulesConfiguration(soup)
		'''# For g2crowd.com
		stars = soup.find_all('div', attrs={'class':'ellipsis'})
		starsval = soup.find_all('div', attrs={'class':'checkbox-line-height tiny-text'})
		productDesc = soup.find_all('p', attrs={'class':'product-show-description'})	
		user_role = soup.find_all('div', attrs={'class':'tiny-text ellipsis'})
		user_role_val = soup.find_all('div', attrs={'class':'checkbox-line-height'})
		extractVals(stars)
		extractVals(starsval)
		extractVals(productDesc)
		extractVals(user_role)
		extractVals(user_role_val)'''
	
		'''# For cambridgefindit.co.nz
		address = soup.find_all('span', attrs={'class':'frontend_address'})
		name = soup.find_all('span', attrs={'class':'trail-end'})
		website = soup.find_all('a', attrs={'id':'website'})
		entry_phone = soup.find_all('span', attrs={'class':'entry-phone'})
		entry_email = soup.find_all('span', attrs={'class':'entry-email'})
		phone_contact = soup.find_all('div', attrs={'class':'tevolution_custom_field'})
		print(str(cnt),extractVals(name),extractVals(address),extractLinkVals(website),extractVals(entry_phone),extractVals(entry_email),extractVals(phone_contact))
		'''
	except requests.exceptions.ConnectionError as e:
		print(str(cnt),"Internet Error : "+e)
	print("\n")	

def loadUrlInputFile():
	with open(UrlInputFile) as f:
		counter=1
		content = f.readlines()
		for weburl in content:	
			get_data(weburl,counter)
			counter=counter+1

def main():
	loadUrlInputFile()

main()

	
	
	


