#!/usr/bin/env pybricks-micropython
#! must be on top of file ↑
# made by Spotnit

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
# brickrun -r --directory="/home/robot/EV3python/auto_chessboard" "/home/robot/EV3python/auto_chessboard/main.py"


# Create your variables here.
# diameter =3.04 
diameter = 1.0225
omtrek = diameter * 3.141592653589793238
speed = 2
linkstolerantie = 0
ondertolerantie = 0
x_coördinaat = 0  #! plaats waar karretje staat
y_coördinaat = 0
letter_values = {
    "y": 0,
    "z": 3.5,
    "a": 7,
    "b": 10.5,
    "c": 14,
    "d": 17.5,
    "e": 21,
    "f": 24.5,
    "g": 28,
    "h": 31.5,
    "i": 35,
    "j": 38.5,
}
gameover = False
player = "white"
pawn_count_w = 0
rook_count_w = 0
knight_count_w = 0
bishop_count_w = 0
pawn_count_b = 0
rook_count_b = 0
knight_count_b = 0
bishop_count_b = 0


# Create your objects here.
ev3 = EV3Brick()
motorB = Motor(Port.B)
motorW = Motor(Port.C)
motorR = Motor(Port.A)
cart = DriveBase(motorB, motorW, wheel_diameter=diameter, axle_track=100)
ev3.speaker.set_speech_options(language="en-us", voice="m3", speed=120, pitch=50)


# Write your functions here.
def loc_to_cor(location):  # a4
    x_cor = int(letter_values.get(location[0], None))
    y_cor = (int(location[1]) - 1) * 3.6
    return (x_cor, y_cor)  # 7 , 10.5


def rand_loc_to_(target_loc):  # a4 , b8 
    global x_coördinaat
    global y_coördinaat
    #! eindpunt - beginpunt
    x_cor, y_cor = loc_to_cor(target_loc)
    x_afstand = x_cor - x_coördinaat
    y_afstand = y_cor - y_coördinaat

    if x_afstand != 0:
        if y_coördinaat <= 26.25:
            boven(1.75)
        else:
            onder(1.75)

    if x_afstand > 0:
        rechts(x_afstand)
    else:
        links(x_afstand)

    if y_afstand != 0:
        rechts(1.75)

    if y_afstand > 0:
        boven(y_afstand)
    else:
        onder(y_afstand)

    if y_afstand != 0:
        links(1.75)

    if x_afstand != 0:
        if y_coördinaat <= 26.25:
            onder(1.75)
        else:
            boven(1.75)


def kingside_castle():
    if player == "white":
        rand_loc_to_("e1")
        magnet(True)
        rechts(7)
        magnet(False)
        rechts(3.5)
        magnet(True)
        boven(1.75)
        links(7)
        onder(1.75)
        magnet(False)
    else:
        rand_loc_to_("e8")
        magnet(True)
        rechts(7)
        magnet(False)
        rechts(3.5)
        magnet(True)
        onder(1.75)
        links(7)
        boven(1.75)
        magnet(False)


def queenside_castle():
    if player == "white":
        rand_loc_to_("e1")
        magnet(True)
        links(10.5)
        magnet(False)
        links(3.5)
        magnet(True)
        boven(1.75)
        rechts(7)
        onder(1.75)
        magnet(False)
    else:
        rand_loc_to_("e8")
        magnet(True)
        links(10.5)
        magnet(False)
        links(3.5)
        magnet(True)
        onder(1.75)
        rechts(7)
        boven(1.75)
        magnet(False)


def free_space(piece):
    global pawn_count_w
    global rook_count_w
    global knight_count_w
    global bishop_count_w
    global pawn_count_b
    global rook_count_b
    global knight_count_b
    global bishop_count_b

    if piece == "p":
        if player == "white":
            pawn_count_w += 1
            return "z" + str(pawn_count_w)
        else:
            pawn_count_b += 1
            return "i" + str(pawn_count_b)

    elif piece == "q":
        if player == "white":
            return "y4"
        else:
            return "j4"

    elif piece == "r":
        if player == "white":
            rook_count_w += 1
            if rook_count_w == 1:
                return "y1"
            else:
                return "y8"
        else:
            rook_count_b += 1
            if rook_count_b == 1:
                return "j1"
            else:
                return "j8"

    elif piece == "n":
        if player == "white":
            knight_count_w += 1
            if knight_count_w == 1:
                return "y2"
            else:
                return "y7"
        else:
            knight_count_b += 1
            if knight_count_b == 1:
                return "j2"
            else:
                return "j7"

    elif piece == "b":
        if player == "white":
            bishop_count_w += 1
            if bishop_count_w == 1:
                return "y3"
            else:
                return "y6"
        else:
            bishop_count_b += 1
            if bishop_count_b == 1:
                return "j3"
            else:
                return "j6"


def piece_to_start():  # for next update
    pass


