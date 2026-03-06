#reed solo visuel

# implémentation du corps F_256 - POO

class GF256:
    def __init__(self, valeur):
        self.valeur = valeur

    def __add__(self, autre):   # on pourra ensuite utiliser +
        return GF256(self.valeur ^ autre.valeur) # addition bit par bit ou xor (^) bit par bit 

    def __sub__(self, autre):   # on pourra ensuite utiliser -
        return GF256(self.valeur ^ autre.valeur)

    
    def __mul__(self, autre):
        a = self.valeur
        b = autre.valeur
        p = 0

        for _ in range(8):
            if b & 1:
                p ^= a

            carry = a & 0x80  # bit de poids fort
            a <<= 1

            if carry:
                a ^= 0x11D  # réduction modulo le polynôme irréductible

            a &= 0xFF  # garder 8 bits
            b >>= 1

        return GF256(p)
    
    
    def __pow__(self, puissance):
        res = GF256(1)
        base = GF256(self.valeur)
        while puissance > 0:
            if puissance & 1:
                res = res * base
            base = base * base
            puissance >>= 1
        return res

    def inverse(self):
        return self**254  # On utilise la relation self**255=1 dans le groupe multiplicatif (F_256)* (Lagrange)

    def __truediv__(self, autre):
        # La division est la multiplication par l'inverse
        return self * autre.inverse()

    def __eq__(self, autre):
        return self.valeur == autre.valeur

    def __repr__(self):
        return f"GF256({self.valeur})"
    
    def representation_en_bits(self):
        # Convertir la valeur en une chaîne de bits
        return bin(self.valeur)[2:].zfill(8)
    


alpha = GF256(2)   # générateur 

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
    
    def poly_add(self, p, q):
        max_len = max(len(p), len(q))
        res = [GF256(0)] * max_len
        for i in range(len(p)):
            res[i + max_len - len(p)] += p[i]
        for i in range(len(q)):
            res[i + max_len - len(q)] += q[i]
        return res
    
    def polymul(self, p, q):
        res = [GF256(0)] * (len(p) + len(q) - 1)
        for i in range(len(p)):
            for j in range(len(q)):
                res[i + j] += p[i] * q[j]
        return res
    
    def poly_eval(self, p, x):
        res = GF256(0)
        for c in p:
            res = res * x + c
        return res
    
    def derivee_polynome(self, p):
        deg_max = len(p) - 1
        return [p[i] for i in range(deg_max) if (deg_max - i) % 2 == 1] # on est en caractéristique 2

    def calculer_syndrome(self, recu):
        syndrome = []
        for i in range(1, 2 * self.t + 1):
            s = self.gf(0)
            for j, val in enumerate(recu):
                s += self.gf(val) * (self.gf(i) ** j)
            syndrome.append(s.valeur)
        return syndrome

    def berlekamp_massey(self, syndrome): # Trouve le polynoôme localisateur d'erreurs
        n = len(syndrome)
        C = [self.gf(1)] + [self.gf(0)] * n
        B = [self.gf(1)] + [self.gf(0)] * n

        L = 0
        m = -1
        b = self.gf(1)

        for i in range(n):
            # Calcul du delta
            delta = self.gf(syndrome[i])
            for j in range(1, L + 1):
                delta += C[j] * self.gf(syndrome[i - j])

            if delta != self.gf(0):
                T = C.copy()
                facteur = delta / b

                for j in range(i - m, n):
                    if j < len(B):
                        C[j] -= facteur * B[j - (i - m)]

                if 2 * L <= i:
                    L = i + 1 - L
                    B = T
                    b = delta
                    m = i

        return C[:L + 1]
    
    def trouver_positions_erreurs(self, locator, n):
        pos = []
        for i in range(n):
            x = alpha ** i
            if self.poly_eval(locator, x) == GF256(0):
                pos.append(n - 1 - i)
        #if len(pos) != len(locator) - 1:
          #  raise ValueError("Racines incorrectes.")
        return pos
    
    def calculer_valeurs_erreurs(self, pos, locator, syndromes): #implémentation de l'algo de Forney
        omega = self.polymul(locator, [self.gf(s) for s in reversed(syndromes)])[-(len(locator)-1):] # on prend les t premiers coefficients de omega
        derivee = self.derivee_polynome(locator)

        valeurs = []
        for i in pos:
            x_inv = alpha ** (255 - i)
            num = self.poly_eval(omega, x_inv)
            den = self.poly_eval(derivee, x_inv)
            valeurs.append(num / den)

        return valeurs


    
    def decoder(self, mot):     #décodage final
        synd = self.calculer_syndrome(mot)

        if all(s == 0 for s in synd):
            return mot[:self.k]

        locator = self.berlekamp_massey(synd)
        pos = self.trouver_positions_erreurs(locator, len(mot))
        val = self.calculer_valeurs_erreurs(pos, locator, synd)

        mot_corrige = list(mot)
        for p, v in zip(pos, val):
            mot_corrige[p] ^= v.valeur

        return mot_corrige[:self.k]

