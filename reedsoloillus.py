#reed solo visuel

# implémentation du corps F_256 - POO

class GF256:
    def __init__(self, valeur):
        self.valeur = valeur

    def __add__(self, autre):   # on pourra ensuite utiliser +
        return GF256(self.valeur ^ autre.valeur) # addition bit par bit ou xor (^) bit par bit 

    def __sub__(self, autre):   # on pourra ensuite utiliser -
        return GF256(self.valeur ^ autre.valeur)

    def __mul__(self, autre):  # on pourra ensuite utiliser *
        # Multiplication dans GF(256)
        p = 0
        for i in range(8):
            if autre.valeur & (1 << i): # 
                p ^= self.valeur << i
        # Réduction modulo par le polynôme irréductible x^8 + x^4 + x^3 + x + 1
        for i in range(8, 15):
            p ^= ((p >> 8) & 1) * 0x11D
        return GF256(p & 0xFF)


    def __truediv__(self, autre):
        # La division est la multiplication par l'inverse
        return self * autre.inverse()

    def inverse(self):
        # Utiliser l'algorithme d'Euclide étendu pour trouver l'inverse
        # Ceci est un espace réservé ; l'implémentation réelle est requise
        pass

    def __eq__(self, autre):
        return self.valeur == autre.valeur

    def __repr__(self):
        return f"GF256({self.valeur})"
    
    def representation_en_bits(self):
        # Convertir la valeur en une chaîne de bits
        return bin(self.valeur)[2:].zfill(8)
    
a=GF256(5)
b=GF256(3)
c = a * b 
print(a)
#print(__repr__(c))

class ReedSolomon:
    def __init__(self, k, n):
        self.k = k  # Nombre de symboles de données
        self.n = n  # Nombre total de symboles (k données + n-k redondance)
        self.t = (n - k) // 2  # Nombre d'erreurs correctibles
        self.gf = GF256  # Supposons que la classe GF256 est définie comme avant

    def encoder(self, message):
        # Convertir le message en coefficients de polynôme
        poly = [self.gf(m) for m in message]

        # Évaluer le polynôme à des points pour obtenir les symboles de redondance
        redondance = []
        for i in range(self.k, self.n):
            x = self.gf(i)
            y = self.gf(0)
            for coeff in reversed(poly):
                y = y * x + coeff
            redondance.append(y.valeur)

        # Retourner le message encodé (données + redondance)
        return message + redondance

    def calculer_syndrome(self, recu):
        syndrome = []
        for i in range(1, 2 * self.t + 1):
            s = self.gf(0)
            for j, val in enumerate(recu):
                s += self.gf(val) * (self.gf(i) ** j)
            syndrome.append(s.valeur)
        return syndrome

    def berlekamp_massey(self, syndrome):
        # Espace réservé pour l'algorithme de Berlekamp-Massey
        # Implémenter l'algorithme pour trouver le polynôme localisateur d'erreurs
        pass

    def forney(self, localisateur_erreur, syndrome):
        # Espace réservé pour l'algorithme de Forney
        # Implémenter l'algorithme pour trouver les valeurs des erreurs
        pass

    def decoder(self, message_encodé):
        syndrome = self.calculer_syndrome(message_encodé)
        if all(s == 0 for s in syndrome):
            return message_encodé[:self.k]  # Aucune erreur

        localisateur_erreur = self.berlekamp_massey(syndrome)
        valeurs_erreur = self.forney(localisateur_erreur, syndrome)

        # Corriger les erreurs
        message_corrigé = message_encodé.copy()
        for pos, val in valeurs_erreur:
            message_corrigé[pos] ^= val

        return message_corrigé[:self.k]
