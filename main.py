from turtle import *

def labyFromFile(fn):
	f = open(fn)
	laby = []
	indline = 0
	for fileline in f:
		labyline = []
		inditem = 0
		for item in fileline:
			# empty cell / case vide
			if item == ".":
				labyline.append(0)
			# wall / mur
			elif item == "#":
				labyline.append(1)
			# entrance / entree
			elif item == "x":
				labyline.append(0)
				mazeIn = [indline,inditem]
			# exit / sortie
			elif item == "X":
				labyline.append(0)
				mazeOut = [indline,inditem]
			# discard "\n" char at the end of each line
			inditem += 1
		laby.append(labyline)
		indline += 1
	f.close()
	return laby, mazeIn, mazeOut

def afficheTextuel(dicoJeu):
	print("\nLabyrinthe Textuel :")
	for ligne in range(len(dicoJeu["ly"])):
		for e in range(len(dicoJeu["ly"][ligne])):
			if ligne == dicoJeu["In"][0] and e == dicoJeu["In"][1]:
				print("x", end="")
			elif ligne == dicoJeu["Out"][0] and e == dicoJeu["Out"][1]:
				print("o", end="")
			elif dicoJeu["ly"][ligne][e] == 1:
				print("#", end="")
			elif dicoJeu["ly"][ligne][e] == 0:
				print(" ", end="")
		print("")

def afficheGraphique(dicoJeu):
	t = dicoJeu["tcell"]
	bgcolor("black")
	speed(1000)
	screensize((len(dicoJeu["ly"])*t), (len(dicoJeu["ly"][0])*t))
	hideturtle()
	for ligne in range(len(dicoJeu["ly"])):
		for e in range(len(dicoJeu["ly"][ligne])):
			if ligne == dicoJeu["In"][0] and e == dicoJeu["In"][1]:
				square(t, e, ligne, "green")
			elif ligne == dicoJeu["Out"][0] and e == dicoJeu["Out"][1]:
				square(t, e, ligne, "red")
			elif dicoJeu["ly"][ligne][e] == 1:
				square(t, e, ligne, "grey")
			elif dicoJeu["ly"][ligne][e] == 0:
				square(t, e, ligne, "white")

def square(t, x, y, fc):
	up()
	goto(-(window_width()/2)+(x*t), (window_height()/2)-(y*t)) # ecris a partir du coin haut gauche de coordonnées (0,0) pour la suite
	fillcolor(fc)
	begin_fill()
	for a in range(4):
		forward(t)
		right(90)
	end_fill()

def pixel2cell(x, y, dicoJeu):
	colonne = int(x/dicoJeu["tcell"])
	ligne = int(y/dicoJeu["tcell"])
	return colonne, ligne

def testClic(x, y, dicoJeu):
	colonne, ligne = pixel2cell(x, y, dicoJeu)
	if 0 <= colonne <= len(dicoJeu["ly"][0]) and 0 <= ligne <= len(dicoJeu["ly"]):
		return colonne, ligne
	print("Erreur, coordonnées non comprises dans le labyrinthe")
	return None, None

def cell2pixel(i, j, dicoJeu):
	x = i*dicoJeu["tcell"] + (dicoJeu["tcell"]/2)
	y = -(j*dicoJeu["tcell"] + (dicoJeu["tcell"]/2))
	return x, y

def typeCellule(ligne, colonne, dicoJeu):
	if ligne == dicoJeu["In"][0] and colonne == dicoJeu["In"][1]:
		return "entrée"
	elif ligne == dicoJeu["Out"][0] and colonne == dicoJeu["Out"][1]:
		return "sortie"
	elif dicoJeu["ly"][ligne][colonne] == 1:
		return "mur"
	elif dicoJeu["ly"][ligne][colonne] == 0:
		somme_voisins = dicoJeu["ly"][ligne+1][colonne] + dicoJeu["ly"][ligne-1][colonne] + dicoJeu["ly"][ligne][colonne+1] + dicoJeu["ly"][ligne][colonne-1]
		if somme_voisins == 0:
			return "carrefour"
		elif somme_voisins == 1:
			return "passage + voie"
		elif somme_voisins == 2:
			return "passage"
		elif somme_voisins == 3:
			return "impasse"

############################# Programme principal #############################
ly, In, Out = labyFromFile("labys\laby0.laby")
dicoJeu = {"ly" : ly, "In" : In, "Out" : Out, "tcell" : 50}

# 1 : Travail preparatoire
for e in ly:
    print(e)
print("Entrée : ", In, "\nSortie : ", Out)

# 2 : Affichage de labyrinthe
afficheTextuel(dicoJeu)
afficheGraphique(dicoJeu) # attention affichage du coin gauche non modifiable

# 3 : Positionnement de la tortue
onscreenclick(testClic) # erreur ?
mainloop()

i, j = pixel2cell(65, 120, dicoJeu)
print(cell2pixel(i, j, dicoJeu))

# 4 : Cases spéciales
print(typeCellule(1,1, dicoJeu))