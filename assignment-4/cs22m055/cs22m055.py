
import os

#Importing the rdflib requirements
from rdflib import Graph,Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
from rdflib.namespace import  RDF, RDFS
cwd=os.getcwd()




#importing the library to read the xml data
import xml.etree.ElementTree as ET

#Create a tree to get the XML data
tree = ET.parse('Shopping_Mall.xml')

root=tree.getroot()

res_name = []
opening_timing= []
closing_timing= []
floor_no = []
cuisine = []

count = 0
#for element in root.findall()
for child in root:
    #print("outside",child, type(child))
    if(child.tag == 'building'):
        #print("inside",child, type(child))
        for child1 in child:

            if(child1.tag == 'floor' and 1 > count):
                count+=1
                for child2 in child1 :

                    if(child2.tag=='resturant'):#resturant

                        for element in child1.findall(child2.tag+'/res_name') :
                            res_name.append(element.text.strip())
                        for element in child1.findall(child2.tag+'/floor_no'):
                            floor_no.append(element.text.strip())
                        for child3 in child2:
                            if child3.tag == 'timings':
                                for element in child2.findall(child3.tag+'/opening'):
                                    opening_timing.append(element.text.strip())
                                for element in child2.findall(child3.tag+'/closing'):
                                    closing_timing.append(element.text.strip())
                            if child3.tag == 'cuisine':
                                for element in child2.findall(child3.tag+'/name'):
                                    cuisine.append(element.text.strip())


print(res_name)
print(floor_no)
print(opening_timing)
print(closing_timing)
print(cuisine)

g=Graph()
g.parse("Assignment4rdf.rdf", format='xml')

print("OWL File Loaded")


myNamespace="http://www.semanticweb.org/home/ontologies/2023/3/Shopping_Mall" #Namespace
namedIndividual = URIRef('http://www.w3.org/2002/07/owl#NamedIndividual') #namedIndividual
#rdftype = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
def isAlreadyDefined(subs):
    for s in g.subjects():
        if(subs in str(s)):
            return True
    return False

all_triplets=[]

index_no=[0]
newRDFTriples = []


#creating the role triplets for the customer - places - order
for index in range(len(res_name)):
    individualName=str(myNamespace)+"#"+res_name[index]
    arc_class=str(myNamespace)+"#"+"res_name"
    arc_individual = URIRef(individualName)

    if(isAlreadyDefined(individualName)==False):
        all_triplets.append((arc_individual,RDF.type, URIRef(arc_class)))
        newRDFTriples.append((arc_individual,RDF.type, URIRef(namedIndividual)))

        #Adding Data Properties - id,name,contact of the customer.
        subject=arc_individual
        pred= URIRef(str(myNamespace)+"#FloorNo")
        literal=floor_no[index]
        newRDFTriples.append((subject,pred, Literal(literal,datatype=XSD.string)))

        pred= URIRef(str(myNamespace)+"#food_served")
        if(index <= len(cuisine)):
            literal=cuisine[index]
            newRDFTriples.append((subject,RDFS.label, Literal(literal,datatype=XSD.string)))

        pred= URIRef(str(myNamespace)+"#hasOpen")
        if(index < len(opening_timing)):
            literal=opening_timing[index]
            newRDFTriples.append((subject,pred, Literal(literal,datatype=XSD.string)))

        pred= URIRef(str(myNamespace)+"#hasClose")
        if(index < len(closing_timing)):
            literal=closing_timing[index]
            newRDFTriples.append((subject,pred, Literal(literal,datatype=XSD.string)))




for i in all_triplets:
    print("*",i,'\n')

print("----------------------------------------------")
for i in newRDFTriples:
    print(i)
    print('\n')

print("Total New RDF Triples are ", len(newRDFTriples))

g.serialize(destination="Assignment4rdf_final.rdf", format='xml')
#
#Checking consitency and inferences

from owlready2 import *
onto = get_ontology(cwd+"/Assignment4rdf.rdf").load()

#Checking consistency approach 1
with onto:
    sync_reasoner()
onto.save("Assignment4rdf_consistent.rdf")
import rdflib
graph2=rdflib.Graph()
graph2.parse("Assignment4rdf_final.rdf", format='xml')

no_of_tuple = 0
for s,p,o in g2:
    no_of_tuple=no_of_tuple+1

print("No of Triples Before :  ", no_of_tuple)

graph3=rdflib.Graph()
graph3.parse("Assignment4rdf_consistent.rdf", format='xml')

count = 0
for s,p,o in g3:
    no_of_tuple=no_of_tuple+1

print("No of Triples After :  ", no_of_tuple)

from rdflib.compare import  graph_diff, to_isomorphic
iso1 = to_isomorphic(graph2)
iso2 = to_isomorphic(graph3)

if(iso1 != iso2):
    i=0
    both, first, second = graph_diff(iso1,iso2)
    print(" New Inderences and All Inferences Generated....")
    def dump_nt_sorted(g,f):
        for l in sorted(g.serialize(format='nt').splitlines()):
            if(l) :
                f.write(l)
                f.write("\n")
    
    fo = open("Allinferred.txt", "w")

    dump_nt_sorted(second, fo)
    dump_nt_sorted(both, fo)

    fo.close()

    fo = open("DATAinferred.txt", "w")
    dump_nt_sorted(second, fo)
    fo.close()
else:
    print("No Inferences")
