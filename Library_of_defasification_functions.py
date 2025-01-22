import math         



def Method_of_division_in_half(P, eps):     # Метод деления пополам для метода USt1 (Bisection method for USt1 method)
    tL=0 
    tR=1
    teps=0.5
    while teps>eps:
        t=(tL+tR)/2
        f=t-t*math.log(t)
        if f == P:
            fi=t
            break
        elif f < P:
            tL=t
            teps=teps/2
        else:
            tR=t
            teps=teps/2
        fi=t
    return fi


def Adamo(a, b, c, alfa):                   # Метод Адамо (Adamo method)
    o=c-(c-b)*alfa
    return o


def CofMax(a, b, c):                        # Метод центра максимумов (Center maxima method)
    o=b
    return o


def CofMass(a, b, c):                       # Метод Центра масс (Center of Mass Method)
    o=(a+b+c)/3
    return o


def Medians(a, b, c):                       # Метод Медианы (Median Method)
    o=(a+2*b+c)/4
    return o


def Chang(a, b, c):                         # Метод - индекс Чанга (Method - Chang Index)
    o=(c**2-a**2-a*b+b*c)/6
    return o


def PAv(a, b, c):                           # Метод - возможное среднее (Method - Possible Average)
    o=(a+4*b+c)/6
    return o


def Jager(a, b, c):                         # Метод - индекс Ягера (Method - Yager index)
    o=(a+2*b+c)/44
    return o


def USt1(a, b, c):                          # Метод - USt1 (Method - USt1)
    eps=0.0001
    if (a+c)/2==b:
        o=b
    elif(a+c)/2<b:
        o=b-(b-a)*Method_of_division_in_half((((b-a)-(c-b))/(2*(b-a))), eps)
    elif(a+c)/2>b:
        o=b+(c-b)*Method_of_division_in_half((((c-b)-(b-a))/(2*(c-b))), eps)
    return o
