from turtle import *

# Utils
def labyFromFile(fn):
	f = open(fn)
	laby = []
	indline = 0
	dicoportails = {}
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
			elif "0" <= item <= "9":
				if item in dicoportails: # associe les deux portails par leurs coordonnées
					labyline.append(dicoportails[item])
					
					laby[dicoportails[item][0]].insert(dicoportails[item][1], (indline, inditem))
				else: # récupere le premier portail pour l'associer au deuxieme par la suite
					dicoportails[item] = (indline, inditem)
			# discard "\n" char at the end of each line
			inditem += 1
		laby.append(labyline)
		indline += 1
	f.close()
	return laby, mazeIn, mazeOut

def pixel2cell(x, y):
	x = -(dicoJeu["csg"][0] - x) - 20 # distance a l'origine du repère (le coin superieur gauche)
	y = (dicoJeu["csg"][1] - y) - 20
	colonne = int(x/dicoJeu["tcell"])
	ligne = int(y/dicoJeu["tcell"])
	return colonne, ligne

def cell2pixel(i, j):
	x = dicoJeu["csg"][0] + j*dicoJeu["tcell"] + (dicoJeu["tcell"]/2) # attention j les colonnes et i les lignes et donc inversé avec coordonnées d'un plan
	y = dicoJeu["csg"][1] - i*dicoJeu["tcell"] - (dicoJeu["tcell"]/2)
	return x, y

def testClic(x, y):
	colonne, ligne  = pixel2cell(x, y)
	if 0 <= ligne < len(dicoJeu["ly"]) and 0 <= colonne < len(dicoJeu["ly"][0]):
		return True
	else:
		print("Erreur, coordonnées non comprises dans le labyrinthe")
		return False

def collisions(x, y):
	colonne, ligne  = pixel2cell(x, y)
	if dicoJeu["ly"][ligne][colonne] != 1:
		return True
	else:
		print("Mur, changez de direction")
		dicoJeu["difficultée"]["vies"] -= 1 # bonus, perd une vie
		return False

def somme_des_voisins(ligne, colonne):
	somme = 0
	if not isinstance(dicoJeu["ly"][ligne+1][colonne], tuple):
		somme += dicoJeu["ly"][ligne+1][colonne]
	if not isinstance(dicoJeu["ly"][ligne-1][colonne], tuple):
		somme += dicoJeu["ly"][ligne-1][colonne]
	if not isinstance(dicoJeu["ly"][ligne][colonne+1], tuple):
		somme += dicoJeu["ly"][ligne][colonne+1]
	if not isinstance(dicoJeu["ly"][ligne][colonne-1], tuple):
		somme += dicoJeu["ly"][ligne][colonne-1]
	return somme

def typeCellule(ligne, colonne):
	if ligne == dicoJeu["In"][0] and colonne == dicoJeu["In"][1]:
		return "entrée"
	elif ligne == dicoJeu["Out"][0] and colonne == dicoJeu["Out"][1]:
		return "sortie"
	elif dicoJeu["ly"][ligne][colonne] == 1:
		return "mur"
	elif dicoJeu["ly"][ligne][colonne] == 0:
		somme_voisins = somme_des_voisins(ligne, colonne)
		if somme_voisins == 0:
			return "carrefour"
		elif somme_voisins == 1:
			return "passage + voie"
		elif somme_voisins == 2:
			return "passage"
		elif somme_voisins == 3:
			return "impasse"
	elif dicoJeu["ly"][ligne][colonne] == 2: # pièces
		return "pièce"
	elif dicoJeu["ly"][ligne][colonne] == 3: # pièces
		return "diamant"
	elif isinstance(dicoJeu["ly"][ligne][colonne], tuple): # portail
		return "portail" # (verifie si le type de dicoJeu["ly"][ligne][colonne] est bien un tuple)