def chess_notation_to_sentence(notation: str) -> str:
    pieces = {
        "k": "King",
        "q": "Queen",
        "r": "Rook",
        "b": "Bishop",
        "n": "Knight",
        "p": "Pawn",
    }
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]

    if notation[0] in pieces:
        piece = pieces[notation[0]]
        notation = notation[1:]
    elif notation[0] in files:
        piece = "Pawn"
    elif notation == "0-0":
        piece = pieces["k"]
        move_type = "castles kingside"
        sentence = "{} {}".format(piece, move_type)
        return sentence
    elif notation == "0-0-0":
        piece = pieces["k"]
        move_type = "castles queenside"
        sentence = "{} {}".format(piece, move_type)
        return sentence
    else:
        return "Invalid input: long algebraic notation required"

    if "#" in notation:
        checkmate = True
        notation = notation[:-1]
    else:
        checkmate = False

    if "+" in notation:
        check = True
        notation = notation[:-1]
    else:
        check = False

    if "=" in notation:
        promotion_index = notation.index("=")
        promotion_piece = pieces[notation[promotion_index + 1]]
        promotion_square_index = promotion_index - 2
        promotion_square = notation[promotion_square_index:promotion_index]
        sentence = "{} on {} promotes to {} on {}".format(
            piece, promotion_square, promotion_piece, promotion_square
        )
        return sentence

    if "-" in notation:
        move_type = "moves to"
        target_square_index = notation.index("-") + 1
        target_square = notation[target_square_index:]
        start_square_index = 0
        start_square = notation[start_square_index : target_square_index - 1]
    elif "e.p." in notation:
        move_type = "captures en passant on"
        start_square_index, target_square_index = [
            i for i, c in enumerate(notation) if c in (" ", "x")
        ]
        target_square = notation[start_square_index + 1 : target_square_index]
        start_square = notation[:start_square_index]
    elif "x" in notation:
        move_type = "captures on"
        target_square_index = notation.index("x") + 1
        target_square = notation[target_square_index:]
        start_square_index = 0
        start_square = notation[start_square_index : target_square_index - 1]
    else:
        return "Invalid input: long algebraic notation required"

    if move_type == "captures en passant on":
        sentence = "{} on {} captures the pawn en passant on {}".format(
            piece, start_square, target_square
        )
    else:
        sentence = "{} on {} {} {}".format(
            piece, start_square, move_type, target_square
        )

    if checkmate:
        sentence += ", resulting in a checkmate"
    elif check:
        sentence += ", putting the opponent's king in check"

    return sentence


def magnet(status):
    if status:
        motorR.run_until_stalled(speed=-200, then=Stop.BRAKE, duty_limit=35)

    else:
        motorR.run_until_stalled(speed=200, duty_limit=30)


def dis_to_ang(distance):
    return round((distance / omtrek) * 360)


def rechts(afstand):
    afstand = abs(afstand)
    global x_coördinaat
    motorB = Motor(Port.B, Direction.CLOCKWISE)
    motorB.reset_angle(0)
    motorW.reset_angle(0)
    cart.reset()

    x_coördinaat = x_coördinaat + afstand
    angle = dis_to_ang(afstand)
    while abs(motorB.angle()) < angle:
        cart.drive(speed, 0)

    cart.stop()
    motorB.hold()
    motorW.hold()
    wait(500)
    motorB.brake()
    motorW.brake()
    wait(500)
    motorB.stop()
    motorW.stop()

    # print(motorB.angle())
    # print(motorW.angle())
    # print("target: ", dis_to_ang(afstand))


def links(afstand):
    afstand = abs(afstand)
    global x_coördinaat
    motorB = Motor(Port.B, Direction.CLOCKWISE)
    motorB.reset_angle(0)
    motorW.reset_angle(0)
    cart.reset()

    x_coördinaat = x_coördinaat - afstand
    angle = dis_to_ang(afstand + linkstolerantie)
    while abs(motorB.angle()) < angle:
        cart.drive(-speed, 0)

    cart.stop()
    motorB.hold()
    motorW.hold()
    wait(500)
    motorB.brake()
    motorW.brake()
    wait(500)
    motorB.stop()
    motorW.stop()

    # print(motorB.angle())
    # print(motorW.angle())
    # print("target: ", dis_to_ang(afstand + linkstolerantie))


def boven(afstand):
    afstand = abs(afstand)
    global y_coördinaat
    motorB = Motor(Port.B, Direction.COUNTERCLOCKWISE)
    motorB.reset_angle(0)
    motorW.reset_angle(0)
    cart.reset()

    y_coördinaat = y_coördinaat + afstand
    angle = dis_to_ang(afstand)
    while abs(motorB.angle()) < angle:
        cart.drive(speed, 0)

    cart.stop()
    motorB.hold()
    motorW.hold()
    wait(500)
    motorB.brake()
    motorW.brake()
    wait(500)
    motorB.stop()
    motorW.stop()

    # print(motorB.angle())
    # print(motorW.angle())
    # print("target: ", dis_to_ang(afstand))


