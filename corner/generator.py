#!/usr/bin/env python3
"""EDGE Corner, Emres Richtung: die Kante als Rahmenecke.

Stand 2: Emres Feedback vom 29.07.2026 eingearbeitet.
- Eigener Schriftschnitt nach seiner Referenz (image Kopie.png), pixelgenau
  vermessen und auf das 160er-Raster normalisiert (Faktor 1,882):
  E mit Stamm unten links und 85%-Mittelbalken, D und G elliptisch gerundet,
  enge Sperrung 35 statt 70.
- Ecke nach Referenz: Mitte des horizontalen Schenkels liegt exakt auf der
  Wortkante, Abstand oben = halbe Versalhoehe, Schenkel bis zur Grundlinie,
  Schraegschnitt am Ende, kleine Radien statt weicher Rundung.
- Verlauf endet unten in Rot (#FF6B6B, das EDGE-Rot), nicht in Purple/Pink.

Messwerte Referenz: Versal 85px, Strich ~10px (18 im Raster), E-Mittelbalken
99/116 = 85%, Abstaende 17-19px (~35), Ecke: H-Schenkel 155px (~292, Mitte
ueber Wortende), Abstand oben 44px (~83 -> 80), V-Schenkel bis Grundlinie,
Schraege ca. 30 Grad nach aussen-unten.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "svg")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- Farben
SCHWARZ = "#030309"
WEISS = "#F4F6FF"
CYAN = "#00E2E2"
BLAU = "#009FF4"
PURPLE = "#C15DE6"
ROT = "#FF6B6B"

# ---------------------------------------------------------------- Emre-Schnitt
# Raster: Versalhoehe 160, Strichstaerke 18, Balken-y wie die Hauptmarke
# (0/71/142), aber eigene Breiten, engere Sperrung und andere Formen.
E_B, D_B, G_B = 220, 252, 254
ABST = 35                          # Buchstabenabstand (Referenz 32-36)

# E: oberer Balken frei, Mittel- und Unterbalken haengen am Stamm unten links.
# Mittelbalken 85% der Breite. Das ist Emres "Strich ganz, nicht halb".
E_EMRE = (f'<rect x="0" y="0" width="{E_B}" height="18"/>'
          f'<rect x="0" y="71" width="18" height="89"/>'
          f'<rect x="0" y="71" width="{int(E_B * 0.85)}" height="18"/>'
          f'<rect x="0" y="142" width="{E_B}" height="18"/>')

# D: links offen, rechts elliptisch gerundet (Rx 38, Ry 71 auf der Mittellinie).
D_EMRE = ('<path d="M0 9 H205 A38 71 0 0 1 205 151 H0" fill="none" '
          'stroke="{c}" stroke-width="18"/>')

# G: Spiegelbild der D-Rundung, obere Gerade endet eine halbe Strichstaerke
# frueher (Referenzdetail), langer Sporn, Abstrich bis zur Grundlinie.
G_EMRE = ('<path d="M245 9 H49 A38 71 0 0 0 49 151 H254" fill="none" '
          'stroke="{c}" stroke-width="18"/>'
          '<rect x="149" y="71" width="105" height="18"/>'
          '<rect x="236" y="71" width="18" height="89"/>')

_x = 0
_teile = []
for _g, _b in [(E_EMRE, E_B), (D_EMRE, D_B), (G_EMRE, G_B), (E_EMRE, E_B)]:
    _teile.append(f'<g transform="translate({_x},0)">{_g}</g>')
    _x += _b + ABST
WORT = "".join(_teile)
WORT_B = _x - ABST                 # 1051, Referenz gemessen 1052

# ---------------------------------------------------------------- Ecke
# Als gefuellte Flaeche, nicht als Stroke: nur so lassen sich Aussenradius,
# fast scharfe Innenecke und der Schraegschnitt getrennt kontrollieren.
ECKE_STRICH = 30                   # Leiter 11 -> 18 -> 30, Faktor 1,64
ECKE_H = 300                       # horizontaler Schenkel
ABSTAND_OBEN = 80                  # halbe Versalhoehe
SCHRAEG = 16                       # Schraegschnitt: aussen laeuft 16 tiefer aus
R_AUS, R_IN = 22, 6

X_OUT = WORT_B + ECKE_H // 2       # 1201: Mitte des Schenkels = Wortkante
X_IN = X_OUT - ECKE_STRICH
X0 = X_OUT - ECKE_H                # 901
Y_IN = -ABSTAND_OBEN               # -80
Y_OUT = Y_IN - ECKE_STRICH         # -110
Y_ENDE = 160                       # Grundlinie

def ecke_pfad(x0=X0, x_out=X_OUT, y_out=Y_OUT, y_in=Y_IN,
              y_ende=Y_ENDE, schraeg=SCHRAEG):
    """Rahmenecke als geschlossene Flaeche mit Schraegschnitt unten."""
    x_in = x_out - ECKE_STRICH
    return (f'M{x0} {y_out} H{x_out - R_AUS} '
            f'A{R_AUS} {R_AUS} 0 0 1 {x_out} {y_out + R_AUS} '
            f'V{y_ende + schraeg} L{x_in} {y_ende} V{y_in + R_IN} '
            f'A{R_IN} {R_IN} 0 0 0 {x_in - R_IN} {y_in} H{x0} Z')

def verlauf(gid, x0, y0, x1, y1):
    """Cyan ueber Blau und Purple bis Rot, hell nach dunkel um die Ecke."""
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" '
            f'x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}">'
            f'<stop offset="0" stop-color="{CYAN}"/>'
            f'<stop offset=".38" stop-color="{BLAU}"/>'
            f'<stop offset=".68" stop-color="{PURPLE}"/>'
            f'<stop offset="1" stop-color="{ROT}"/></linearGradient>')

LOCKUP_VB = f"-6 {Y_OUT - 6} {X_OUT + 12} {Y_ENDE + SCHRAEG - Y_OUT + 12}"


def schreibe(name, viewbox, inhalt):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">\n{inhalt}\n</svg>\n')


# ---------------------------------------------------------------- Lockups
for cname, farbe in [("white", "#FFFFFF"), ("black", "#000000"),
                     ("ci-weiss", WEISS), ("ci-schwarz", SCHWARZ)]:
    inhalt = (f'<g fill="{farbe}">{WORT.format(c=farbe)}</g>'
              f'<path d="{ecke_pfad()}" fill="{farbe}"/>')
    schreibe(f"edge-corner-mono-{cname}.svg", LOCKUP_VB, inhalt)

for cname, farbe in [("auf-dunkel", WEISS), ("auf-hell", SCHWARZ)]:
    inhalt = (f'<defs>{verlauf("kante", X0, Y_OUT, X_OUT, Y_ENDE)}</defs>'
              f'<g fill="{farbe}">{WORT.format(c=farbe)}</g>'
              f'<path d="{ecke_pfad()}" fill="url(#kante)"/>')
    schreibe(f"edge-corner-verlauf-{cname}.svg", LOCKUP_VB, inhalt)

# ---------------------------------------------------------------- Icon
# Dieselben Regeln auf ein einzelnes E: Schenkelmitte ueber der E-Kante,
# Abstand oben 80, bis zur Grundlinie mit Schraegschnitt.
I_XOUT = E_B + ECKE_H // 2         # 370
I_X0 = I_XOUT - ECKE_H             # 70
ICON_VB = f"-14 {Y_OUT - 14} {I_XOUT + 28} {Y_ENDE + SCHRAEG - Y_OUT + 28}"

def icon_pfad():
    return ecke_pfad(x0=I_X0, x_out=I_XOUT)

for cname, farbe in [("white", "#FFFFFF"), ("black", "#000000"), ("ci-weiss", WEISS)]:
    schreibe(f"edge-corner-icon-mono-{cname}.svg", ICON_VB,
             f'<g fill="{farbe}">{E_EMRE}</g><path d="{icon_pfad()}" fill="{farbe}"/>')

schreibe("edge-corner-icon-verlauf.svg", ICON_VB,
         f'<defs>{verlauf("kante", I_X0, Y_OUT, I_XOUT, Y_ENDE)}</defs>'
         f'<g fill="{WEISS}">{E_EMRE}</g><path d="{icon_pfad()}" fill="url(#kante)"/>')

print("Wortbreite:", WORT_B, "| Ecke x", X0, "..", X_OUT, "| viewBox", LOCKUP_VB)
print("\n".join(sorted(os.listdir(OUT))))