def typeCelluleHardcore(ligne, colonne):
	if ligne == dicoJeu["In"][0] and colonne == dicoJeu["In"][1]: # entrée
		return "entrée"
	elif ligne == dicoJeu["Out"][0] and colonne == dicoJeu["Out"][1]: # sortie
		return "sortie"
	elif dicoJeu["ly"][ligne][colonne] == 1: # mur
		return "mur"
	elif dicoJeu["ly"][ligne][colonne] == 0: # chemin
		somme_voisins = somme_des_voisins(ligne, colonne)
		if somme_voisins == 0:
			return "carrefour"
		elif somme_voisins == 1:
			if not isinstance(dicoJeu["ly"][ligne+1][colonne], tuple) and dicoJeu["ly"][ligne+1][colonne] == 1: # si le seul mur est en bas, alors il n'y en a pas ailleurs
				return "carrefour sauf bas"
			elif not isinstance(dicoJeu["ly"][ligne-1][colonne], tuple) and dicoJeu["ly"][ligne-1][colonne] == 1: # 4 possibilitées
				return "carrefour sauf haut"
			elif not isinstance(dicoJeu["ly"][ligne][colonne]+1, tuple) and dicoJeu["ly"][ligne][colonne+1] == 1:
				return "carrefour sauf droite"
			elif not isinstance(dicoJeu["ly"][ligne+1][colonne-1], tuple) and dicoJeu["ly"][ligne][colonne-1] == 1:
				return "carrefour sauf gauche"
		elif somme_voisins == 2:
			# Hyyyyyperrr long car on doit verifier que chaque coté tésté n'est pas un tuple..
			if not isinstance(dicoJeu["ly"][ligne][colonne+1], tuple) and not isinstance(dicoJeu["ly"][ligne][colonne-1], tuple) and (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne][colonne+1]) == 2:  # si les murs sont a gauche et a droite, alors il n' en a pas en haut et en bas
				return "passage haut bas"
			elif not isinstance(dicoJeu["ly"][ligne][colonne-1], tuple) and not isinstance(dicoJeu["ly"][ligne+1][colonne], tuple) and (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne+1][colonne]) == 2: # 6 possibilitées
				return "passage haut droite"
			elif not isinstance(dicoJeu["ly"][ligne+1][colonne], tuple) and not isinstance(dicoJeu["ly"][ligne][colonne+1], tuple) and (dicoJeu["ly"][ligne+1][colonne] + dicoJeu["ly"][ligne][colonne+1]) == 2:
				return "passage haut gauche"
			elif not isinstance(dicoJeu["ly"][ligne+1][colonne], tuple) and not isinstance(dicoJeu["ly"][ligne-1][colonne], tuple) and (dicoJeu["ly"][ligne+1][colonne] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage gauche droite"
			elif not isinstance(dicoJeu["ly"][ligne][colonne+1], tuple) and not isinstance(dicoJeu["ly"][ligne-1][colonne], tuple) and (dicoJeu["ly"][ligne][colonne+1] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage gauche bas"
			elif not isinstance(dicoJeu["ly"][ligne][colonne-1], tuple) and not isinstance(dicoJeu["ly"][ligne-1][colonne], tuple) and (dicoJeu["ly"][ligne][colonne-1] + dicoJeu["ly"][ligne-1][colonne]) == 2:
				return "passage droite bas"
		elif somme_voisins == 3:
			return "impasse"
	elif dicoJeu["ly"][ligne][colonne] == 2: # pièces
		return "pièce"
	elif dicoJeu["ly"][ligne][colonne] == 3: # pièces
		return "diamant"
	elif isinstance(dicoJeu["ly"][ligne][colonne], tuple): # portail
		return "portail" # (verifie si le type de dicoJeu["ly"][ligne][colonne] est bien un tuple)

def quitter():
	global ecoute
	ecoute = False

def suppr_detours(co_deplacement, cellules):
	tot = 0
	for d in range(len(co_deplacement)):
		if co_deplacement.count(co_deplacement[d]) == 2:
			for d2 in range(d, len(co_deplacement)):
				if co_deplacement[d2] ==  co_deplacement[d]:
					df = d2
			del(co_deplacement[d:df + 1])
			del(dicoJeu["li_deplacements"][d:df + 1])
			del(cellules[d:df + 1])
			tot += df - d
	print("actions inutiles supprimées :", tot)

def coté_debut():
	if dicoJeu["In"][1] == 0:
		return "gauche"
	elif dicoJeu["In"][1] == (len(dicoJeu["ly"][0])-1):
		return "droite"
	elif dicoJeu["In"][0] == 0:
		return "haut"
	elif dicoJeu["In"][0] == (len(dicoJeu["ly"])-1):
		return "bas"
	else:
		return "milieu"

def portail(ligne, colonne):
	ligne_tp = dicoJeu["ly"][ligne][colonne][0] # renvoie les coordonnées de l'autre coté du portail, c'est a dire les elements du tuple (ligne, colonne)
	colonne_tp = dicoJeu["ly"][ligne][colonne][1]
	return ligne_tp, colonne_tp

# Graphic
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
			Cell = typeCellule(ligne, colonne)
			if Cell == "entrée":
				square(t, colonne, ligne, "green")
			elif Cell == "sortie":
				square(t, colonne, ligne, "red")
			elif Cell == "mur":
				square(t, colonne, ligne, "grey")
			elif Cell == "passage":
				square(t, colonne, ligne, "#fef0a8")
			elif Cell == "passage + voie":
				square(t, colonne, ligne, "#fff8d4")
			elif Cell == "carrefour":
				square(t, colonne, ligne, "white")
			elif Cell == "impasse":
				square(t, colonne, ligne, "#ffea7f")
			# elif Cell == "pièce":

			# elif Cell == "diamant":

			elif Cell == "portail":
				square(t, colonne, ligne, "pink")

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

def animations_tortue(x, y):
	colonne, ligne = pixel2cell(x, y)
	cell = typeCellule(ligne, colonne)
	if cell == "sortie":
		color("green")
		print("Bravo, vous avez gagné")
	elif cell == "carrefour":
		color("pink")
	elif cell == "impasse":
		color("brown")

# Travel
def gauche():
	x = xcor() - dicoJeu["tcell"]
	y = ycor()
	if deplacement_portail(x,y):
		dicoJeu["difficultée"]["actions"] -= 1
		return True
	elif testClic(x, y) and collisions(x, y):
		dicoJeu["difficultée"]["actions"] -= 1
		dicoJeu["li deplacements"].append("gauche")
		color("black")
		tiltangle(180) # se positionne a 180 degres par rapport a 0 (et non pas par rapport a l'ancien angle)
		goto(x,y)
		animations_tortue(x, y)
		return True
	else:
		color("red")
		return False

def droite(): 
	x = xcor() + dicoJeu["tcell"]
	y = ycor()
	if deplacement_portail(x,y):
		dicoJeu["difficultée"]["actions"] -= 1
		return True
	elif testClic(x, y) and collisions(x, y):
		dicoJeu["difficultée"]["actions"] -= 1
		dicoJeu["li deplacements"].append("droite")
		color("black")
		tiltangle(0)
		goto(x,y)
		animations_tortue(x, y)
		return True
	else:
		color("red")
		return False

def bas():
	x = xcor()
	y = ycor() - dicoJeu["tcell"]
	if deplacement_portail(x,y):
		dicoJeu["difficultée"]["actions"] -= 1
		return True
	elif testClic(x, y) and collisions(x, y):
		dicoJeu["difficultée"]["actions"] -= 1
		dicoJeu["li deplacements"].append("bas")
		color("black")
		tiltangle(270)
		goto(x,y)
		animations_tortue(x, y)
		return True
	else:
		color("red")
		return False

def haut(): 
	x = xcor()
	y = ycor() + dicoJeu["tcell"]
	if deplacement_portail(x,y):
		dicoJeu["difficultée"]["actions"] -= 1
		return True
	elif testClic(x, y) and collisions(x, y):
		dicoJeu["difficultée"]["actions"] -= 1
		dicoJeu["li deplacements"].append("haut")
		color("black")
		tiltangle(90)
		goto(x,y)
		animations_tortue(x, y)
		return True
	else:
		color("red")
		return False

def gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly):
	action = gauche()
	if action:
		co_deplacement.append((ligne, colonne-1))
		nb_exploration_ly[ligne][colonne] += 1
	return action, "gauche"

def droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly):
	action = droite()
	if action:
		co_deplacement.append((ligne, colonne+1))
		nb_exploration_ly[ligne][colonne] += 1
	return action, "droite"

