Ce projet est une implémentation en Python des codes correcteurs d'erreurs Reed-Solomon sur F_256.

## Usage

1. Implémenter le corps à 256 éléments et les codes de ReedSolomon
2. Encoder un message
3. Introduire éventuellement des erreurs
4. Décoder le message pour corriger les erreurs

## Exemple

```python
rs = ReedSolomon(k=8, n=12)
message = [1,2,3,4,5,6,7,8]
code = rs.encoder(message)
