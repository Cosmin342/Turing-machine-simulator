#Radu Cosmin 323 CB
#@cosminr47 - utilizator pe hackerrank

#Functie ce intoarce numarul taskului de executat
def cons(string):
	if string == 'step':
		return 1
	if string == 'accept':
		return 2
	if string == 'k_accept':
		return 3

#Functie ce intoarce o masina Turing pornind de la un string
def readTM(codificare):
	#Inintializarea componentelor
	stari_fin = []
	stare_ini = 0
	alfabet = []
	tranz = []
	num = 0
	d = {}
	i = 0
	#Codificarea fiind pe mai multe randuri, se prelucreaza linie cu linie
	for p in codificare.split('\n'):
		#Prima oara se citreste numarul de stari
		if i == 0:
			num = int(p)
		#Apoi starile finale, daca exista
		if i == 1:
			if p == '-':
				i += 1
				continue
			for n in p.split(' '):
				stari_fin.append(int(n))
		#Pentru fiecare tranzitie am creat o lista ce retine cele 5
		#caractere ale sale
		if i >= 2:
			impar = 0
			tranzitie = []
			for n in p.split(' '):
				#In paralel cu crearea tranzitiei, adaug si literele pentru
				#alfabet intr-un dictionar
				if impar % 2 == 1:
					if not n in d:
						d[n] = n
				tranzitie.append(n)
				impar += 1
			#Adaug tranzitia creata intr-o lista
			tranz.append(tranzitie)
		i += 1
	tranz.remove(tranz[len(tranz) - 1])
	#Extrag fiecare litera existenta in dictionar pentru a crea alfabetul
	for lit in d:
		alfabet.append(lit)
	alfabet.append('#')
	stari = []
	for l in range(0, num):
		stari.append(l)
	#La final creez un tuplu si il returnez
	masina = (stari, alfabet, tranz, stare_ini, stari_fin)
	return masina

#Functie care executa un pas al masinii pe o configuratie
def step(tuplu, date):
	output = ''
	for i in date.split(' '):
		ind = 0
		for l in i.split(','):
			#Prima oara se extrage partea stanga a configuratiei
			if ind == 0:
				stanga = l
			#Apoi starea curenta
			if ind == 1:
				stare_curenta = int(l)
			#Iar in final se ia si partea dreapta a benzii
			if ind == 2:
				dreapta = l
			ind += 1
		#Variabila utilizata pentru oprirea for-ului ce urmeaza
		gasit = 0
		for st in tuplu[2]:
			#Daca este gasita o tranzitie pentru starea si caracterul curent
			#se prelucreaza configuratia
			if st[0] == str(stare_curenta) and st[1] == dreapta[0]:
				gasit = 1
				if st[4] == 'R':
					#Daca se indica mutarea cursorului spre dreapta, se va
					#pune in partea stanga noul caracter
					stanga = stanga + st[3]
					#Se elimina caracterul cel mai din stanga
					dreapta = dreapta[1:]
					#Daca este atins maximul benzii in dreapta, se va adauga
					#un # la configuratie
					if len(dreapta) == 1:
						dreapta = '#' + dreapta
					#Este schimbata starea curenta
					stare_curenta = int(st[2])
					#Se realizeaza noua configuratie
					config = stanga + ',' + str(stare_curenta) + ','
					config = config + dreapta + ' '
					break
				if st[4] == 'H':
					#Daca se indica ramanerea pe aceeasi pozitie, se schimba
					#starea curenta si caracterul actual, iar cursorul ramane
					#la aceeasi pozitie
					stare_curenta = int(st[2])
					dreapta = st[3] + dreapta[1:]
					config = stanga + ',' + str(stare_curenta) + ','
					config = config + dreapta + ' '
					break				
				if st[4] == 'L':
					#Pentru mutarea la stanga, totul se realizeaza ca la
					#mutarea la dreapta, cu schimbarile de rigoare
					dreapta = stanga[len(stanga) - 1] + st[3] + dreapta[1:]
					stanga = stanga[:len(stanga) - 1]
					if (len(stanga) == 1):
						stanga = stanga + '#'
					stare_curenta = int(st[2])
					config = stanga + ',' + str(stare_curenta) + ','
					config = config + dreapta + ' '
					break
		#Daca nu s-a gasit tranzitia pentru o anumita configuratie, se pune
		#in output False
		if gasit == 0:
			output = output + 'False '
		#Altfel se pune noua configuratie
		if gasit == 1:
			output = output + config
	#Se elimina spatiul suplimentar de la finalul outputului
	output = output[:len(output) - 1]
	return output