def basauto(ligne, colonne, co_deplacement, nb_exploration_ly):
	action = bas()
	if action:
		co_deplacement.append((ligne+1, colonne))
		nb_exploration_ly[ligne][colonne] += 1
	return action, "bas"

def hautauto(ligne, colonne, co_deplacement, nb_exploration_ly):
	action = haut()
	if action:
		co_deplacement.append((ligne-1, colonne))
		nb_exploration_ly[ligne][colonne] += 1
	return action, "haut"

def suivreChemin(liste_mouvements):
	up()
	goto(cell2pixel(dicoJeu["In"][0] , dicoJeu["In"][1]))
	down()
	showturtle()
	for mouvement in liste_mouvements:
		if mouvement == "gauche":
			valide = gauche()
		elif mouvement == "droite":
			valide = droite()
		elif mouvement == "bas":
			valide = bas()
		elif mouvement == "haut":
			valide = haut()
		if not(valide):
			print("erreur, mouvement impossible")
	print("Chemin parcouru avec succès")

def inverserChemin(liste_mouvements):
	liste_mouvements_reverse = list(liste_mouvements)
	liste_mouvements_reverse.reverse()
	for mouvement in liste_mouvements_reverse: # même fonctionnement que suivreChemin, avec des actions inversées
		if mouvement == "gauche":
			valide = droite()
		elif mouvement == "droite":
			valide = gauche()
		elif mouvement == "bas":
			valide = haut()
		elif mouvement == "haut":
			valide = bas()
		if not(valide):
			print("erreur, mouvement impossible")
	print("Chemin parcouru en sens inverse avec succès")

