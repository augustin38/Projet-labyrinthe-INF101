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

def afficheTextuel():
	print("\nLabyrinthe Textuel :")
	for ligne in range(len(dicoJeu["ly"])):
		for colonne in range(len(dicoJeu["ly"][ligne])):
			if ligne == dicoJeu["In"][0] and colonne == dicoJeu["In"][1]:
				print("x", end="")
			elif ligne == dicoJeu["Out"][0] and colonne == dicoJeu["Out"][1]:
				print("o", end="")
			elif dicoJeu["ly"][ligne][colonne] == 1:
				print("#", end="")
			elif dicoJeu["ly"][ligne][colonne] == 0:
				print(" ", end="")
		print("")

def afficheGraphique():
	t = dicoJeu["tcell"]
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

def afficheGraphiquebonus():
	t = dicoJeu["tcell"]
	for ligne in range(len(dicoJeu["ly"])):
		for colonne in range(len(dicoJeu["ly"][ligne])):
			if typeCellule(ligne, colonne) == "entrée":
				square(t, colonne, ligne, "green")
			elif typeCellule(ligne, colonne) == "sortie":
				square(t, colonne, ligne, "red")
			elif typeCellule(ligne, colonne) == "mur":
				square(t, colonne, ligne, "grey")
			elif typeCellule(ligne, colonne) == "passage":
				square(t, colonne, ligne, "#fef0a8")
			elif typeCellule(ligne, colonne) == "passage + voie":
				square(t, colonne, ligne, "#fff8d4")
			elif typeCellule(ligne, colonne) == "carrefour":
				square(t, colonne, ligne, "white")
			elif typeCellule(ligne, colonne) == "impasse":
				square(t, colonne, ligne, "#ffea7f")

def square(t, x, y, fc):
	up()
	goto(dicoJeu["csg"][0] + (x*t), dicoJeu["csg"][1] - (y*t)) # ecris a partir du coin superieur gauche
	color("black", fc)
	down()
	begin_fill()
	for a in range(4):
		forward(t)
		right(90)
	end_fill()

def pixel2cell(x, y):
	x = -(dicoJeu["csg"][0] - x) - 20 # distance a l'origine du repère (le coin superieur gauche)
	y = (dicoJeu["csg"][1] - y) - 20
	colonne = int(x/dicoJeu["tcell"])
	ligne = int(y/dicoJeu["tcell"])
	return colonne, ligne

def testClic(x, y):
	colonne, ligne  = pixel2cell(x, y)
	if 0 <= ligne < len(dicoJeu["ly"]) and 0 <= colonne < len(dicoJeu["ly"][0]):
		return True
	else:
		print("Erreur, coordonnées non comprises dans le labyrinthe")
		return False

def cell2pixel(i, j):
	x = dicoJeu["csg"][0] + j*dicoJeu["tcell"] + (dicoJeu["tcell"]/2) # attention j les colonnes et i les lignes et donc inversé avec coordonnées d'un plan
	y = dicoJeu["csg"][1] - i*dicoJeu["tcell"] - (dicoJeu["tcell"]/2)
	return x, y

def typeCellule(ligne, colonne):
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

def collisions(x, y):
	colonne, ligne  = pixel2cell(x, y)
	if dicoJeu["ly"][ligne][colonne] != 1:
		return True
	else:
		print("Mur, changez de direction")
		return False

def gauche():
	x = xcor() - dicoJeu["tcell"]
	y = ycor()
	if testClic(x, y) and collisions(x, y):
		color("black")
		tiltangle(180)
		goto(x,y)
		return True
	else:
		color("red")
		return False

def droite(): 
	x = xcor() + dicoJeu["tcell"]
	y = ycor()
	if testClic(x, y) and collisions(x, y):
		color("black")
		tiltangle(0)
		goto(x,y)
		return True
	else:
		color("red")
		return False

def bas():
	x = xcor()
	y = ycor() - dicoJeu["tcell"]
	if testClic(x, y) and collisions(x, y):
		color("black")
		tiltangle(270)
		goto(x,y)
		return True
	else:
		color("red")
		return False

def haut(): 
	x = xcor()
	y = ycor() + dicoJeu["tcell"]
	if testClic(x, y) and collisions(x, y):
		color("black")
		tiltangle(90)
		goto(x,y)
		return True
	else:
		color("red")
		return False

