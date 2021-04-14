from math import *
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import newton
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print("Ten program wizualizuje ruch punktu materialnego w rzucie ukośnym przy oporze powietrza")

m = float(input("Podaj masę ciała\n m[kg] = "))
y0 = float(input("Podaj wysokość z której rzucono ciało:\n h[m] = "))
v0 = float(input("Podaj prędkość początkową ciała:\n v0[m\s] = "))
B = float(input("Podaj współczynnik oporu powietrza:\n B = "))
alpha = float(input("Podaj kąt który tworzy wektor prędkości początkowej z osią OX:\n alpha[deg.] = "))

alpha0 = radians(alpha) 
mu = B / m # Na potrzeby obliczeń dzielę przez masę
g = 9.81   # przyspieszenie ziemskie

x0 = 0.0   # ustalam x początkowy
vx0, vy0 = v0 * cos(alpha0), v0 * sin(alpha0) #ustalam składowe prędkości początkowej


#####################################################################################

#Główna funkcja wyliczająca w ogólności parametry x, y, vx, vy
#Jest to zasadniczo rozwiązanie układu równań różniczkowych. Wybrałem ten sposób,
#ponieważ radzi sobie z bardziej ekstremalnymi wartościami parametrów początkowych


def ruch_ciała(g, mu, xy0, vxy0, tt):
    # Używam wektora vec = [x, y, vx ,vy]
    def dif(vec, t):
        # Pochodna czasowa wektora vec
        v = sqrt(vec[2] ** 2 + vec[3] ** 2)
        return [vec[2], vec[3], -mu * v * vec[2], -g - mu * v * vec[3]]

    # numeryczne rozwiązanie równania różniczkowego
    vec = odeint(dif, [xy0[0], xy0[1], vxy0[0], vxy0[1]], tt)
    return vec[:, 0], vec[:, 1], vec[:, 2], vec[:, 3]  
    # zwraca x, y, vx, vy (a w zasadzie listy ich wartości)

#####################################################################################

# Liczę czas dla którego y jest maksymalne. ,,newton" znajduje miejsce zerowe prędkości w osi y
# zwróconej przez funkcję zadaną przez wyrażenie lambda w zależności od parametru oznaczającego czas
T_szczyt = newton(lambda t: ruch_ciała(g, mu, (x0, y0), (vx0, vy0), [0, t])[3][1], 0)

# Oblicza maksymalną wysokość na jakiej znajdzie się ciało - na potrzeby dopasowania rozmiaru wykresu
y_max = ruch_ciała(g, mu, (x0, y0), (vx0, vy0), [0, T_szczyt])[1][1]

# Oblicza czas ruchu poprzez znalezienie miejsca zerowego ,,y", drugi argument funkcji newton, 
# to ,,zgadnięcie" czyli przewidywana przeze mnie minimalna wartość czasu dla szukanego miejsca
#  zerowego y. Ma na celu przyspieszenie obliczeń
T = newton(lambda t: ruch_ciała(g, mu, (x0, y0), (vx0, vy0), [0, t])[1][1], 2 * T_szczyt)

#zadaję czas, sama animacja nie jest w czasie rzeczywistym, ponieważ przy bardziej ekstremalnych parametrach 
#początkowych trwała by zbyt długo. Przy podziale na 1000 elementów gładkość wykresu jest dobra. 
t = np.linspace(0, T, 1000)

x, y, vx, vy = ruch_ciała(g, mu, (x0, y0), (vx0, vy0), t)

####################################################################################

fig, ax = plt.subplots(tight_layout = True)
wykres_rzutu, = ax.plot([], [], '-b', label = "tor ruchu" , linewidth=2)
marker_położenia, = ax.plot([], [], 'ro', label ="ciało", ms = 8)
if alpha > 90:
    if y_max > abs(x[-1]):
        ax.set_xlim(-6 * y_max / 5, 0)
        ax.set_ylim(0, 6 * y_max / 5)
    else:
        ax.set_xlim(6 * x[-1] / 5, 0)
        ax.set_ylim(0, 6 * abs(x[-1]) / 5)
else:
    if y_max > x[-1]:
        ax.set_xlim(0, 6 * y_max / 5)
        ax.set_ylim(0, 6 * y_max / 5)
    else:
        ax.set_xlim(0, 6 * x[-1] / 5)
        ax.set_ylim(0, 6 * x[-1] / 5)
ax.grid()
ax.set_xlabel("Odległość [m]")
ax.set_ylabel("$Wysokość$ [m]")
ax.set_title(r"Rzut ukośny z oporem powietrza proporcjonalnym do $V^2$", fontsize = 12)
ax.legend()

def Dane(i):
    wykres_rzutu.set_data(x[:i+1], y[:i+1])
    marker_położenia.set_data(x[i], y[i])
    return wykres_rzutu, marker_położenia

#animacja ma nieliniowy przebieg czasu, by trwała krócej, oraz by dla dużych parametrów początkowych
#ostatnia faza ruchu ,,opadanie" trwało krócej.

animacja = animation.FuncAnimation(fig, Dane, len(x), interval = 20/len(x), blit = True, repeat = False)

plt.show()