def onder(afstand):
    afstand = abs(afstand)
    global y_coördinaat
    motorB = Motor(Port.B, Direction.COUNTERCLOCKWISE)
    motorB.reset_angle(0)
    motorW.reset_angle(0)
    cart.reset()

    y_coördinaat = y_coördinaat - afstand
    angle = dis_to_ang(afstand + ondertolerantie)
    while abs(motorB.angle()) < angle:
        cart.drive(-speed, 0)

    cart.stop()
    motorB.hold()
    motorW.hold()
    wait(500)
    motorB.brake()
    motorW.brake()
    wait(500)
    motorB.stop()
    motorW.stop()

    # print(motorB.angle())
    # print(motorW.angle())
    # print("target: ", dis_to_ang(afstand + ondertolerantie))


def game():
    print("let the game start!")
    global player
    gameover = False
    input_s = ""
    player = "white"
    pawn_count_w = 0
    rook_count_w = 0
    knight_count_w = 0
    bishop_count_w = 0
    pawn_count_b = 0
    rook_count_b = 0
    knight_count_b = 0
    bishop_count_b = 0

    while not gameover:
        input_s = "move: " + player + " = "
        command = input(input_s).lower()
        temp = command
        if "stop" in command:
            break

        if "x" in command:
            if not "e.p." in command:
                temp = (
                    command[:6] + command[7:] if isinstance(command, str) else command
                )

        sentence = chess_notation_to_sentence(temp)  #! long algebraic notation
        print(sentence)
        ev3.speaker.say(sentence)

        if "e.p." in command:
            piece = command[0]
            loc1 = command[1] + command[2]
            loc2 = command[4] + command[5]
            if player == "white":
                rand_loc_to_(loc1)
                magnet(True)
                rand_loc_to_(loc2)
                magnet(False)
                loc = command[4] + str((int(command[5]) - 1))
                rand_loc_to_(loc)
                magnet(True)
                rand_loc_to_(free_space("p"))  # pawn
                magnet(False)
            else:
                rand_loc_to_(loc1)
                magnet(True)
                rand_loc_to_(loc2)
                magnet(False)
                loc = command[4] + str((int(command[5]) + 1))
                rand_loc_to_(loc)
                magnet(True)
                rand_loc_to_(free_space("p"))  # pawn
                magnet(False)

        elif "0-0-0" in command:
            queenside_castle()

        elif "0-0" in command:
            kingside_castle()

        elif "-" in command:
            piece = command[0]
            loc1 = command[1] + command[2]
            loc2 = command[4] + command[5]
            rand_loc_to_(loc1)
            magnet(True)
            rand_loc_to_(loc2)
            magnet(False)

        elif "x" in command:
            piece = command[6]
            loc1 = command[1] + command[2]
            loc2 = command[4] + command[5]
            rand_loc_to_(loc2)
            magnet(True)
            loc = free_space(piece)
            print(loc)
            rand_loc_to_(loc)
            magnet(False)
            rand_loc_to_(loc1)
            magnet(True)
            rand_loc_to_(loc2)
            magnet(False)

        if "#" in command:
            print("checkmate")
            ev3.speaker.say("checkmate")
            ev3.speaker.play_file(SoundFile.CHEERING)
            gameover = True

            answer = input("do you want to put all the pieces on te start place(y/n)")
            if answer == "y" or "Y":
                piece_to_start()
            else:
                pass

        if player == "white":
            player = "black"
        else:
            player = "white"


# Write program here.

while True:
    command = input("command: ").lower()

    if command == "stop":
        print("program stop.")
        break

    elif command == "0x0":
        print(x_coördinaat)
        print(y_coördinaat)
        rand_loc_to_("y1")

    elif "right" in command:
        try:
            afstand = float(command.split()[1])
            print("Distance:", afstand)
            rechts(afstand)  # cm
        except IndexError:
            print("Distance not provided")

    elif "left" in command:
        try:
            afstand = float(command.split()[1])
            print("Distance:", afstand)
            links(afstand)  # cm
        except IndexError:
            print("Distance not provided")

    elif "up" in command:
        try:
            afstand = float(command.split()[1])
            print("Distance:", afstand)
            boven(afstand)  # cm
        except IndexError:
            print("Distance not provided")

    elif "down" in command:
        try:
            afstand = float(command.split()[1])
            print("Distance:", afstand)
            onder(afstand)  # cm
        except IndexError:
            print("Distance not provided")
    elif "game" in command:
        game()

    elif "goto" in command:
        try:
            position = command.split()[1].lower()
            rand_loc_to_(position)
        except IndexError:
            print("position not provided")

    elif "magnet" in command:
        try:
            status = command.split()[1]
            if status == "1":
                status = True
            else:
                status = False
            magnet(bool(status))
        except:
            print("status not provided")

    elif "loc" in command:
        print(x_coördinaat, y_coördinaat)

    elif not command == "":
        print("command dus not exist!")

# commands
# stop
# 0x0
# right 5
# left 5
# up 5
# down 5
# game
# goto e4
# magnet 1
# loc
