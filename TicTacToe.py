# Da man nur eine Datei anfügen kann, konnte ich euch keine README.md anfügen. Schaut gerne auf github unter https://github.com/gabrieldudau/Programmiervorkurs_Challenge/tree/master vorbei, um euch das testen zu vereinfachen :)

import re
import time
import random

# \033[F ist um eine Zeile nach oben zu gehen
# \033[K ist um die Zeile zu löschen


class StupidBot:
    def __init__(self):
        self.name = "Stoopid Bot"

    def makeMove(self, field) -> list:
        emptyFields = []
        for i in range(3):
            for j in range(3):
                if field[i][j] == 0:
                    emptyFields.append([i, j])
        
        return random.choice(emptyFields)

class SmartBot:
    def __init__(self):
        self.name = "Smart Bot"

    def checkWin(self, field: list):
        '''
        Überprüft ob ein Spieler gewonnen hat.
        Zurückgegeben wird:
        - 0: Kein Spieler hat gewonnen
        - 1: X hat gewonnen
        - 2: O hat gewonnen
        '''
        
        for i in range(3):
            if field[i][0] == field[i][1] == field[i][2] != 0:
                return field[i][0]
        
        for i in range(3):
            if field[0][i] == field[1][i] == field[2][i] != 0:
                return field[0][i]
        
        if field[0][0] == field[1][1] == field[2][2] != 0:
            return field[0][0]
        
        if field[0][2] == field[1][1] == field[2][0] != 0:
            return field[0][2]

        return 0
    
    def makeMove(self, field) -> list:
        '''
        Macht den bestmöglichen Zug für den Bot.
        '''
        
        possibleMoves = []
        for i in range(3):
            for j in range(3):
                if field[i][j] == 0:
                    possibleMoves.append([i, j])  # Es werden alle Stellungen hinzugefügt, die möglich wären.
        
        scores = []
        for move in possibleMoves:
            new_field = [row[:] for row in field]  # Kopie des Spielfeldes, um das original nicht zu verändern
            new_field[move[0]][move[1]] = 2  # Der Bot macht einen Zug, und schaut wie es weitergeht.
            scores.append(self.getMoveScore(new_field, 2, len(possibleMoves), True))
        
        biggest = float("-inf")
        biggestI = 0
        for i in range(len(scores)):
            if scores[i] > biggest:
                biggest = scores[i]
                biggestI = i
        
        return possibleMoves[biggestI]
    

    
    def getMoveScore(self, field: list, currentPlayer: int, weight: int, firstmove:bool) -> int:
        '''
        Es wird eine Summe erstellt für jede eingegebene Position. Die Summe wird um 1 erhöht, wenn aus dieser Position ein 
        Gewinn entsteht, um 1 verringert, wenn aus der Position verloren wird, und 1 hinzugefügt wenn aus dieser Position ein 
        Gleichstand entsteht.
        '''

        winner = self.checkWin(field)

        if winner == 2:
            return (1 * weight) if not firstmove else  1000000000
        elif winner == 1:
            return weight -10

        possibleMoves = []
        for i in range(3):
            for j in range(3):
                if field[i][j] == 0:
                    possibleMoves.append([i, j])
        
        if len(possibleMoves) == 0:
            return 0

        sum = 0
        for move in possibleMoves:
            field[move[0]][move[1]] = currentPlayer
            sum += self.getMoveScore(field, 2 if currentPlayer == 1 else 1, weight - 1, False)
            field[move[0]][move[1]] = 0

        return sum



# Initialisierung des Spielfeldes

field = [[],[],[]]

for i in range (3):
    for j in range (3):
        field[i].append(0)

# Werte: 0 = leer, 1 = X, 2 = O



def checkWin():
    '''
    Überprüft ob ein Spieler gewonnen hat.
    Zurückgegeben wird:
    - 0: Kein Spieler hat gewonnen
    - 1: X hat gewonnen
    - 2: O hat gewonnen
    '''
    
    for i in range(3):
        if field[i][0] == field[i][1] == field[i][2] != 0:
            return field[i][0]
    
    for i in range(3):
        if field[0][i] == field[1][i] == field[2][i] != 0:
            return field[0][i]
    
    if field[0][0] == field[1][1] == field[2][2] != 0:
        return field[0][0]
    
    if field[0][2] == field[1][1] == field[2][0] != 0:
        return field[0][2]

    return 0

