from django.shortcuts import render, redirect
from .forms import AddUrlForm
import requests
from bs4 import BeautifulSoup
import socket
from ipwhois import IPWhois 
from pprint import pprint


def index(request ):
	form = AddUrlForm()
	if "errors" in request.session:
		errors = request.session["errors"]
	else:
		errors= None		
	context = { 
		"urlForm": form,
		"errors": errors

	 }

	return render(request, "testurl/index.html", context)

def create(request):
	if request.method == "POST":
		if request.POST['Add_URL'][:4] == 'http':
			print request.POST['Add_URL'], "BEFORE PICKIN UP PAGE"
			page = requests.get(request.POST['Add_URL'])
			print page.status_code
			soup = BeautifulSoup(page.content, 'html.parser')
			list(soup.children)
			results={}

			if request.POST['Add_URL'][:5] == 'https':
				host = request.POST['Add_URL'][8:]
			elif request.POST['Add_URL'][:5] == 'http:':
				host = request.POST['Add_URL'][7:]
			host = host.split('/')
			host = host[0]
			cdn = find_cdn(host)
			results[host] = cdn

			atributes = ['img', 'script', 'input', 'video', 'source', 'embed', 'iframe', 'track', 'frame']

			for atribute in atributes:

				targets =  soup.findAll(atribute)
				for target in targets :
					if target.get('src') != None:
						if target['src'][:5]== 'https':
							host = target['src'][8:]
							host = host.split('/')
							host = host[0]
							print host, "this is a  host 1",target
						elif target['src'][:5]== 'http:':
							host = target['src'][7:]
							host = host.split('/')
							host = host[0]
							print host, "this is a  host 1", target
						elif target['src'][:2] == "//":
							host = target['src'][2:]
							host = host.split('/')
							host = host[0]
							print host, "this is a host 1", target
						if results.get(host) == None:
							cdn = find_cdn(host)
							results[host] = cdn

	

 			print results
 			#could if need saved db instead!
 			if "errors" in request.session:
 				del request.session["errors"]
 			request.session['results'] = results
			return redirect("/result")
		else:
			request.session["errors"] = 'This not a valid URL. The URL need to start with http:// or https://'
			return redirect("/")	
	else:
		request.session["errors"] = "stop abusing my form."
		return redirect("/")

def show(request):
	data = request.session['results']
	results = []
	for key,val in data.iteritems():
		result = key + " = "+  val
		results.append(result)
		context= {'results': results}
	return render(request, 'testurl/result.html', context)


def find_cdn(host):
	obj = IPWhois(socket.gethostbyname(host))
	results = obj.lookup_rdap(depth=1)
	return results['network']['name']