def typeCelluleHardcore(ligne, colonne):
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
			if dicoJeu["ly"][ligne+1][colonne] == 1: # si le seul mur est en bas, alors il n'y en a pas ailleurs
				return "carrefour sauf bas"
			elif dicoJeu["ly"][ligne-1][colonne] == 1: # 4 possibilitées
				return "carrefour sauf haut"
			elif dicoJeu["ly"][ligne][colonne+1] == 1:
				return "carrefour sauf droite"
			elif dicoJeu["ly"][ligne][colonne-1] == 1:
				return "carrefour sauf gauche"
		elif somme_voisins == 2:
			if (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne][colonne+1]) == 2:  # si les murs sont a gauche et a droite, alors il n' en a pas en haut et en bas
				return "passage haut bas"
			elif (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne+1][colonne]) == 2: # 6 possibilitées
				return "passage haut droite"
			elif (dicoJeu["ly"][ligne+1][colonne] + dicoJeu["ly"][ligne][colonne+1]) == 2:
				return "passage haut gauche"
			elif (dicoJeu["ly"][ligne+1][colonne] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage gauche droite"
			elif (dicoJeu["ly"][ligne][colonne+1] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage gauche bas"
			elif (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage droite bas"
		elif somme_voisins == 3:
			return "impasse"

def coté_debut():
	if dicoJeu["In"][1] == 0:
		return "haut"
	elif dicoJeu["In"][1] == (len(dicoJeu["ly"])-1):
		return "bas"
	if dicoJeu["In"][0] == 0:
		return "gauche"
	elif dicoJeu["In"][0] == (len(dicoJeu["ly"][0])-1):
		return "droite"

def gaucheauto(ligne, colonne, deplacements, co_deplacement):
	action = gauche()
	if action:
		deplacements.append("gauche")
		co_deplacement.append((ligne, colonne-1))
	return action

def droiteauto(ligne, colonne, deplacements, co_deplacement):
	action = droite()
	if action:
		deplacements.append("droite")
		co_deplacement.append((ligne, colonne+1))
	return action

def basauto(ligne, colonne, deplacements, co_deplacement):
	action = bas()
	if action:
		deplacements.append("bas")
		co_deplacement.append((ligne+1, colonne))
	return action

def hautauto(ligne, colonne, deplacements, co_deplacement):
	action = haut()
	if action:
		deplacements.append("haut")
		co_deplacement.append((ligne-1, colonne))
	return action

def explorer():
	derniere_action = coté_debut()
	ligne = dicoJeu["In"][0] ; colonne = dicoJeu["In"][1]
	deplacements = []
	co_deplacement = []
	typeCell = typeCelluleHardcore(ligne, colonne)
	while typeCell != "sortie":
		if typeCell == "impasse" or typeCell == "entrée": # retourne en arrière a une impasse et avance si on est a l'entrée
			if derniere_action == "haut":
				action = bas()
				if action:
					deplacements.append("bas")
					co_deplacement.append((ligne+1, colonne))
			elif derniere_action == "bas":
				action = haut()
				if action:
					deplacements.append("haut")
					co_deplacement.append((ligne-1, colonne))
			elif derniere_action == "gauche":
				action = droite()
				if action:
					deplacements.append("droite")
					co_deplacement.append((ligne, colonne+1))
			elif derniere_action == "droite":
				action = gauche()
				if action:
					deplacements.append("gauche")
					co_deplacement.append((ligne, colonne-1))
		elif typeCell == "carrefour": # continue la route dans la même direction qu'avant
			if derniere_action == "haut":
				action = hautauto(ligne, colonne, deplacements, co_deplacement)
			elif derniere_action == "bas":
				action = basauto(ligne, colonne, deplacements, co_deplacement)
			elif derniere_action == "gauche":
				action = gaucheauto(ligne, colonne, deplacements, co_deplacement)
			elif derniere_action == "droite":
				action = droiteauto(ligne, colonne, deplacements, co_deplacement)
		elif typeCell in ["carrefour sauf bas", "carrefour sauf haut", "carrefour sauf gauche", "carrefour sauf droite"]: # Va en priorité a : droite / haut / gauche / bas
			if typeCell != "carrefour sauf droite":
				action = droiteauto(ligne, colonne, deplacements, co_deplacement)
			elif typeCell != "carrefour sauf haut":
				action = hautauto(ligne, colonne, deplacements, co_deplacement)
			elif typeCell != "carrefour sauf gauche":
				action = gaucheauto(ligne, colonne, deplacements, co_deplacement)
			elif typeCell != "carrefour sauf bas":
				action = basauto(ligne, colonne, deplacements, co_deplacement)
		elif typeCell in ["passage haut bas", "passage haut droite", "passage haut gauche", "passage gauche droite", "passage gauche bas", "passage droite bas"]:
			if typeCell == "passage haut bas":
				if derniere_action == "haut":
					
		typeCell = typeCelluleHardcore(ligne, colonne)


############################# Programme principal #############################
ly, In, Out = labyFromFile("Labys/laby0.laby")
dicoJeu = {"ly" : ly, "In" : In, "Out" : Out, "tcell" : 40, "csg" : [-(window_width()/2) + 20 , (window_height()/2) - 20]}
bgcolor("black")
speed(10000)
hideturtle()

# 1 : Travail préparatoire
# for e in ly:
#     print(e)
# print("Entrée : ", In, "\nSortie : ", Out)

# # 2 : Affichage de labyrinthe
# afficheTextuel(dicoJeu)
# afficheGraphique(dicoJeu) # attention affichage du coin gauche non modifiable

# # 3 : Positionnement de la tortue
# onscreenclick(testClic) # erreur ?
# mainloop()

# i, j = pixel2cell(65, 120, dicoJeu)
# print(cell2pixel(i, j, dicoJeu))

# # 4 : Cases spéciales
# print(typeCellule(1,1, dicoJeu))
afficheGraphiquebonus()

# 6 : Navigation guidée
up()
goto(cell2pixel(dicoJeu["In"][0] , dicoJeu["In"][1]))
down()
showturtle()
onkeypress(gauche,"Left")
onkeypress(droite,"Right")
onkeypress(haut,"Up")
onkeypress(bas,"Down")
listen()
mainloop()

# Navigation automatique dans un labyrinthe simple
