"""TP 2 - Les villes de Madagascar (tuples, déballage, retour multiple)."""
import math
from collections import namedtuple

villes = [
    ("Antananarivo", -18.88, 47.51),
    ("Toamasina", -18.15, 49.40),
    ("Mahajanga", -15.72, 46.32),
    ("Fianarantsoa", -21.45, 47.09),
]

print("Question 1")
for nom, latitude, longitude in villes:
    print(f"{nom} : {latitude}, {longitude}")

print("\nQuestion 2")
plus_au_nord = max(villes, key=lambda v: v[1])
print(plus_au_nord[0])


def bornes(villes):
    """Renvoie le tuple (lat_min, lat_max, lon_min, lon_max)."""
    latitudes = [v[1] for v in villes]
    longitudes = [v[2] for v in villes]
    return min(latitudes), max(latitudes), min(longitudes), max(longitudes)


print("\nQuestion 3")
lat_min, lat_max, lon_min, lon_max = bornes(villes)
print(f"Latitude : {lat_min} à {lat_max}")
print(f"Longitude : {lon_min} à {lon_max}")


def distance(p1, p2):
    """Distance euclidienne entre deux points (latitude, longitude)."""
    return math.dist(p1, p2)


print("\nQuestion 4")
print(f"{distance((-18.88, 47.51), (-18.15, 49.40)):.2f} degrés")

print("\nQuestion 5")
distances = {}
for i, (nom1, lat1, lon1) in enumerate(villes):
    for nom2, lat2, lon2 in villes[i + 1:]:
        distances[(nom1, nom2)] = distance((lat1, lon1), (lat2, lon2))

for (nom1, nom2), d in distances.items():
    print(f"{nom1} - {nom2} : {d:.2f}")
print(f"Nombre de paires : {len(distances)}")

print("\nQuestion 6")
try:
    villes[0][1] = -19.00
except TypeError as erreur:
    print(f"Erreur interceptée : {erreur}")
    print("Un tuple est non modifiable : on crée un nouveau tuple à la place.")

villes_corrigees = villes.copy()
nom, _, longitude = villes_corrigees[0]
villes_corrigees[0] = (nom, -19.00, longitude)
print(villes_corrigees[0])

Ville = namedtuple("Ville", ["nom", "latitude", "longitude"])


def haversine(v1, v2):
    """Distance réelle en kilomètres entre deux villes."""
    rayon = 6371
    phi1, phi2 = math.radians(v1.latitude), math.radians(v2.latitude)
    dphi = phi2 - phi1
    dlambda = math.radians(v2.longitude - v1.longitude)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * rayon * math.asin(math.sqrt(a))


print("\nBonus")
villes_nt = [Ville(*v) for v in villes]
print(f"{villes_nt[0].nom} - {villes_nt[1].nom} : {haversine(villes_nt[0], villes_nt[1]):.0f} km")
