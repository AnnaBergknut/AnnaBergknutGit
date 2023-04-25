
# --------------------------------0.0------------------------------------------------------------------------------------

# print("hello world!") # the standerd to writ hello world the fist thing you do. also it is weird to use # isted of //

# a = "\t i have programed c# before"
# b = "but this far python is fun."
# print(a,b, "`\n What more can i do now while waiting for others to download")

# c = "okay let's make placeholders, my name is {}"
# d = c.format('Anna!')
# print (d)

# how print works (\n is create new row)(\t is to start the text thurther in)({} is uesd to make placeholders)

# --------------------------------------------------föreläsning 1------------------------------------------------------------------

# print("write two numbers:")
# Number1 = int (input("number1: "))
# Number2 = int (input("number2: "))

# if Number2 < Number1:
#     print("Num2<Num1")
# elif Number1 < Number2:
#     print("num1<num2")
# else:
#     print("num1 = num2")

# result = Number1 + Number2

# print("result:", result )

# ---------------------------------------------------------funktioner 1.8 till 1.11 % 1.5----------------------------------------------------------------

# # Simple calculator

# # all funktion under is for us to call on later to do the calculations

# # This function adds two numbers
# def add(a, b): # def is a start of a funktion
#     return a + b

# # This function subtracts two numbers
# def subtract(a, b):
#     return a - b

# # This function multiplies two numbers
# def multiply(a, b):
#     return a * b

# # This function divides two numbers
# def divide(a, b):
#     return a / b

# # Instruktions for user what to do
# print("Select operation.")
# print("1.Add")
# print("2.Subtract")
# print("3.Multiply")
# print("4.Divide")

# while True:
#     # Take input from the user
#     choice = input("Enter choice(1/2/3/4): ")

#     # Check if choice is one of the four options
#     if choice in ('1', '2', '3', '4'):
#         number1 = float(input("Enter first number: ")) # is input a
#         number2 = float(input("Enter second number: ")) # is input b
        
#         # Make and print calculations
#         if choice == '1':
#             print(number1, "+", number2, "=", add(number1, number2))

#         elif choice == '2':
#             print(number1, "-", number2, "=", subtract(number1, number2))

#         elif choice == '3':
#             print(number1, "*", number2, "=", multiply(number1, number2))

#         elif choice == '4':
#             print(number1, "/", number2, "=", divide(number1, number2))
#         break
#     else:
#         print("Invalid Input")

#         ------------------------------------------------------omvandla enheter 1.4 & 1.7 -----------------------------------------------------------

# # How many seconds in a second, be minute, c houres?   

# def calculations(a, b, c):
#     return(a + (b*60)+ (c*3600))

# print("Enter input of time")

# number1 = int(input("Enter seconds: ")) # is input a
# number2 = int(input("Enter minutes: ")) # is input b
# number3 = int(input("Enter houres: ")) # is input c

# print(number3, "h", "+", number2, "min", "+", number1, "sec", "=", calculations(number1, number2, number3), "sec")

# # ----------------------------------------------------------- 1.4 ---------------------------------------------------------------
# #20 km to miles

# # Taking kilometers input from the user
# kilometers = float(input("Enter value in kilometers: "))

# # conversion factor
# conv_fac = 1.609344

# # calculate miles
# miles = kilometers * conv_fac
# print("%0.2f kilometers is equal to %0.2f miles" %(kilometers,miles)) 
# # "print" treats the % as a special caracter you need to add, so it can knoe, that whaen you type "f", the number (result) that will be printed will be a floating point type,
# # and the "0.2" tells your "print" to print only the first 2 digits after the print. - stackoverflow

# ------------------------------------------------------- 1.4 -------------------------------------------------------------------

#                         #translate x kilometor to miles and the other way around

#                         print("Translate kilometers and miles")

#                         print("Select option.")
#                         print("1.Mile to Kilometer")
#                         print("2.Kilometer to Mile")

#                         conv_fac = 1.609344


#                         choice = input("Enter choice(1/2): ")
#                         while True:
#                                 if choice in ("1", "2"):

#                                         elif choice == "1":
#                                                 miles = float(input("Enter miles: "))
#                                                 kilometers = miles * conv_fac
#                                                 print(miles, "miles is", kilometers, "kilometers.")

#                                         elif choice == "2":
#                                                 kilometers = float(input("Enter kilometers: "))
#                                                 miles = kilometers / conv_fac
#                                                 print(kilometers, "kilometers is", miles, "miles.")
#                                                 break

# -------------------------------------------------------- 1.6 -------------------------------------------------------------------------

# print("How old are you on x year?")

# year = int(input("What year were you born?: "))
# month = str(input("What month?: "))
# day = int(input("What day?: "))
# whatYear = int(input("What year do you want to know how old you are?: "))

# howOld = int(whatYear - year)
# print("OK, then you will turn", howOld, "on", month, day, "in", whatYear, "!")

# ------------------------------------------------------------ 1.7---------------------------------------------------------------

# #How many houres, minues and seconds in x seconds?   

# print("How many houres, minues and seconds in x seconds?")
# seconds = int(input("Enter input of seconds: "))

# #I can make varibles for the math so that i don't hardcode but this is so small i don't feel the need for it
# hours = int(seconds/3600)
# minutes = int((seconds-(hours*3600))/60)
# leftOverSeconds = int(seconds - (hours*3600) - (minutes*60))

# print(hours, "hours,", minutes,"minutes,", leftOverSeconds, "seconds.")

# ------------------------------------------------------------1.7 ------------------------------------------------------------------------------

def time():
        inputSeconds = input("how many seconds?: ")

        resultSeconds = int(inputSeconds) % 60
        totalMinutes = int(inputSeconds) // 60
        resultMinutes = totalMinutes % 60
        resultHoures = totalMinutes // 60

        print(inputSeconds, "Seconds are", resultHoures, "houres,", resultMinutes, "minutes and", resultSeconds, "seconds.")

time()


# -----------------------------------------------------------------------------------------------------------------------------------------------

# procent. take two numbers and return the procent of the firt number to the second

# print("what is x procent out of y ")

# number1 = float(input("your x: "))
# number2 = float(input("your y: "))

# quotient = number1/number2
# procent = quotient*100

# print(number1, "is", procent, "%", "out of", number2)

# -----------------------------------------------------------------------------------------------------------------------------------------------

# funktioner

# ett litet kod avsnit som är avgränsat. en tegensten i en tegel vägg.
# en funktion ska gör en sak. avgränsad som hämtar och retunerar sina resultat
# det för definition

# days = 40
# book_pages = 244
# pages = book_pages/days
# print("läs", pages, "sidor on dagen.")

# ------------------------------------------------------------------------------------------------------------------------------------------------------

# import math
# # radius = float(input("input the radius: "))

# def calculate_area():
#     radius = float(input("input the radius: "))
#     (radius* radius) * math.pi 
#     print(radius)

# calculate_area()

# ------------------------------------------------------------------------------------------------------------------------------------------------------

#  #Skriv en funktion som skriver Hello i terminalen.

# def print_msg():
#      print("Hello!")

# print_msg()