def deplacement_portail(x,y):
	colonne, ligne = pixel2cell(x,y)
	if typeCellule(ligne, colonne) == "portail":
		ligne_tp, colonne_tp = portail(ligne, colonne)
		up()
		delay(10) # marque une pause
		goto(cell2pixel(ligne_tp, colonne_tp)) # se téléporte de l'autre coté du portail
		down()
		return True
	else:
		return False

# Independant
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

def explorer():
	up()
	goto(cell2pixel(dicoJeu["In"][0] , dicoJeu["In"][1]))
	down()
	showturtle()
	# initialisation de la tortue
	derniere_action = coté_debut()
	ligne = dicoJeu["In"][0] ; colonne = dicoJeu["In"][1]
	co_deplacement = [] # enregistre les coordonnées (i,j) de chaque case ou on est passé, dans l'ordre
	cellules = [] # enregistre chaque type de cellule ou on est passé, dans l'ordre
	nb_exploration_ly = [[0 for e in range(len(dicoJeu["ly"][0]))] for e in range(len(dicoJeu["ly"]))] # grille qui représente le nombre de passages sur chaque case du laby
	nb_deplacements = 0
	action = False
	typeCell = typeCelluleHardcore(ligne, colonne)
	while typeCell != "sortie":
		# print(derniere_action, typeCell, action) # comprehension des beugs
		if typeCell == "impasse" or typeCell == "entrée": # retourne en arrière a une impasse et avance si on est a l'entrée
			if derniere_action == "haut":
				action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly) # 4 cas
			elif derniere_action == "bas":
				action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "gauche":
				action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "droite":
				action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "milieu": # si le début du labyrinthe n'est pas sur un coté
				typeCell = typeCelluleHardcore(ligne, colonne)
		elif typeCell == "carrefour": # continue la route dans la même direction qu'avant, sauf si deja exploré
			if derniere_action == "haut" and nb_exploration_ly[ligne-1][colonne] <= 4:# 4 cas
				action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "bas" and nb_exploration_ly[ligne+1][colonne] <= 4:
				action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "gauche" and nb_exploration_ly[ligne][colonne-1] <= 4:
				action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif derniere_action == "droite" and nb_exploration_ly[ligne][colonne+1] <= 4:
				action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly)
		elif typeCell in ["carrefour sauf bas", "carrefour sauf haut", "carrefour sauf gauche", "carrefour sauf droite"]: # Va en priorité a : droite / haut / gauche / bas
			if typeCell != "carrefour sauf droite" and nb_exploration_ly[ligne][colonne+1] <= 5:# 4 cas
				action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell != "carrefour sauf haut" and nb_exploration_ly[ligne-1][colonne] <= 5:
				action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell != "carrefour sauf gauche" and nb_exploration_ly[ligne][colonne-1] <= 5:
				action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell != "carrefour sauf bas" and nb_exploration_ly[ligne+1][colonne] <= 5:
				action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly)
		elif typeCell in ["passage haut bas", "passage haut droite", "passage haut gauche", "passage gauche droite", "passage gauche bas", "passage droite bas"]:# suit le chemin du passage
			if typeCell == "passage haut bas":
				if derniere_action == "bas":
					action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly) # 6 cas avec 2 cas pour chaque
				elif derniere_action == "haut":
					action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly) # si c'est une ligne droite, continuer dans la meme direction (2 cas * 2)
			elif typeCell == "passage gauche droite":
				if derniere_action == "droite":
					action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly)
				elif derniere_action == "gauche":
					action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell == "passage haut droite":
				if derniere_action == "gauche":
					action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly) # si c'est un coude, changer de direction (4 cas * 2)
				elif derniere_action == "bas":
					action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly) # attention la derniere action ne fait pas partie des 2 du passage
			elif typeCell == "passage haut gauche":
				if derniere_action == "droite":
					action, derniere_action = hautauto(ligne, colonne, co_deplacement, nb_exploration_ly)
				elif derniere_action == "bas":
					action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell == "passage gauche bas":
				if derniere_action == "haut":
					action, derniere_action = gaucheauto(ligne, colonne, co_deplacement, nb_exploration_ly)
				elif derniere_action == "droite":
					action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly)
			elif typeCell == "passage droite bas":
				if derniere_action == "haut":
					action, derniere_action = droiteauto(ligne, colonne, co_deplacement, nb_exploration_ly)
				elif derniere_action == "gauche":
					action, derniere_action = basauto(ligne, colonne, co_deplacement, nb_exploration_ly)
		elif typeCell == "portail" and derniere_action != "teleportation": # pour ne pas qu'il boucle entre les deux cotés du portail
			ligne_tp, colonne_tp = portail(ligne, colonne)
			up()
			goto(cell2pixel(ligne_tp, colonne_tp)) # se téléporte de l'autre coté du portail
			down()
			derniere_action = "teleportation"
		if action:
			nb_deplacements += 1
		colonne, ligne  = pixel2cell(xcor(), ycor()) # update des coordonnées
		cellules.append(typeCell)
		typeCell = typeCelluleHardcore(ligne, colonne) # update de la cellule
	# Fin de boucle quand on trouve l'arrivé
	print("------------------ Exploration automatique ------------------")
	suppr_detours(co_deplacement, cellules) # suppression des detours, pas encore uttilisé (ni verifié)
	print("Vous avez gagné en", nb_deplacements, "déplacements.")
	print("------------------ Exploration automatique ------------------")

