### INTERFEJS UZYTKOWNIKA ###
def userUI():

    print("=== Preferencje użytkownika ===")
    preferred_length = float(input("Maksymalna długość trasy (km): "))
    preferred_terrain = input("Preferowany typ terenu (np. mountain, lakeside, forest): ").strip().lower()
    preferred_difficulty = int(input("Maksymalny poziom trudności (1 = łatwy, 3 = trudny): "))

  