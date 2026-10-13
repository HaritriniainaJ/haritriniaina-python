"""TP 1 - Les notes d'une classe (listes, découpage, compréhensions, sorted)."""

notes = [12, 8, 15, 17, 9, 11, 14, 6, 13, 16]

print("Question 1")
print(f"Nombre de notes : {len(notes)}")
print(f"Moyenne : {sum(notes) / len(notes):.2f}")
print(f"Min : {min(notes)} | Max : {max(notes)}")

print("\nQuestion 2")
admis = [n for n in notes if n >= 10]
ajournes = len(notes) - len(admis)
print(admis)
print(f"{ajournes} ajournés")

print("\nQuestion 3")
print(sorted(notes))
print(sorted(notes, reverse=True)[:3])

print("\nQuestion 4")
apres_deliberation = [min(n + 2, 10) if n < 10 else n for n in notes]
print(apres_deliberation)


def histogramme(notes):
    """Affiche une étoile par note, regroupées par tranche."""
    tranches = [(0, 4), (5, 9), (10, 14), (15, 20)]
    for debut, fin in tranches:
        effectif = len([n for n in notes if debut <= n <= fin])
        print(f"{f'{debut}-{fin}':<6}| {'*' * effectif}")


print("\nQuestion 5")
histogramme(notes)


def rang(notes, note):
    """Position d'une note dans le classement décroissant (1 = meilleure)."""
    return sorted(notes, reverse=True).index(note) + 1


print("\nQuestion 6")
print(f"rang(notes, 14) = {rang(notes, 14)}")

print("\nBonus")
print(list(dict.fromkeys(notes + [15, 6, 18])))