############################# Programme principal #############################
nom_laby = input("Nom du labyrinthe : ")
ly, In, Out = labyFromFile("Labys/" + nom_laby + ".laby")
dicoJeu = {"ly" : ly, "In" : In, "Out" : Out, "tcell" : 40, "csg" : [-(window_width()/2) + 20 , (window_height()/2) - 20], "li deplacements" : [], "difficultée" : {"vies" : 5, "temps" : 500, "actions" : 60}}
bgcolor("black")
speed('fastest')
hideturtle()

# P1 Exportation et affichage de labyrinthes :

# 1 : Travail préparatoire
# for e in ly:
#     print(e)
# print("Entrée : ", In, "\nSortie : ", Out)

# # 2 : Affichage de labyrinthe
# afficheTextuel()
# afficheGraphique()

# # 3 : Positionnement de la tortue
# onscreenclick(testClic)
# mainloop()

# i, j = pixel2cell(65, 120)
# print(cell2pixel(i, j))

# # 4 : Cases spéciales
# print(typeCellule(1,1))
afficheGraphiquebonus()

# P2 Navigation Guidée :

# 6 : Navigation guidée
ecran = Screen()
up()
goto(cell2pixel(dicoJeu["In"][0] , dicoJeu["In"][1]))
down()
showturtle()
ecran.onkeypress(gauche,"Left")
ecran.onkeypress(droite,"Right")
ecran.onkeypress(haut,"Up")
ecran.onkeypress(bas,"Down")
ecran.onkeypress(quitter,"q")
ecran.listen()