def checkFieldFull():
    '''
    Überprüft, ob das Spielfeld voll ist, und damit kein Spieler gewonnen hat.
    '''
    for i in range (3):
        for j in range(3):
            if(field[i][j] == 0):
                return False
    return True

def printPlayField():
    '''
    Es braucht 14 Zeilen für diese Ausgabe. Hier wird das Spielfeld auf der Konsole ausgegeben.
    '''
    print("-"*35)
    for i in range (len(field)):
        print("||         ||         ||         ||")
        for j in range (len(field[i])):
            print("||    ", end="")
            if field[i][j] == 0:
                print("     ", end="")
            elif field[i][j] == 1:
                print("X    ", end="")
            else:
                print("O    ", end="")
        
        print("||")
        print("||         ||         ||         ||")
        print("-"*35, end="\n")
    print()
    

def printWinField():
    wayOfWin = 0            # 1 = horizontal, 2 = vertikal, 3 = diagonal
    rowOfWin = 0            # 0 = 1. Zeile, 1 = 2. Zeile, 2 = 3. Zeile
    columnOfWin = 0         # 0 = 1. Spalte, 1 = 2. Spalte, 2 = 3. Spalte
    diagonalOfWin = 0       # 0 = Diagonale von links oben nach rechts unten, 1 = Diagonale von rechts oben nach links unten

    for i in range(3):
        if field[i][0] == field[i][1] == field[i][2] != 0:
            wayOfWin = 1
            rowOfWin = i
            break
    
    for i in range(3):
        if field[0][i] == field[1][i] == field[2][i] != 0:
            wayOfWin = 2
            columnOfWin = i
            break
    
    if field[0][0] == field[1][1] == field[2][2] != 0:
        wayOfWin = 3
        diagonalOfWin = 0
    
    if field[0][2] == field[1][1] == field[2][0] != 0:
        wayOfWin = 3
        diagonalOfWin = 1

    if wayOfWin == 1:
        print("-"*35)
        for i in range (len(field)):
            if i == rowOfWin:
                print("||▄▄▄▄▄▄▄▄▄||▄▄▄▄▄▄▄▄▄||▄▄▄▄▄▄▄▄▄||")
            else:
                print("||         ||         ||         ||")

            for j in range (len(field[i])):
                print("||███▌" if i == rowOfWin else "||    ", end="")
                if field[i][j] == 0:
                    print(" ▐███" if i == rowOfWin else "     ", end="")
                elif field[i][j] == 1:
                    print("X▐███" if i == rowOfWin else "X    ", end="")
                else:
                    print("O▐███" if i == rowOfWin else "O    ", end="")
            
            print("||")
            if i == rowOfWin:
                print("||▀▀▀▀▀▀▀▀▀||▀▀▀▀▀▀▀▀▀||▀▀▀▀▀▀▀▀▀||")
            else:
                print("||         ||         ||         ||")
            print("-"*35, end="\n")
        print()
    
    if wayOfWin == 2:
        print("-"*35)
        for i in range (len(field)):
            if columnOfWin == 0:
                print("||   ███   ||         ||         ||")
            elif columnOfWin == 1:
                print("||         ||   ███   ||         ||")
            else:
                print("||         ||         ||   ███   ||")
            for j in range (len(field[i])):
                print("||   ▌" if j == columnOfWin else "||    ", end="")
                if field[i][j] == 1:
                    print("X▐   " if j == columnOfWin else "X    ", end="")
                else:
                    print("O▐   " if j == columnOfWin else "O    ", end="")
            
            print("||")
            if columnOfWin == 0:
                print("||   ███   ||         ||         ||")
            elif columnOfWin == 1:
                print("||         ||   ███   ||         ||")
            else:
                print("||         ||         ||   ███   ||")
            print("-"*35, end="\n")
        print()

    if wayOfWin == 3:
        if diagonalOfWin == 0:
            print("-"*35)
            for i in range (len(field)):
                if(i == 0):
                    print("||████▙▄   ||         ||         ||")
                elif(i == 1):
                    print("||         ||████▙▄   ||         ||")
                else:
                    print("||         ||         ||████▙▄   ||")

                for j in range (len(field[i])):
                    print("|| ▜█▌" if i == j else "||    ", end="")
                    if field[i][j] == 0:
                        print("▐█▙  " if i == j else "     ", end="")
                    elif field[i][j] == 1:
                        print("X▐█▙ " if i == j else "X    ", end="")
                    else:
                        print("O▐█▙ " if i == j else "O    ", end="")
                print("||")
                if(i == 0):
                    print("||   ▀▜████||         ||         ||")
                elif(i == 1):
                    print("||         ||   ▀▜████||         ||")
                else:
                    print("||         ||         ||   ▀▜████||")
                print("-"*35, end="\n")

            print()
        else:
            print("-"*35)
            for i in range (len(field)):
                if(i == 0):
                    print("||         ||         ||   ▄▟████||")
                elif(i == 1):
                    print("||         ||   ▄▟████||         ||")
                else:
                    print("||   ▄▟████||         ||         ||")

                for j in range (len(field[i])):
                    print("|| ▄▟▌" if (abs(i) + abs(j) == 2) else "||    ", end="")       # abs(i) + abs(j) ist das gleiche wie (i == 0 and j == 2) or (i == 1 and j == 1) or (i == 2 and j == 0)
                    if field[i][j] == 0:
                        print(" ▐▛▀ " if (abs(i) + abs(j) == 2) else "     ", end="")
                    elif field[i][j] == 1:
                        print("X▐▛▀ " if (abs(i) + abs(j) == 2) else "X    ", end="")
                    else:
                        print("O▐▛▀ " if (abs(i) + abs(j) == 2) else "O    ", end="")
                print("||")
                if(i == 0):
                    print("||         ||         ||████▛▀   ||")
                elif(i == 1):
                    print("||         ||████▛▀   ||         ||")
                else:
                    print("||████▛▀   ||         ||         ||")
                print("-"*35, end="\n")

            print()



