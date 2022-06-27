from guietta import _, Gui, Quit, CB #gui
import codecs #kopiuje zawartość pliku
import shutil #dzięki tej bibliotece zmienimy system kodowania Unicode
import re #zaawansowane replace
import networkx as nx #grafy
import matplotlib.pyplot as plt #wykresy
import os

class main:
    global re

    opdict = {'tak': '1',
              'nie': '0'}
    
    gui = Gui(
            ["ścieżka do pliku:", "__a__","separator:", "__b__","1 linijka:", CB('op', opdict), ["CSV"]],
            [_,     _,   "",    _,   _,    _,          _],
            ["ścieżka do pliku:", "__c__",   _,   _,   _,   _,   ["XML"]],
            [_,     _,   "",    _,   _,    _,          _],
            ["ścieżka do pliku:","__d__",   _,    _,   _,   _,   ["XSD"]],
            [_,     _,   "",    _,   _,    _,          _],
            ["ścieżka do pliku:", "__e__", _, _,  _, _, ["Wizualizacja"]],
            [_,     _,    _,    _,   _,    _,       Quit]
    )

main=main()

class SQL_to_CSV:
    gui=main.gui
    with gui.CSV:

        separator=gui.b
               
        name, op=gui.get_selections('op')
        first_line = int(op)
        
        with codecs.open(gui.a, encoding="utf-16") as input_file:
            with codecs.open("script2.txt", "w", encoding="utf-8") as output_file:
                    shutil.copyfileobj(input_file, output_file)
        file=open("script2.txt", mode = 'r')
        read_data = file.read()
        
        table = read_data.split('CREATE TABLE') #liczy ilość tabel
        number_of_tables=len(table)-1

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'create table'
        searched_text='CREATE TABLE'
        list_of_tables = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    list_of_tables.append(line.rstrip()) #rstrip usuwa zbędne spacje

        list_of_tables1=[""] * len(list_of_tables)

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables[i]

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables1[i].replace("CREATE TABLE [","INSERT [")
            list_of_tables1[i]=list_of_tables1[i].replace("](","] (")

        for i in range(number_of_tables):
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","[")
            list_of_tables[i]=list_of_tables[i].replace("](","]")
            list_of_tables[i]=list_of_tables[i].replace("]","")
            list_of_tables[i]=list_of_tables[i].replace("[","")

        tab5=[[] for y in range(number_of_tables)] 

        tab6=[0] * number_of_tables

        file_name='script2.txt'
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                for i in range(number_of_tables):
                    if list_of_tables1[i] in line:
                        tab5[i].append(line.rstrip())

        for i in range(number_of_tables):
            tab6[i]=len(tab5[i])

        zm=re.escape(")")
        for i in range(number_of_tables):
            for j in range(tab6[i]):
                tab5[i][j]=re.sub(r'\s?\Decimal.*?\)', r'Decimal',tab5[i][j])
                tab5[i][j]=tab5[i][j].replace(" ASDecimal","")
                tab5[i][j]=re.sub('INSERT.*VALUES ','',tab5[i][j],flags=re.DOTALL)
                tab5[i][j]=tab5[i][j].replace(" AS DateTime","")
                tab5[i][j]=tab5[i][j].replace("CAST(N","")
                tab5[i][j]=tab5[i][j].replace("CAST(","")
                tab5[i][j]=tab5[i][j].replace("(","")
                tab5[i][j]=tab5[i][j].replace("(","")
                tab5[i][j]=tab5[i][j].replace(")","")
                tab5[i][j]=tab5[i][j].replace(" N'"," ")
                tab5[i][j]=tab5[i][j].replace("'","")
                tab5[i][j]=tab5[i][j].replace(" AS Date","")
                tab5[i][j]=tab5[i][j].replace("         ","")
                tab5[i][j]=tab5[i][j].replace(" as "," ")
                tab5[i][j]=tab5[i][j].replace("T00:00:00"," 00:00:00")
                tab5[i][j]=tab5[i][j].strip()

        for i in range(number_of_tables):
            for j in range(tab6[i]):
                tab5[i][j]=tab5[i][j].split(", ")

        tab9=[0] * number_of_tables
        for i in range(len(tab5)):
            tab9[i]=len(tab5[i][0])  

        tab4=[[] for y in range(number_of_tables)] 

        tab8=[0] * number_of_tables
        for i in range(number_of_tables):
            tab8[i]=len(tab4[i])

        for i in range(number_of_tables):
            if tab8[i]>tab9[i]:
                difference = tab8[i]-tab9[i]
                for j in range(len(tab5[i])):
                    for k in range(difference):
                        tab5[i][j].append("")

        for i in range(number_of_tables):
            file_object = open(list_of_tables[i] + '.csv', 'a')
            file_object.truncate(0)
        
        tab6.append(3)
        tab9.append(3)
        searched_text='CREATE TABLE'
        tab10 = []
        oo= 0
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if searched_text in line:
                    tab10.append(oo)

        tab11=[[] for y in range(number_of_tables)] 
        tab2 = []
        oo= 0
        o1=0
        o2=-1
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if o1==1 and line[0]=="	" and line[1]=="[":
                    tab2.append(oo)
                    tab11[o2].append(oo)
                else:
                    o1=0
                if oo in tab10:
                    o1=1
                    o2=o2+1

        tab4=[[] for y in range(number_of_tables)] 
        iii=0
        with open(file_name, 'r') as read_obj:        
            for line in read_obj:
                iii=iii+1
                for i in range(len(tab10)):
                    if iii in tab11[i]: 
                        tab4[i].append(line.rstrip())

        for i in range(len(tab10)):
            for j in range(len(tab4[i])):
                tab4[i][j]=tab4[i][j].replace("\t[","")
                tab4[i][j]=tab4[i][j].replace("))))","NULL")
                tab4[i][j]=tab4[i][j].replace(")))","NULL")
                tab4[i][j]=tab4[i][j].replace("))","NULL")
                tab4[i][j]=re.sub('].*NULL,','',tab4[i][j],flags=re.DOTALL)
        for i in range(number_of_tables):
            file_object = open(list_of_tables[i] + '.csv', 'a')
            file_object.truncate(0)
            if first_line==1:
                if i==number_of_tables:
                    break
                for l in range(tab9[i]):
                    if l==(tab9[i]-1):
                        file_object.write(tab4[i][l])
                    else:
                        file_object.write(tab4[i][l]+separator+' ')
                file_object.write("\n")
                for j in range(tab6[i]):
                    for k in range(tab9[i]):
                        if k==(tab9[i]-1):
                            file_object.write(tab5[i][j][k])
                        else:
                            file_object.write(tab5[i][j][k]+separator+' ')
                    file_object.write("\n")
            else:
                if i==number_of_tables:
                    break
                for j in range(tab6[i]):
                    for k in range(tab9[i]):
                        if k==(tab9[i]-1):
                            file_object.write(tab5[i][j][k])
                        else:
                            file_object.write(tab5[i][j][k]+separator+' ')
                    file_object.write("\n")

class SQL_to_XML:
    gui=main.gui     
    with gui.XML:
        with codecs.open(gui.c, encoding="utf-16") as input_file:
            with codecs.open("script2.txt", "w", encoding="utf-8") as output_file:
                shutil.copyfileobj(input_file, output_file)

        file=open("script2.txt", mode = 'r')
        read_data = file.read()

        table = read_data.split('CREATE TABLE') #liczy ilość tabel
        number_of_tables=len(table)-1

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'create table'
        searched_text='CREATE TABLE'
        list_of_tables = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    list_of_tables.append(line.rstrip()) #rstrip usuwa zbędne spacje

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'USE [', żeby znaleźć nazwe bazy
        searched_text='USE ['
        database_name1 = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    database_name1.append(line.rstrip()) #rstrip usuwa zbędne spacje

        if len(database_name1) == 1:
            nn=0
        elif len(database_name1) > 1:
            nn=1

        database_name=database_name1[nn]
        database_name=database_name.replace("USE [","<USE [")
        database_name=database_name.replace("]","]>")
        database_name=database_name.replace("USE [","")
        database_name=database_name.replace("]","")

        tab1 = [0,0]
        tab1[0]=database_name
        tab1[1]=database_name
        tab1[1]=tab1[1].replace("<","</")

        list_of_tables1=[""] * len(list_of_tables)

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables[i]

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables1[i].replace("CREATE TABLE [","INSERT [")
            list_of_tables1[i]=list_of_tables1[i].replace("](","] (")

        for i in range(number_of_tables):
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","<CREATE TABLE [")
            list_of_tables[i]=list_of_tables[i].replace("](","](>")
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","[")
            list_of_tables[i]=list_of_tables[i].replace("](","]")
            list_of_tables[i]=list_of_tables[i].replace("]","")
            list_of_tables[i]=list_of_tables[i].replace("[","")

        tab3=[]
        for i in range(number_of_tables):
            tab3.append(list_of_tables[i])
            tab3.append(list_of_tables[i])

        for i in range(number_of_tables*2):
            if i % 2 == 1:
                tab3[i]=tab3[i].replace("<","</")

        aa=0

        searched_text='CREATE TABLE'
        tab10 = []
        oo= 0
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if searched_text in line:
                    tab10.append(oo)

        tab11=[[] for y in range(number_of_tables)] 
        tab2 = []
        oo= 0
        o1=0
        o2=-1
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if o1==1 and line[0]=="	" and line[1]=="[":
                    tab2.append(oo)
                    tab11[o2].append(oo)
                else:
                    o1=0
                if oo in tab10:
                    o1=1
                    o2=o2+1

        tab4=[[] for y in range(number_of_tables)] 
        iii=0
        with open(file_name, 'r') as read_obj:        
            for line in read_obj:
                iii=iii+1
                for i in range(len(tab10)):
                    if iii in tab11[i]: 
                        tab4[i].append(line.rstrip())

        for i in range(len(tab10)):
            for j in range(len(tab4[i])):
                tab4[i][j]=tab4[i][j].replace("\t[","")
                tab4[i][j]=tab4[i][j].replace("))))","NULL")
                tab4[i][j]=tab4[i][j].replace(")))","NULL")
                tab4[i][j]=tab4[i][j].replace("))","NULL")
                tab4[i][j]=re.sub('].*NULL,','',tab4[i][j],flags=re.DOTALL)

        tab5=[[] for y in range(number_of_tables)] 

        file_name='script2.txt'
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                for i in range(number_of_tables):
                    if list_of_tables1[i] in line:
                        tab5[i].append(line.rstrip())

        tab6=[0] * number_of_tables

        for i in range(number_of_tables):
            tab6[i]=len(tab5[i])

        tab7=[[] for y in range(number_of_tables)] 

        y=-1
        while y<(number_of_tables-1):
            y=y+1
            x=0
            while x<tab6[y]:
                x=x+1
                tab7[y].append(x)
                tab7[y].append(x)

        aa=0
        for i in range(number_of_tables):
            for j in range(tab6[i]*2):
                if j % 2 == 0:
                    tab7[i][j]=str(tab7[i][j])
                    tab7[i][j]=tab7[i][j].replace(tab7[i][j],"<" + tab7[i][j] + ">")
                if j % 2 == 1:
                    tab7[i][j]=str(tab7[i][j])
                    tab7[i][j]=tab7[i][j].replace(tab7[i][j],"</" + tab7[i][j] + ">")

        tab8=[0] * number_of_tables
        for i in range(number_of_tables):
            tab8[i]=len(tab4[i])

        zm=re.escape(")")
        for i in range(number_of_tables):
            for j in range(tab6[i]):
                tab5[i][j]=re.sub(r'\s?\Decimal.*?\)', r'Decimal',tab5[i][j])
                tab5[i][j]=tab5[i][j].replace(" ASDecimal","")
                tab5[i][j]=re.sub('INSERT.*VALUES ','',tab5[i][j],flags=re.DOTALL)
                tab5[i][j]=tab5[i][j].replace(" AS DateTime","")
                tab5[i][j]=tab5[i][j].replace("CAST(N","")
                tab5[i][j]=tab5[i][j].replace("CAST(","")
                tab5[i][j]=tab5[i][j].replace("(","")
                tab5[i][j]=tab5[i][j].replace("(","")
                tab5[i][j]=tab5[i][j].replace(")","")
                tab5[i][j]=tab5[i][j].replace(" N'"," ")
                tab5[i][j]=tab5[i][j].replace("'","")
                tab5[i][j]=tab5[i][j].replace(" AS Date","")
                tab5[i][j]=tab5[i][j].replace("         ","")
                tab5[i][j]=tab5[i][j].replace(" as "," ")
                tab5[i][j]=tab5[i][j].replace("T00:00:00"," 00:00:00")
                tab5[i][j]=tab5[i][j].strip()

        for i in range(number_of_tables):
            for j in range(tab6[i]):
                tab5[i][j]=tab5[i][j].split(", ")

        tab9=[0] * number_of_tables

        for i in range(len(tab5)):
            tab9[i]=len(tab5[i][0])

        for i in range(number_of_tables):
            if tab8[i]>tab9[i]:
                difference = tab8[i]-tab9[i]
                for j in range(len(tab5[i])):
                    for k in range(difference):
                        tab5[i][j].append("")

        file_object = open('SQL_to_XML.xml', 'a')
        file_object.truncate(0)

        aa=0
        file_object.write(tab1[0])
        file_object.write("\n")
        for i in range(len(tab3)):
            file_object.write("    ")
            file_object.write(tab3[i])
            file_object.write("\n")
            if i % 2 == 0:
                for j in range(tab6[aa]*2):
                    file_object.write("        ")
                    file_object.write(tab7[aa][j])
                    file_object.write("\n")
            
                    if j % 2 == 0:
                        for i in range(tab8[aa]):
                            file_object.write("            <"+ tab4[aa][i]+">"+       tab5[aa][int(j/2)][i]       +"</"+ tab4[aa][i]+">")
                            file_object.write("\n")
                aa=aa+1 
        file_object.write(tab1[1])
        file_object.close()

class SQL_to_XSD:
    gui=main.gui
    with gui.XSD:
        with codecs.open(gui.d, encoding="utf-16") as input_file:
            with codecs.open("script2.txt", "w", encoding="utf-8") as output_file:
                shutil.copyfileobj(input_file, output_file)
        file=open("script2.txt", mode = 'r')
        read_data = file.read()

        table = read_data.split('CREATE TABLE') #liczy ilość tabel
        number_of_tables=len(table)-1

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'create table'
        searched_text='CREATE TABLE'
        list_of_tables = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    list_of_tables.append(line.rstrip()) #rstrip usuwa zbędne spacje

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'USE [', żeby znaleźć nazwe bazy
        searched_text='USE ['
        database_name1 = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    database_name1.append(line.rstrip()) #rstrip usuwa zbędne spacje

        if len(database_name1) == 1:
            nn=0
        elif len(database_name1) > 1:
            nn=1

        database_name=database_name1[nn]
        database_name=database_name.replace('USE [','<xsd:element name="USE [')
        database_name=database_name.replace(']',']">')
        database_name=database_name.replace("USE [","")
        database_name=database_name.replace("]","")

        tab1 = [0,0]
        tab1[0]=database_name
        tab1[1]="</xsd:element>"

        list_of_tables1=[""] * len(list_of_tables)

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables[i]

        for i in range(number_of_tables):
            list_of_tables1[i]=list_of_tables1[i].replace("CREATE TABLE [","INSERT [")
            list_of_tables1[i]=list_of_tables1[i].replace("](","] (")

        for i in range(number_of_tables):
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","<CREATE TABLE [")
            list_of_tables[i]=list_of_tables[i].replace("](","](>")
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","[")
            list_of_tables[i]=list_of_tables[i].replace("](","]")
            list_of_tables[i]=list_of_tables[i].replace("]","")
            list_of_tables[i]=list_of_tables[i].replace("[","")

        tab3=[]
        for i in range(number_of_tables):
            tab3.append(list_of_tables[i])
            tab3.append("<xsd:complexType>")

        for i in range(number_of_tables*2):
            if i % 2 == 0:
                tab3[i]=tab3[i].replace('<','<xsd:complexType name="')
                tab3[i]=tab3[i].replace('>','">')
            if i % 2 == 1:
                tab3[i]=tab3[i].replace("<","</")

        searched_text='CREATE TABLE'
        tab10 = []
        oo= 0
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if searched_text in line:
                    tab10.append(oo)

        tab11=[[] for y in range(number_of_tables)] 
        tab2 = []
        oo= 0
        o1=0
        o2=-1
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                oo=oo+1
                if o1==1 and line[0]=="	" and line[1]=="[":
                    tab2.append(oo)
                    tab11[o2].append(oo)
                else:
                    o1=0
                if oo in tab10:
                    o1=1
                    o2=o2+1

        tab4=[[] for y in range(number_of_tables)] 
        iii=0
        with open(file_name, 'r') as read_obj:        
            for line in read_obj:
                iii=iii+1
                for i in range(len(tab10)):
                    if iii in tab11[i]: 
                        tab4[i].append(line.rstrip())

        for i in range(len(tab10)):
            for j in range(len(tab4[i])):
                tab4[i][j]=tab4[i][j].replace("\t[","")
                tab4[i][j]=tab4[i][j].replace("))))","NULL")
                tab4[i][j]=tab4[i][j].replace(")))","NULL")
                tab4[i][j]=tab4[i][j].replace("))","NULL")
                tab4[i][j]=re.sub('].*NULL,','',tab4[i][j],flags=re.DOTALL)

        tab8=[0] * number_of_tables
        for i in range(number_of_tables):
            tab8[i]=len(tab4[i])
        bb=-1

        tab9=[[] for y in range(number_of_tables)] 
        iii=0
        with open(file_name, 'r') as read_obj:        
            for line in read_obj:
                iii=iii+1
                for i in range(len(tab10)):
                    if iii in tab11[i]: 
                        tab9[i].append(line.rstrip())

        set_of_data_types=["string","dateTime","decimal","int","long","short","boolean","time","date","float","double"]
        for i in range(len(tab10)):
            for j in range(len(tab9[i])):        
                tab9[i][j]=tab9[i][j].replace("\t[","aaaa\t[")
                tab9[i][j]=re.sub(r'(?<=aaaa).+?(?= )', '', tab9[i][j], count=1)
                tab9[i][j]=tab9[i][j].replace("aaaa [","")
                if tab9[i][j][0]=="a" and tab9[i][j][1]=="a" and tab9[i][j][2]=="a" and tab9[i][j][3]=="a":
                    tab9[i][j]="string"
                tab9[i][j]=re.sub('].*NULL,','', tab9[i][j],flags=re.DOTALL)
                tab9[i][j]=tab9[i][j].replace("varchar","string")
                tab9[i][j]=tab9[i][j].replace("char","string")
                tab9[i][j]=tab9[i][j].replace("datetime","dateTime")
                tab9[i][j]=tab9[i][j].replace("smalldatetime","dateTime")
                tab9[i][j]=tab9[i][j].replace("timestamp","dateTime")
                tab9[i][j]=tab9[i][j].replace("varbinary","int")
                tab9[i][j]=tab9[i][j].replace("money","decimal")
                tab9[i][j]=tab9[i][j].replace("smallmoney","int")
                tab9[i][j]=tab9[i][j].replace("bigint","long")
                tab9[i][j]=tab9[i][j].replace("smallint","short")
                tab9[i][j]=tab9[i][j].replace("bit","boolean")
                if tab9[i][j] not in set_of_data_types:
                    tab9[i][j]="string"

        file_object = open('SQL_to_XSD.xsd', 'a')
        file_object.truncate(0)
        bb=-1
        file_object.write(tab1[0])
        file_object.write("\n")
        for i in range(len(tab3)):    
            file_object.write("    ")
            file_object.write(tab3[i])
            file_object.write("\n")        
            if i % 2 == 0:
                bb=bb+1
                for j in range(tab8[bb]):
                    file_object.write('        <xsd:element name="')
                    file_object.write(tab4[bb][j])
                    file_object.write('" type="xs:'+tab9[bb][j]+'"/>')
                    file_object.write("\n")
        file_object.write(tab1[1])
        file_object.close()

class visualisation:
    gui=main.gui
    with gui.Wizualizacja:       
        with codecs.open(gui.e, encoding="utf-16") as input_file:
            with codecs.open("script2.txt", "w", encoding="utf-8") as output_file:
                shutil.copyfileobj(input_file, output_file)

        file=open("script2.txt", mode = 'r')
        read_data = file.read()
        table = read_data.split('CREATE TABLE') #liczy ilość tabel
        number_of_tables=len(table)-1
        file_name='script2.txt' #wyświetla linijki zawierające fraze 'create table'
        searched_text='CREATE TABLE'
        list_of_tables = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    list_of_tables.append(line.rstrip()) #rstrip usuwa zbędne spacje
        for i in range(number_of_tables):
            list_of_tables[i]=list_of_tables[i].replace("CREATE TABLE [","[")
            list_of_tables[i]=list_of_tables[i].replace("](","]")
            list_of_tables[i]=list_of_tables[i].replace("]","")
            list_of_tables[i]=list_of_tables[i].replace("[","")
            for j in range (len(list_of_tables[i])):
                if list_of_tables[i][0] ==".":
                    list_of_tables[i] = list_of_tables[i][1:]
                    break
                else:
                    list_of_tables[i] = list_of_tables[i][1:]

        file_name='script2.txt' #wyświetla linijki zawierające fraze 'create table'
        searched_text='FOREIGN KEY'
        keys = []
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                if searched_text in line: #jeśli szukana fraza jest danej linijce to zostaje dodana do listy
                    keys.append(line.rstrip()) #rstrip usuwa zbędne spacje
        for i in range(len(keys)):
            keys[i]=re.sub('ALTER.*FOREIGN KEY','',keys[i],flags=re.DOTALL)
            keys[i]=keys[i].replace("([","")
            keys[i]=keys[i].replace("])","")

        searched_text='CREATE TABLE'
        tab10 = []
        ooo= 0
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                ooo=ooo+1
                if searched_text in line:
                    tab10.append(ooo)

        tab11=[[] for y in range(number_of_tables)] 
        tab2 = []
        ooo= 0
        o1=0
        o2=-1
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                ooo=ooo+1
                if o1==1 and line[0]=="	" and line[1]=="[":
                    tab2.append(ooo)
                    tab11[o2].append(ooo)
                else:
                    o1=0
                if ooo in tab10:
                    o1=1
                    o2=o2+1

        tab4=[[] for y in range(number_of_tables)] 
        iii=0
        with open(file_name, 'r') as read_obj:        
            for line in read_obj:
                iii=iii+1
                for i in range(len(tab10)):
                    if iii in tab11[i]: 
                        tab4[i].append(line.rstrip())

        for i in range(len(tab10)):
            for j in range(len(tab4[i])):
                tab4[i][j]=tab4[i][j].replace("\t[","")
                tab4[i][j]=tab4[i][j].replace("))))","NULL")
                tab4[i][j]=tab4[i][j].replace(")))","NULL")
                tab4[i][j]=tab4[i][j].replace("))","NULL")
                tab4[i][j]=re.sub('].*NULL,','',tab4[i][j],flags=re.DOTALL)

        b=[]
        a=[]
        for i in range(len(list_of_tables)):
            for j in range(len(keys)):
                if keys[j] in tab4[i]:
                    b.append(j)
                    a.append(i)

        tab=[]
        c=[]
        d=[]
        for j in range(len(list_of_tables)):
            for i in range(len(b)):
                if b[i]==j:
                    tab.append(a[i])
            for k in range(len(tab)):
                for l in range(len(tab)):
                    if tab[l]!=tab[k]:
                        x=tab[l]
                        y=tab[k]
                        c.append(list_of_tables[x])
                        d.append(list_of_tables[y])
            tab=[]
        x=0
        for i in range(len(list_of_tables)):
            if list_of_tables[i] not in c:
                if list_of_tables[i] not in d:
                    list_of_tables[i]=""
                    x=x+1

        for i in range(x):
            list_of_tables.remove('')

        for i in range(len(c)):
            for j in range(len(c)):
                if c[i]==d[j]:
                    if c[j]==d[i]:
                        c[j]=""
                        d[j]=""

        for i in range(int(len(c)/2)):
            c.remove('')
            d.remove('')

        G=nx.Graph()
        for i in range(len(list_of_tables)):
            G.add_node(list_of_tables[i])
        for i in range(len(c)):
            G.add_edge(c[i],d[i])
        plt.figure(figsize=(9,7))

        nx.draw(G, node_size=1000, with_labels = True, font_size=10, node_shape="s")

        plt.axis('off')
        axis = plt.gca()
        axis.set_xlim([1.2*x for x in axis.get_xlim()])
        axis.set_ylim([1.2*y for y in axis.get_ylim()])
        
        databasename=gui.e
        databasename=databasename.replace(".sql","")
        plt.savefig(databasename +'.png')

    gui.run()


main
