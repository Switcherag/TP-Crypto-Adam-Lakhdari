## TP Secure chat Adam Lakhdari
# Prise en main

1.  Comment s'appelle cette topologie ?
    La topologie du chat semble être sous forme d'étoile. En effet, à chaque envoi de message par un client, le serveur le récupère et le renvoie vers les autres clients connectés au serveur.

2.  Que remarquez-vous dans les logs ?
    Chaque message envoyé par le client est d'abord reçu par le serveur puis renvoyé vers les autres clients.

3.  Pourquoi est-ce un problème et quel principe cela viole-t-il ?

    Confidentialité : les messages sont envoyés à tous les utilisateurs à chaque fois et le serveur a accès aux messages en clair.
    Disponibilité : le serveur représente un unique point de défaillance ; en effet, si ce dernier ne fonctionne plus, les communications sont impossibles.

4.  Quelle solution la plus simple pouvez-vous mettre en place pour éviter cela ? Détaillez votre réponse.
    Pour pallier le problème de confidentialité, on peut utiliser un chiffrement des messages avant l'envoi ainsi qu'un déchiffrement au moment de la réception.

# Chiffrement

5.  Est-ce que urandom est un bon choix pour de la cryptographie ? Pourquoi ?
    Tout d'abord, la fonction os.urandom() a été créée spécialement pour la cryptographie. En effet, c'est un bon choix pour la cryptographie d'une petite application car, se basant sur l'entropie, elle génère un nombre aléatoire plus intéressant que la fonction random(). Cependant, dans une application plus importante et à risque, il peut être nécessaire d'utiliser un générateur plus complexe.

6.  Pourquoi utiliser ces primitives cryptographiques peut-il être dangereux ?
    Utiliser ces primitives cryptographiques peut représenter un danger car elles doivent être utilisées correctement. En effet, une erreur d'implémentation provoquera une vulnérabilité dans le système. L'utilisation de bibliothèques pré-conçues permet de limiter ces problèmes d'implémentation.

7.  Pourquoi malgré le chiffrement, un serveur malveillant peut-il encore nous nuire ?
    Le chiffrement permet une protection des données par rapport aux utilisateurs  cependant un serveur malveillant pourrait modifier ou enregistrer les données pour un usage malveillant.

8.  Quelle propriété manque-t-il ici ?
    La propriété manquante est l'intégrité. En effet, le message pourrait être modifié entre les différents utilisateurs durant le transfert par le serveur. En utilisant une authentification du message, on pourrait ainsi assurer son intégrité.

# Authenticated Symmetric Encryption

9.  Pourquoi Fernet est moins risqué que le précédent chapitre en termes d'implémentation ?
    Comme explicité précédemment, il est nécessaire d'ajouter une authentification des messages. HMAC, qui est utilisé par le module Fernet, permet cela. Avec cette authentification, l'intégrité est conservée.

10. Un serveur malveillant peut néanmoins attaquer avec des faux messages déjà utilisés dans le passé. Comment appelle-t-on cette attaque ?
    Ce type d'attaque s'appelle l'attaque par rejeu.