#!/usr/bin/env python3
"""EDGE Corner, Emres Richtung: die Kante als Rahmenecke.

Konstruiert die Ecke im selben Raster wie die Wortmarke und erzeugt alle
SVG-Dateien. Aenderungen hier machen, nie in den Einzeldateien.

Raster: Versalhoehe 160, Buchstabenbreite 200, Strichstaerke 18.
Strichstaerken-Leiter: 11 (Light) -> 18 (Regulaer) -> 30 (Ecke),
jeder Schritt Faktor 1,64. Die Ecke ist damit kein Fremdkoerper,
sondern die naechste Sprosse derselben Leiter.

Referenz vermessen (image Kopie.png): Buchstaben 10-11 px, Ecke 18 px,
Faktor 1,7. Der Verlauf laeuft hell -> dunkel um die Ecke; das Magenta
der Referenz ist kein CI-Ton und wird durch Purple ersetzt.
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

# ---------------------------------------------------------------- Wortmarke
# identisch zur Hauptmarke (offener Schnitt)
E_OFFEN = ('<rect x="0" y="0" width="200" height="18"/>'
           '<rect x="0" y="71" width="88" height="18"/>'
           '<rect x="0" y="142" width="200" height="18"/>')
E_OFFEN_M = ('<rect x="0" y="0" width="200" height="18"/>'
             '<rect x="112" y="71" width="88" height="18"/>'
             '<rect x="0" y="142" width="200" height="18"/>')
D = '<path d="M0 9 H120 A71 71 0 0 1 120 151 H0" fill="none" stroke="{c}" stroke-width="18"/>'
G = ('<path d="M200 9 H80 A71 71 0 0 0 80 151 H200" fill="none" stroke="{c}" stroke-width="18"/>'
     '<rect x="126" y="71" width="74" height="18"/>'
     '<rect x="182" y="71" width="18" height="89"/>')

WORT = "".join(f'<g transform="translate({x},0)">{t}</g>'
               for t, x in [(E_OFFEN, 0), (D, 270), (G, 516), (E_OFFEN_M, 786)])
WORT_B = 986

# ---------------------------------------------------------------- Ecke
ECKE_STRICH = 30          # Leiter 11 -> 18 -> 30, Faktor 1,64
ECKE_H = 200              # horizontaler Schenkel = eine Buchstabenbreite
ECKE_ENDE = 80            # der Schenkel greift bis zur Mittelachse des Wortes
ABSTAND = 54              # die Schutzzone; die Ecke haelt sie selbst ein

# Aussenkanten: rechts x=WORT_B+ABSTAND+ECKE_STRICH, oben y=-ABSTAND-ECKE_STRICH
# Mittellinien daraus:
mx = WORT_B + ABSTAND + ECKE_STRICH / 2          # 1031
my = -ABSTAND - ECKE_STRICH / 2                  # -69
x0 = WORT_B + ABSTAND + ECKE_STRICH - ECKE_H     # 876: Beginn des horizontalen Schenkels
y1 = ECKE_ENDE                                   # Ende auf der Wortmitte

def ecke(stroke):
    """Die Rahmenecke als ein Pfad. Runde Aussenecke (linejoin) verbindet die
    Formsprache der Boegen von D und G mit den flachen Balken der E's."""
    return (f'<path d="M{x0} {my} H{mx} V{y1}" fill="none" stroke="{stroke}" '
            f'stroke-width="{ECKE_STRICH}" stroke-linejoin="round" stroke-linecap="butt"/>')

VERLAUF = (f'<linearGradient id="kante" gradientUnits="userSpaceOnUse" '
           f'x1="{x0}" y1="{my}" x2="{mx}" y2="{y1}">'
           f'<stop offset="0" stop-color="{CYAN}"/>'
           f'<stop offset=".5" stop-color="{BLAU}"/>'
           f'<stop offset="1" stop-color="{PURPLE}"/></linearGradient>')

LOCKUP_VB = f"0 {my - ECKE_STRICH / 2 - 6} {mx + ECKE_STRICH / 2 + 6} {160 - (my - ECKE_STRICH / 2 - 6) + 6}"
# etwas Luft (6) rundum, damit die runde Ecke nicht am Rand klebt


def schreibe(name, viewbox, inhalt):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">\n{inhalt}\n</svg>\n')


# ---------------------------------------------------------------- Lockups
for cname, farbe in [("white", "#FFFFFF"), ("black", "#000000"),
                     ("ci-weiss", WEISS), ("ci-schwarz", SCHWARZ)]:
    inhalt = (f'<g fill="{farbe}" color="{farbe}">{WORT.format(c=farbe)}</g>'
              + ecke(farbe))
    schreibe(f"edge-corner-mono-{cname}.svg", LOCKUP_VB, inhalt)

# Verlauf auf der Ecke, Wort monochrom (die Referenz-treue Fassung)
for cname, farbe in [("auf-dunkel", WEISS), ("auf-hell", SCHWARZ)]:
    inhalt = (f'<defs>{VERLAUF}</defs>'
              f'<g fill="{farbe}" color="{farbe}">{WORT.format(c=farbe)}</g>'
              + ecke("url(#kante)"))
    schreibe(f"edge-corner-verlauf-{cname}.svg", LOCKUP_VB, inhalt)

# ---------------------------------------------------------------- Icon: E in der Ecke
# Das Icon ist das letzte E der Wortmarke mit derselben Ecke: Abstand 54,
# horizontaler Schenkel 200, Ende auf der Mittelachse des E. Keine neuen Zahlen.
i_mx = 200 + ABSTAND + ECKE_STRICH / 2            # 269
i_my = -ABSTAND - ECKE_STRICH / 2                 # -69
i_x0 = i_mx + ECKE_STRICH / 2 - ECKE_H            # 84
ICON_VB = f"-14 {i_my - ECKE_STRICH / 2 - 14} {i_mx + ECKE_STRICH / 2 + 28} {160 - i_my + ECKE_STRICH / 2 + 28}"

def icon_pfad(stroke):
    return (f'<path d="M{i_x0} {i_my} H{i_mx} V{ECKE_ENDE}" fill="none" stroke="{stroke}" '
            f'stroke-width="{ECKE_STRICH}" stroke-linejoin="round" stroke-linecap="butt"/>')

for cname, farbe in [("white", "#FFFFFF"), ("black", "#000000"), ("ci-weiss", WEISS)]:
    schreibe(f"edge-corner-icon-mono-{cname}.svg", ICON_VB,
             f'<g fill="{farbe}">{E_OFFEN}</g>' + icon_pfad(farbe))

ICON_VERLAUF = ('<linearGradient id="kante" gradientUnits="userSpaceOnUse" '
                f'x1="{i_x0}" y1="{i_my}" x2="{i_mx}" y2="{ECKE_ENDE}">'
                f'<stop offset="0" stop-color="{CYAN}"/>'
                f'<stop offset=".5" stop-color="{BLAU}"/>'
                f'<stop offset="1" stop-color="{PURPLE}"/></linearGradient>')
schreibe("edge-corner-icon-verlauf.svg", ICON_VB,
         f'<defs>{ICON_VERLAUF}</defs><g fill="{WEISS}">{E_OFFEN}</g>' + icon_pfad("url(#kante)"))

print("\n".join(sorted(os.listdir(OUT))))
print(f"\n{len(os.listdir(OUT))} Dateien in {OUT}")