def enterName(player:int) -> str:
    """
    Der spieler mit der Nummer 'player' wird aufgefordert seinen Namen einzugeben. 
    Hierbei wird geprüft, ob der Name richtig ist.

    Args:
        player (int): Die Nummer des Spielers, der seinen Namen eingeben soll.

    Returns:
        str: Der bestätigte Name des Spielers.
    """


    print(f"Spieler {player}, gebe deinen Namen ein"," \n   (Gebe sBot ein, um gegen einem schlauen Bot zu spielen <nicht gewinnbar> \n    oder bBot ein, um gegen einem schlechten Bot zu spielen <gewinnbar>):   "if player == 2 else ":   ", end="")

    name = input()

    answer = ""

    if player == 2:
        print("\033[F\033[K"*2, end="")

    while answer != "y":
        print("\033[F\033[K", end="")
        
        print(f"Ist der Name \"{name}\" richtig? Gebe 'y' ein um fortzufahren. Ansonsten gebe 'n' ein:   ", end="")
        answer = input()
        
        if answer == "y":
            print("\033[F\033[K", end="")
            continue
        
        print("\033[F\033[K", end="")

        print("Schreibe deinen Namen erneut auf:   ", end="")
        name = input()
    
    return name



def checkInputPosition(user: str) -> bool:
    '''
    Überprüft, ob die Benutzereingabe für die Position auf dem Spielfeld gültig ist.
    '''
    
    pattern = re.compile(r".*[012].*,.*[012].*")
    if not pattern.match(user):
        return False

    input = getInputList(user)
    if field[input[0]][input[1]] != 0:
        return False
    
    return True


