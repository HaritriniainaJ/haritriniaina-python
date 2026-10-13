"""TP 4 - Atelier décorateurs (fermetures, @wraps, décorateurs avec paramètre)."""
import time
from functools import wraps, lru_cache


def chronometrer_simple(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        debut = time.perf_counter()
        resultat = fonction(*args, **kwargs)
        duree = time.perf_counter() - debut
        print(f"{fonction.__name__} a pris {duree:.2f} s")
        return resultat
    return enveloppe


@chronometrer_simple
def lente():
    time.sleep(1)


print("Question 1")
lente()


def majuscules(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        return fonction(*args, **kwargs).upper()
    return enveloppe


@majuscules
def dire_bonjour():
    return "bonjour"


print("\nQuestion 2")
print(dire_bonjour())


def compter_appels(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        enveloppe.appels += 1
        return fonction(*args, **kwargs)
    enveloppe.appels = 0
    return enveloppe


@compter_appels
def saluer():
    return "salut"


print("\nQuestion 3")
saluer()
saluer()
saluer()
print(f"Nombre d'appels : {saluer.appels}")


def verifier_positifs(fonction):
    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        for valeur in list(args) + list(kwargs.values()):
            if isinstance(valeur, (int, float)) and valeur < 0:
                raise ValueError(f"Argument négatif refusé : {valeur}")
        return fonction(*args, **kwargs)
    return enveloppe


@verifier_positifs
def surface(longueur, largeur):
    return longueur * largeur


print("\nQuestion 4")
print(surface(4, 5))
try:
    surface(-4, 5)
except ValueError as erreur:
    print(f"Erreur : {erreur}")


def chronometrer(unite="s"):
    def decorateur(fonction):
        @wraps(fonction)
        def enveloppe(*args, **kwargs):
            debut = time.perf_counter()
            resultat = fonction(*args, **kwargs)
            duree = time.perf_counter() - debut
            if unite == "ms":
                print(f"{fonction.__name__} a pris {duree * 1000:.0f} ms")
            else:
                print(f"{fonction.__name__} a pris {duree:.2f} s")
            return resultat
        return enveloppe
    return decorateur


@chronometrer(unite="ms")
def pause_courte():
    time.sleep(0.25)


print("\nQuestion 5")
pause_courte()


def memoriser(fonction):
    cache = {}

    @wraps(fonction)
    def enveloppe(*args, **kwargs):
        cle = args + tuple(sorted(kwargs.items()))
        if cle not in cache:
            cache[cle] = fonction(*args, **kwargs)
        return cache[cle]
    return enveloppe


def fibonacci_brut(n):
    if n < 2:
        return n
    return fibonacci_brut(n - 1) + fibonacci_brut(n - 2)


@memoriser
def fibonacci_memo(n):
    if n < 2:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


@chronometrer(unite="ms")
def lancer(fonction, n):
    return fonction(n)


print("\nQuestion 6")
print("Sans mémoïsation :")
print(lancer(fibonacci_brut, 30))
print("Avec @memoriser :")
print(lancer(fibonacci_memo, 30))
print("Avec @lru_cache :")
print(lancer(fibonacci_lru, 30))


@chronometrer()
@compter_appels
def ordre_1():
    return "ok"


@compter_appels
@chronometrer()
def ordre_2():
    return "ok"


print("\nQuestion 7")
ordre_1()
ordre_1()
ordre_2()
ordre_2()
print(f"Ordre 1 (chronometrer au-dessus) : appels = {ordre_1.appels}")
print(f"Ordre 2 (compter_appels au-dessus) : appels = {ordre_2.appels}")


class MiniFlask:
    def __init__(self):
        self.routes = {}
        self.gestionnaire_404 = None

    def route(self, chemin):
        def enregistrer(fonction):
            if chemin in self.routes:
                raise ValueError(f"La route {chemin} est déjà enregistrée")
            self.routes[chemin] = fonction
            return fonction
        return enregistrer

    def erreur_404(self, fonction):
        self.gestionnaire_404 = fonction
        return fonction

    def lister_routes(self):
        for chemin in self.routes:
            print(chemin)

    def traiter(self, chemin):
        fonction = self.routes.get(chemin)
        if fonction:
            return fonction()
        if self.gestionnaire_404:
            return self.gestionnaire_404()
        return "404 : page introuvable"


app = MiniFlask()


@app.route("/")
def accueil():
    return "Bonjour !"


@app.route("/contact")
def contact():
    return "Contactez-nous"


@app.erreur_404
def page_perdue():
    return "Oups, cette page n'existe pas"


print("\nQuestion 8")
app.lister_routes()
print(app.traiter("/"))
print(app.traiter("/inconnue"))
try:
    @app.route("/")
    def doublon():
        return "doublon"
except ValueError as erreur:
    print(f"Erreur : {erreur}")
