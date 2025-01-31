# 📸 Discord Image Logger [ARCHIVÉ]

**Ce projet a été archivé !** Une version V2 avec des corrections de bugs, des capacités d'auto-hébergement, une meilleure plateforme d'hébergement et d'autres fonctionnalités sera bientôt disponible !

**Discord Image Logger** est un outil simple mais puissant que j'ai créé pour faciliter le clic des gens sur les liens. Vous pouvez amener une personne à visiter à peu près n'importe quel site en utilisant cette astuce, et tout ce que vous avez à faire est de lui envoyer une image ! Il comprend également un enregistreur IP intégré avec des informations détaillées sur l'utilisateur.

Veuillez noter qu'il ne s'agit **PAS** d'un enregistreur d'images « en un clic ». Il existe une arnaque très populaire dans laquelle les gens prétendent pouvoir créer une image qui volera tous vos jetons, mots de passe et plus encore (en gros une RCE d'image) simplement en cliquant sur une image. Cependant, ils sont tous **faux**, et je vous déconseille d'exécuter les fichiers EXE que vous trouvez dans ces référentiels ou d'acheter quoi que ce soit à qui que ce soit.

**Si vous envisagez de forker ce dépôt, ajoutez-le aussi en guise d'étoile tant que vous y êtes !**

Vous êtes bloqué ? Essayez le [Tutoriel vidéo !](https://www.youtube.com/watch?v=rFbiW2x4HEw) <br>
Pour les mises à jour et les événements, vous devriez rejoindre le [Discord !](https://discord.gg/Shb47XpQxq)

# 📚 Table des matières
* [Introduction](#-discord-image-logger) <br>
* [Fonctionnalités](#-features) <br>
* [Configuration](#-configuration) <br>
* [Configuration](#%EF%B8%8F-setup) <br>
* [Tutoriel vidéo](https://www.youtube.com/watch?v=rFbiW2x4HEw) <br>
* [Rapports de bugs et suggestions](#-bug-reports--suggestions) <br>
* [Déclarations de clôture](#-closing-statements) <br>

---

# 💎 Fonctionnalités
* Rapide, gratuit et facile !
* 100 % intraçable et anonyme !
* Il suffit de cliquer sur « Ouvrir l'original » !
* Vole autant que possible, y compris votre adresse postale via GPS !
* ~~En cours de développement actif, de nombreuses nouvelles fonctionnalités seront ajoutées !~~ Pas tant que ça, mais une nouvelle version sera bientôt en cours de développement ! Donnez-nous vos idées !

---

# 🔧 Configuration

Avant de le configurer, modifions la **config.** <br>
Ouvrez `main.py` et modifiez les valeurs, reportez-vous à la clé ci-dessous.

**WEBHOOK :** `Votre webhook Discord !` <br>
**IMAGE :** `Un LIEN vers l'image souhaitée.` <br>
**IMAGEARGUMENT :** `Activer la lecture d'image à partir de l'argument. (Voir Annotation #1)` <br>
**USERNAME :** `Le nom d'utilisateur du bot qui envoie` <br>
**COLOR :** `La couleur de la barre latérale de l'intégration` <br>
**DOCRASHBROWSER :** `Faire planter le navigateur de l'utilisateur` <br>
**DOMESSE :** `Afficher un message personnalisé lorsqu'il clique ?` <br>
**MESSAGE :** `Le message à afficher.` <br>
**RICHMESSAGE :** `Activer un message enrichi, qui permet d'insérer des variables. (Voir l'annotation n°2)` <br>
**VPNCHECK :** `Empêcher les VPN de spammer votre webhook !` <br>
**LINKALERTS :** `Vous avertir lorsque quelqu'un envoie un lien de journalisation d'image` <br>
**BUGGEDIMAGE :** `Afficher une image de chargement sur Discord` <br>
**ANTIBOT :** `Empêcher les robots de spammer votre webhook !` <br>
**REDIRECT :** `Rediriger l'utilisateur ?` <br>
**PAGE :** `Page vers laquelle rediriger, si oui` <br>

**ANNOTATIONS :**
* **1)** `IMAGEARGUMENT`
Lorsqu'il est activé, cela vous permettra de fournir un argument dans l'URL en tant qu'image. <br>
Vous pouvez le faire en codant un lien en Base64 sécurisé par URL et en le fournissant comme argument `URL` ou `ID`. <br>
EXEMPLE : `https://your.epic.image.logger/api/main?url=aHR0cHM6Ly8...` <br>
Le Base64 ci-dessus est coupé court, mais il conduirait à l'URL d'une image. <br>
S'il est activé et qu'aucun argument `URL` ou `ID` n'est fourni, celui configuré par défaut sera utilisé.

* **2)** `RICHMESSAGE`
Rich Message vous permet d'insérer des variables telles que l'IP du client, l'emplacement, l'ASN, etc. pour le message Crashbrowser. <br>
Insérez simplement n'importe quoi dans le tableau suivant et il le remplacera respectivement. <br>

| Valeurs |
|--------|
| `{ip}` Leur adresse IP. |
| `{isp}` Leur FAI (fournisseur d'accès Internet) |
| `{asn}` Leur ASN (numéro de système autonome) |
| `{country}` Le pays dans lequel l'IP est située. |
| `{region}` La région dans laquelle l'IP est située. |
| `{city}` La ville dans laquelle l'IP est située. |
| `{lat}` La latitude de l'IP. |
| `{long}` La longitude de l'IP. |
| `{timezone}` Le fuseau horaire de l'IP. |
| `{mobile}` S'il s'agit d'une connexion mobile. |
| `{vpn}` Si l'IP appartient à un VPN/Proxy. |
| `{bot}` Si l'IP est un robot. |
| `{browser}` Le navigateur du client. |
| `{os}` Le système d'exploitation du client. |

---

# ⚒️ Configuration

Maintenant que vous avez tout configuré, installons cette chose ! <br>

Vous pouvez également regarder le [tutoriel vidéo !](https://www.youtube.com/watch?v=rFbiW2x4HEw)

- **1 :** Créez un dépôt GitHub. Je recommande qu'il soit privé, afin que les autres ne puissent pas voir l'URL de votre webhook.
- **2 :** Créez un dossier nommé `api` et placez-y `requirements.txt` et `main.py` (renommez-le comme vous le souhaitez, par exemple catpicture.py ferait de l'URL votre.site/api/catepicture)
- **3 :** (Facultatif) créez un fichier dans la racine principale (PAS DANS L'API) nommé `index.html` et placez-y le code ci-dessous :
```html
<meta http-equiv="refresh" content="0;url=./api/main.py">
```
(Vous pouvez remplacer main.py par ce que vous avez créé !); Le but de cette étape est que vous puissiez simplement visiter votre.site et non votre.site/api/main (le premier semble beaucoup moins suspect) cependant
