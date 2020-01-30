# Tim Bot 2000
Bot permettant de gérer les equipes du serveur controliste<br>
Les différentes team sont listée dans roles.json<br>

## Commandes
<b>!ping </b>: Pong!<br>
<b>!help \<commande\></b>: Affiche de l'aide<br>
<b>!list \<team\></b>: Affiche les team et le nombre de membre. Maintenant ordonné! Si une team est donnée en argument, affiche la liste des membres de ladite team<br>
<b>!rejoin \<membre\> </b>: Permet de faire rejoindre <membre> dans sa propre team. Ne marche que si l'auteur de la commande est dans une team et si l'invité n'en a pas<br>
<b>!degage \<membre\> </b>: Permet de kick quelquun de sa propre team (marche sur soi meme). Ne marche que si l'auteur et le kické sont de la meme team<br>
<b>!limit </b>: Affiche les différentes limites<br>
<b>!score </b>: Affiche le score actuel de chaque equipe<br>

## Système de score
Chaque message d'un membre donne 1 point au score de son équipe. Une mesure anti spam a été mise en place, donc pas la peine de spam comme un bourrin. Les messages du bot sont ignorés.<br>
Des backups sont fait automatiquement toute les demi heure quand un message est envoyé
## En cours de développement
- Une commande qui affiche le changelog