def getInputList(user: str) -> list:
    pattern = re.compile(r".*([012]).*,.*([012]).*")        # Dieses Regex-Muster wird benutzt, um die Indexe aus der Benutzereingabe zu extrahieren.
                                                                # Jedes Index wird dabei in eine eigene Gruppe gespeichert.

    match = pattern.search(user)                                # Mithilfe von search() wird das Objekt match erstellt, welches es uns erlaubt, auf die Gruppen zuzugreifen.

    return [int(match.group(1)), int(match.group(2))]           # Die Gruppen werden in eine Liste gespeichert und zurückgegeben.

# Game Loop

player1 = ""
player2 = ""


print(r".___________. __    ______        .___________.    ___       ______        .___________.  ______    _______ ")
print(r"|           ||  |  /      |       |           |   /   \     /      |       |           | /  __  \  |   ____|")
print(r"`---|  |----`|  | |  ,----' ______`---|  |----`  /  ^  \   |  ,----' ______`---|  |----`|  |  |  | |  |__   ")
print(r"    |  |     |  | |  |     |______|   |  |      /  /_\  \  |  |     |______|   |  |     |  |  |  | |   __|  ")
print(r"    |  |     |  | |  `----.           |  |     /  _____  \ |  `----.           |  |     |  `--'  | |  |____ ")
print(r"    |__|     |__|  \______|           |__|    /__/     \__\ \______|           |__|      \______/  |_______|")
print(r"                                                                                                            ")
print(r"                                                                                                            ")
print(r"                                                                                                            ")


player1 = enterName(1)

print(f"Spieler 1:  {player1}  ")

player2 = enterName(2)


# --- ein Bot wird erstellt, der random Züge macht --- 
botPlayer = False
if player2 == "sBot" or player2 == "bBot":
    botPlayer = True
    bot = SmartBot() if player2 == "sBot" else StupidBot()
    player2 = bot.name

print(f"\033[F\033[K"*3 + f"Spieler 1:  {player1}          -          Spieler 2:  {player2}  \n")


winner = checkWin()
currentPlayer = 1

draw = False

while winner == 0:
    printPlayField()

    currentPlayerSign = "X" if currentPlayer == 1 else "O"

    currentPlayerName = player1 if currentPlayer == 1 else player2

    print(f"{currentPlayerName}, wo möchtest du dein Zeichen setzen?  > Zeile, Spalte <    (beides sind Zahlen zwischen 0 und 2)   ", end="")
    
    if currentPlayer == 2:
        if botPlayer:
            botMove = bot.makeMove(field)
            user = str(botMove[0]) + "," + str(botMove[1])
        else:
            user = input()
    else:
        user = input()

    isUserInputValid = False

    while not isUserInputValid:
        isUserInputValid = checkInputPosition(user)
        if(isUserInputValid):
            break

        print("\033[F\033[K", end="")
        print(f"Die Eingabe war falsch! Versuche es nochmal, beide Zahlen müssen zwischen 0 und 2 liegen <>Zeile, Spalte<>:   ", end="")
        user = input()
    
    move = getInputList(user)


    print(f"\033[K" if currentPlayer == 2 and botPlayer else f"\033[F\033[K", end="")
    print(f"{currentPlayerName} macht ein {currentPlayerSign} in der {move[0]}. Zeile und {move[1]}. Spalte!")

    time.sleep(1)

    print("\033[F\033[K"*15, end="")
    field[move[0]][move[1]] = currentPlayer
    
    winner = checkWin()
    
    if winner == 0:
        printPlayField()
        
        print(f"{player1 if currentPlayer == 1 else player2} macht ein {currentPlayerSign} in der {move[0]}. Zeile und {move[1]}. Spalte!")
    else:
        printWinField()
        print(f"{player1 if currentPlayer == 1 else player2} macht ein {currentPlayerSign} in der {move[0]}. Zeile und {move[1]}. Spalte!")
        break

    time.sleep(1)
    
    draw = checkFieldFull()
    if draw:
        break

    currentPlayer = 1 if currentPlayer == 2 else 2

    print("\033[F\033[K"*15, end="")

if draw:
    print("\n\nUnentschieden! Keiner hat gewonnen!\n\n")
else:
    print(f"\n\n{player1 if winner == 1 else player2} hat gewonnen! Herzlichen Glückwunsch!\n\n")