#Functie care verifica daca o masina Turing accepta un set de cuvinte
def accept(tuplu, date):
	output = ''
	for i in date.split(' '):
		cuvant = i
		ind = 0
		stare = tuplu[3]
		while 1:
			gasit = 0
			fin = 0
			#Se cauta o tranzitie pentru caracterul si starea curenta
			for st in tuplu[2]:
				if st[1] == cuvant[ind] and stare == int(st[0]):
					gasit = 1
					#Se schimba caracterul curent cu noul caracter dat de
					#tranzitie
					cuvant = cuvant[:ind] + st[3] + cuvant[ind + 1:]
					stare = int(st[2])
					#Daca se indica ramanerea la caracterul curent, se
					#verifica daca s-a ajuns intr-o stare finala sau nu
					if st[4] == 'H':
						#fin se seteaza la 1 pentru a evita anumite
						#instructiuni
						if stare in tuplu[4]:
							output = output + 'True '
							fin = 1
							break
						else:
							output = output + 'False '
							fin = 1
							break
					#Daca se indica mutarea la dreapta, se incrementeaza
					#indicele
					if st[4] == 'R':
						#Daca se ajunge la finalul cuvantului, se adauga #
						#pentru a continua verificarea
						if ind == len(cuvant) - 1:
							cuvant = cuvant + '#'
							ind = len(cuvant) - 2
						ind += 1
					#Daca se indica mutarea la stanga, se decrementeaza indicele
					if st[4] == 'L':
						if ind == 0:
							#Daca se ajunge la finalul cuvantului, se adauga #
							#pentru a continua verificarea
							cuvant = '#' + cuvant
							ind = 1
						ind -= 1
					#Se verifica daca noua stare este finala
					if stare in tuplu[4]:
						output = output + 'True '
						fin = 1
					break
			if fin == 1:
				break
			#Daca nu se gaseste o noua tranzitie si starea curenta nu este
			#finala, cuvantul este respins
			if gasit == 0:
				output = output + 'False '	
				break
	output = output[:len(output) - 1]
	return output

#Functie care verifica daca o masina Turing accepta un set de cuvinte in cel
#mult k pasi
def k_accept(tuplu, date):
	output = ''
	for i in date.split(' '):
		count = 0
		k = 0
		#Se extrag cuvantul si numarul k din fiecare pereche
		for l in i.split(','):
			if count == 0:
				cuvant = l
			else:
				k = int(l)
			count += 1
		#Se porneste de la pozitia 0
		ind = 0
		stare = tuplu[3]
		#Variabila pentru a controla daca un cuvant a fost decis deja sau nu
		printat = 0
		for s in range(0, k):
			gasit = 0
			fin = 0
			for st in tuplu[2]:
				if st[1] == cuvant[ind] and stare == int(st[0]):
					gasit = 1
					cuvant = cuvant[:ind] + st[3] + cuvant[ind + 1:]
					stare = int(st[2])
					#Daca se indica ramanerea pe pozitia curenta, se verifica
					#daca s-a ajuns intr-o stare finala
					if st[4] == 'H':
						if stare in tuplu[4]:
							output = output + 'True '
							fin = 1
							break
					#In cazul in care se indica mutarea la stanga/dreapta, se
					#incrementeaza/decrementeaza indicele
					if st[4] == 'R':
						if ind == len(cuvant) - 1:
							cuvant = cuvant + '#'
							ind = len(cuvant) - 2
						ind += 1
					if st[4] == 'L':
						if ind == 0:
							cuvant = '#' + cuvant
							ind = 1
						ind -= 1
					#Se verifica daca noua stare este finala
					if stare in tuplu[4]:
						output = output + 'True '
						fin = 1
					break
			if fin == 1:
				break
			#Daca nu se mai gasesc tranzitii, cuvantul este respins
			if gasit == 0:
				printat = 1
				output = output + 'False '	
				break
		#Daca in k pasi nu s-a ajuns la o stare finala, cuvantul este respins
		if not stare in tuplu[4] and printat == 0:
			output = output + 'False '
	output = output[:len(output) - 1]
	return output

#Variabila utilizata pentru a sti ce se extrage de la input
var = 0
codif_masina = '';
import sys
while True:
	#Se verifica daca se ajunge la finalul fisierului sau daca s-a intalnit
	#la citirea de la tastatura combinatia CTRL+D
	try:
		line = input()
	except EOFError:
		break
	#Pe prima linie se afla numele taskului
	if var == 0:
		task = line
	#Pe a doua se gaseste inputul taskului
	if var == 1:
		input_task = line
	#Iar de la a treia pana la final, se gaseste codificarea masinii
	if var >= 2:
		codif_masina = codif_masina + line + '\n'
	var += 1
#Se formeaza masina
tup = readTM(codif_masina)
#Se cauta numarul taskului
nr_task = cons(task)
#In functie de numarul taskului, se apeleaza o functie definita mai sus si se
#afiseaza rezultatul
if nr_task == 1:
	print(step(tup, input_task))
if nr_task == 2:
	print(accept(tup, input_task))
if nr_task == 3:
	print(k_accept(tup, input_task))