# # alternative a mainloop() car celle ci ne se stoppe que si on ferme la fenetre (ici on arrete la boucle quand "q" est appuyé sur le clavier)
# ecoute = True
# while ecoute:
# 	ecran.update()

# 6)-7)-8)
# mouvements = list(dicoJeu["li deplacements"]) # on copie sans associativité sinon la liste augmenterais a chaque nouveau mouvement (y compris ceux des fonctions)
# suivreChemin(mouvements) # variante a l'énnoncé, on repars du départ avec suivreChemin() donc on fait : entrée -> arrivée -> entrée
# inverserChemin(mouvements)
# done()

# P3 Navigation automatique dans un labyrinthe simple :

# 1)-2)-3)
# explorer()

# # 4) variante a l'énoncé : la tortue fait directement le chemin a l'écran dans la fonction explorer (et donc graçe a turtle) 
# # donc on n'a pas besoin de tester le chemin dans la fonction suivreChemin(). On peut quand même la faire suivre le chemin trouvé.

# mouvements = list(dicoJeu["li deplacements"])
# suivreChemin(mouvements)
# inverserChemin(mouvements)
# done()

# problème actuel : fonction deja_explore qui prend trop ou pas assez de cas en compte 
# (bloque parfois le chemin alors que c'est pas necessaire, et ne le bloque pas d'autre fois ce qui fait boucler indefiniement)

# modification pour la complexité : créer une grille avec le nombre de passage sur chaque case au lieu de calculer a chaque fois pour toutes les cases avec .count

# modification pour s'adapter : le nombre limite de passage sur une case dépend du type de la case (alors qu'avant c'etait 2 passage max quelle que soit la case) (pas suffisant)

# P4 Extensions :

# 7 : Améliorer l’interface

# créer une interface graphique de fond ou des "boutons" sont liés a des zones de pixels
# boutons : Echap / changer de laby
# uttiliser une autre tortue pour implémenter des boutons et autres (vitesse car division des taches)

# 8 : créer des labyrinthes 

# créer un menu dans echap qui permet d'acceder a la modification (changement de background + boutons pour positioner les murs)
# ajouter boutons pour positionner les pieces et les portails
# verifier que le labyrinthe a une entrée et au moins une sortie (option : et qu'elle est accessible)

# 9 : donjons et tortues

# créer des cases teleportation qui sont link 2 a 2 et qui permettent d'aller a un autre endroit ( 2 cases = 1 couleur)
# proposer des difficultées differentes (nombre de vies, temps pour résoudre, nombre d'actions)
# créer un objet collectable (pieces) qui sont comme des trophés dont le total est affiché a l'ecran
# quand le labyrinthe est fini, passer au niveau suivant (faire une graduation de laby de plus en plus durs)
