import asyncio, json, os, time, uuid, random, string, hashlib, hmac, warnings, socket
from datetime import datetime, timezone
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# ═══════════════ SYSTEM CONFIG ═══════════════
# Credit: @Prime_Leader69
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

JSON_FILE = "accounts.json"
TXT_FILE  = "Acc_level.txt"

MSDK_APP_VER  = "1.132.9"
MSDK_VER_CODE = "2024010012"
MSDK_UA = f"GarenaMSDK/4.0.42(NX809J ;Android 9;en;US;app {MSDK_APP_VER} {MSDK_VER_CODE};)"
HKEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

xK = b'Yg&tc%DEuh6%Zc^8'
xV = b'6oyZDr22E3ychjM%'

RELEASE_VERSION = "OB55"
UNITY_VERSION   = "2018.4.12f1"
CLIENT_VERSION  = "1.132.9"

BIO_TEXT = "Ｂ Ａ Ｓ Ａ Ｎ Ｔ Ａ Ｆ Ｆ Ｌ Ｉ Ｋ Ｅ Ｓ"

# ═══════════════ ALL REGIONS / SERVERS ═══════════════
REGIONS = {
    "BD": {
        "name": "Bangladesh",
        "oauth_register": "https://ffmconnect.ppmainecoonghj.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://ffmconnect.ppmainecoonghj.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ppmainecoonghj.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "bn", "choose_code": "BD",
        "cities": [("Tangail","C"),("Dhaka","C"),("Chittagong","B"),("Sylhet","E"),
                   ("Rajshahi","D"),("Khulna","A"),("Gazipur","C")],
        "isps":    ["TelKila","Grameenphone","Robi","Banglalink","Carnival","Link3","Dot Internet"],
        "ip_subnets": ["103.157","103.205","27.147","118.179","182.160","43.224"],
    },
    "IND": {
        "name": "India",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "client.ind.freefiremobile.com",
        "gateway": "IND", "lang": "hi", "choose_code": "IND",
        "cities": [("Mumbai","MH"),("New Delhi","DL"),("Bangalore","KA"),
                   ("Kolkata","WB"),("Chennai","TN"),("Hyderabad","TS"),("Pune","MH")],
        "isps":    ["Jio 5G","Airtel","Vi India","BSNL Broadband","ACT Fibernet","Tata Play Fiber"],
        "ip_subnets": ["49.36","49.32","27.59","106.193","115.99","122.161","157.34"],
    },
    "PK": {
        "name": "Pakistan",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "ur", "choose_code": "PK",
        "cities": [("Karachi","SD"),("Lahore","PB"),("Islamabad","IS"),
                   ("Rawalpindi","PB"),("Faisalabad","PB"),("Peshawar","KP")],
        "isps":    ["Jazz","Zong 4G","Telenor PK","PTCL Broadband","Nayatel","Ufone"],
        "ip_subnets": ["39.40","39.50","111.68","182.180","119.160"],
    },
    "SG": {
        "name": "Singapore & Malaysia",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "en", "choose_code": "SG",
        "cities": [("Singapore","SG"),("Kuala Lumpur","14"),("Johor Bahru","01"),("Penang","07")],
        "isps":    ["Singtel","StarHub Mobile","M1 Limited","MyRepublic","Maxis","Unifi"],
        "ip_subnets": ["116.86","118.189","175.156","219.74","115.66"],
    },
    "ID": {
        "name": "Indonesia",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "id", "choose_code": "ID",
        "cities": [("Jakarta","JK"),("Surabaya","JI"),("Bandung","JB"),
                   ("Medan","SU"),("Semarang","JT"),("Makassar","SN")],
        "isps":    ["Telkomsel","Indosat Ooredoo","XL Axiata","Smartfren","Biznet Networks"],
        "ip_subnets": ["114.124","180.252","125.160","36.68","110.138"],
    },
    "VN": {
        "name": "Vietnam",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "vi", "choose_code": "VN",
        "cities": [("Hanoi","HN"),("Ho Chi Minh City","SG"),("Da Nang","DN"),("Hai Phong","HP")],
        "isps":    ["Viettel","VNPT","FPT Telecom","MobiFone"],
        "ip_subnets": ["14.160","113.160","171.224","123.16"],
    },
    "BR": {
        "name": "Brazil",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "client.us.freefiremobile.com",
        "gateway": "SG", "lang": "pt", "choose_code": "BR",
        "cities": [("Sao Paulo","SP"),("Rio de Janeiro","RJ"),("Belo Horizonte","MG"),("Curitiba","PR")],
        "isps":    ["Vivo Fibra","Claro Brasil","TIM Brasil","Oi Fibra"],
        "ip_subnets": ["177.18","179.184","189.100","191.178"],
    },
    "NA": {
        "name": "North America",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "client.us.freefiremobile.com",
        "gateway": "US", "lang": "en", "choose_code": "US",
        "cities": [("New York","NY"),("Los Angeles","CA"),("Dallas","TX"),("Chicago","IL"),("Miami","FL")],
        "isps":    ["AT&T Internet","Verizon Fios","T-Mobile USA","Comcast Xfinity"],
        "ip_subnets": ["98.240","172.58","68.192","73.180"],
    },
    "ME": {
        "name": "Middle East",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "ar", "choose_code": "ME",
        "cities": [("Riyadh","01"),("Dubai","DU"),("Cairo","C"),("Casablanca","CAS"),("Jeddah","02")],
        "isps":    ["STC","Etisalat","Zain KSA","Orange Egypt","du Telecom"],
        "ip_subnets": ["188.48","94.200","197.32","196.200","82.178"],
    },
    "TH": {
        "name": "Thailand",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "th", "choose_code": "TH",
        "cities": [("Bangkok","10"),("Chiang Mai","50"),("Phuket","83"),("Chonburi","20")],
        "isps":    ["AIS","TrueMove H","dtac","3BB Broadband","NT Broadband"],
        "ip_subnets": ["49.228","171.96","58.8","182.52","1.46"],
    },
    "TW": {
        "name": "Taiwan",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "zh-TW", "choose_code": "TW",
        "cities": [("Taipei","TPE"),("Kaohsiung","KHH"),("Taichung","TXG"),("Tainan","TNN")],
        "isps":    ["Chunghwa Telecom","Taiwan Mobile","FarEasTone","Taiwan Broadband"],
        "ip_subnets": ["114.32","211.20","61.216","220.130","1.160"],
    },
    "EU": {
        "name": "Europe",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "en", "choose_code": "EU",
        "cities": [("Frankfurt","HE"),("Paris","IDF"),("London","ENG"),("Madrid","MD"),("Berlin","BE")],
        "isps":    ["Deutsche Telekom","Vodafone","Orange","Telefonica","BT Broadband"],
        "ip_subnets": ["80.187","82.64","92.207","88.16","212.186"],
    },
    "SAC": {
        "name": "South America",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "client.us.freefiremobile.com",
        "gateway": "SG", "lang": "es", "choose_code": "SAC",
        "cities": [("Buenos Aires","B"),("Santiago","RM"),("Bogota","DC"),("Lima","LMA"),("Medellin","ANT")],
        "isps":    ["Claro","Movistar","Tigo","Entel","Telecom Argentina"],
        "ip_subnets": ["181.44","190.11","200.89","186.104","190.232"],
    },
    "CIS": {
        "name": "Russia & CIS",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "ru", "choose_code": "RU",
        "cities": [("Moscow","MOW"),("Saint Petersburg","SPE"),("Novosibirsk","NVS"),("Yekaterinburg","SVE")],
        "isps":    ["Rostelecom","MTS","Beeline","MegaFon","Dom.ru"],
        "ip_subnets": ["178.62","188.162","213.87","95.153","94.25"],
    },
    "RU": {
        "name": "Russia",
        "oauth_register": "https://connect.garena.com/api/v2/oauth/guest:register",
        "oauth_token":    "https://connect.garena.com/api/v2/oauth/guest/token:grant",
        "login_host":     "loginbp.ggblueshark.com",
        "client_host":    "clientbp.ppmainecoonghj.com",
        "gateway": "SG", "lang": "ru", "choose_code": "RU",
        "cities": [("Moscow","MOW"),("Saint Petersburg","SPE"),("Novosibirsk","NVS"),("Kazan","TA")],
        "isps":    ["Rostelecom","MTS","Beeline","MegaFon","Dom.ru"],
        "ip_subnets": ["178.62","188.162","213.87","95.153","94.25"],
    },
}

REGION_MENU = [
    ("01","BD","Bangladesh"),    ("02","IND","India"),
    ("03","PK","Pakistan"),      ("04","SG","Singapore"),
    ("05","ID","Indonesia"),     ("06","VN","Vietnam"),
    ("07","BR","Brazil"),        ("08","NA","North America"),
    ("09","ME","Middle East"),   ("10","TH","Thailand"),
    ("11","TW","Taiwan"),        ("12","EU","Europe"),
    ("13","SAC","South America"),("14","CIS","Russia/CIS"),
    ("15","RU","Russia"),        ("AU","AUTO","All regions · random"),
]
_RMAP = {
    "1":"BD","01":"BD","2":"IND","02":"IND","3":"PK","03":"PK",
    "4":"SG","04":"SG","5":"ID","05":"ID","6":"VN","06":"VN",
    "7":"BR","07":"BR","8":"NA","08":"NA","9":"ME","09":"ME",
    "10":"TH","11":"TW","12":"EU","13":"SAC","14":"CIS","15":"RU",
    "AU":"AUTO","AUTO":"AUTO",
}


# ═══════════════ PREMIUM UI & COLORS ═══════════════
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    PURPLE  = "\033[38;5;135m"
    ORANGE  = "\033[38;5;208m"
    WHITE   = "\033[97m"
    DIM     = "\033[2m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(f"""{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ██╗     ███████╗ █████╗ ██████╗ ███████╗██████╗            ║
║  ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔══██╗           ║
║  ██║     █████╗  ███████║██║  ██║█████╗  ██████╔╝           ║
║  ██║     ██╔══╝  ██╔══██║██║  ██║██╔══╝  ██╔══██╗           ║
║  ███████╗███████╗██║  ██║██████╔╝███████╗██║  ██║           ║
║  ╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝           ║
║                                                              ║
║              👑 LEADER GEN PRO                               ║
║                                                              ║
║       ⚡ CREDIT : @Prime_Leader69                             ║
║       🌐 MULTI-SERVER  |  15 REGIONS                         ║
║       🚀 GEN + ACTIVE + BIO SETTER                            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{C.RESET}""")

def show_region_menu():
    print(f"{C.CYAN}{C.BOLD}╔══ SELECT REGION ══════════════════════════════════╗{C.RESET}")
    half = (len(REGION_MENU) + 1) // 2
    for i in range(half):
        num1, code1, name1 = REGION_MENU[i]
        row = f"  {C.DIM}{num1}{C.RESET}  {C.CYAN}{C.BOLD}{code1:<6}{C.RESET}{C.WHITE}{name1:<20}{C.RESET}"
        if i + half < len(REGION_MENU):
            num2, code2, name2 = REGION_MENU[i + half]
            row += f"  {C.DIM}{num2}{C.RESET}  {C.CYAN}{C.BOLD}{code2:<6}{C.RESET}{C.WHITE}{name2}{C.RESET}"
        print(row)
    print(f"{C.CYAN}{C.BOLD}╚═══════════════════════════════════════════════════╝{C.RESET}")


# ═══════════════ FILE LOCK & SAVE SYSTEM ═══════════════
file_lock = asyncio.Lock()

async def _save_safe(acc_data):
    async with file_lock:
        try:
            existing = []
            if os.path.exists(JSON_FILE):
                try:
                    with open(JSON_FILE, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                except Exception:
                    existing = []
            existing.append(acc_data)
            tmp = JSON_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2, ensure_ascii=False)
            if os.path.exists(JSON_FILE):
                os.remove(JSON_FILE)
            os.replace(tmp, JSON_FILE)
            with open(TXT_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"UID: {acc_data['uid']} | PASS: {acc_data['password']} | "
                    f"ACC_ID: {acc_data['account_id']} | NAME: {acc_data['name']} | "
                    f"REGION: {acc_data['region']} | ONLINE: {acc_data['online_status']} | "
                    f"BIO: {acc_data['bio_status']}\n"
                )
        except Exception:
            pass


# ═══════════════ CRYPTO & PROTOBUF HELPERS ═══════════════
def _gen_sig(payload: str) -> str:
    return hmac.new(HKEY.encode(), payload.encode(), hashlib.sha256).hexdigest()

def _aes_encrypt(data: bytes) -> bytes:
    return AES.new(xK, AES.MODE_CBC, xV).encrypt(pad(data, 16))

def EnV_VaRiAnT(n):
    d = []
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        d.append(b)
        if not n: break
    return bytes(d)

def ProToBuF(Fields):
    p = bytearray()
    for f, v in Fields.items():
        if isinstance(v, bool):
            p.extend(EnV_VaRiAnT((f << 3) | 0)); p.extend(EnV_VaRiAnT(1 if v else 0))
        elif isinstance(v, int):
            p.extend(EnV_VaRiAnT((f << 3) | 0)); p.extend(EnV_VaRiAnT(v))
        elif isinstance(v, str):
            d = v.encode()
            p.extend(EnV_VaRiAnT((f << 3) | 2)); p.extend(EnV_VaRiAnT(len(d))); p.extend(d)
        elif isinstance(v, (bytes, bytearray)):
            d = bytes(v)
            p.extend(EnV_VaRiAnT((f << 3) | 2)); p.extend(EnV_VaRiAnT(len(d))); p.extend(d)
    return bytes(p)

def _proto(fields: dict) -> bytes:
    out = bytearray()
    for f, v in fields.items():
        if isinstance(v, int): out += EnV_VaRiAnT((f << 3) | 0) + EnV_VaRiAnT(v)
        elif isinstance(v, (str, bytes)):
            b = v.encode() if isinstance(v, str) else v
            out += EnV_VaRiAnT((f << 3) | 2) + EnV_VaRiAnT(len(b)) + b
        elif isinstance(v, dict):
            nested = _proto(v)
            out += EnV_VaRiAnT((f << 3) | 2) + EnV_VaRiAnT(len(nested)) + nested
    return bytes(out)

def _first_varint(data: bytes, want: int):
    off = 0
    while off < len(data):
        key = shift = 0
        while True:
            b = data[off]; off += 1
            key |= (b & 0x7F) << shift
            if not (b & 0x80): break
            shift += 7
        fn, wt = key >> 3, key & 7
        if wt == 0:
            v = shift = 0
            while True:
                b = data[off]; off += 1
                v |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
            if fn == want: return v
        elif wt == 2:
            ln = shift = 0
            while True:
                b = data[off]; off += 1
                ln |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
            off += ln
        elif wt == 1: off += 8
        elif wt == 5: off += 4
        else: break
    return None

_PW_STASH: dict = {}


# ═══════════════ GENERATORS ═══════════════
SUPERSCRIPTS = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹"]

def generate_nickname():
    length = random.choice([4, 5])
    rand_sup = "".join(random.choices(SUPERSCRIPTS, k=length))
    return f"B_FF__{rand_sup}"

def generate_password():
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    rand_str = "".join(random.choices(chars, k=26))
    return f"B_FF{rand_str}"


# ═══════════════ SERVER TIME SYNC ═══════════════
def get_server_time():
    try:
        r = requests.head("https://www.google.com", timeout=5)
        server_date = r.headers.get('Date')
        if server_date:
            dt = datetime.strptime(server_date, "%a, %d %b %Y %H:%M:%S GMT")
            server_ts = dt.replace(tzinfo=timezone.utc).timestamp()
            return int(server_ts), dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass
    return int(time.time()), time.strftime("%Y-%m-%d %H:%M:%S")


# ═══════════════ GARENA AUTH & ACTIVATION ═══════════════
def _new_session():
    s = requests.Session()
    s.verify = False
    s.headers.update({"Accept-Encoding": "gzip, deflate", "Connection": "Keep-Alive"})
    return s

def guest_register(device_id, cfg, max_retries=5):
    reg_url = cfg["oauth_register"]
    host = reg_url.split("/")[2]
    for attempt in range(max_retries):
        try:
            password = generate_password()
            body = json.dumps({"app_id": 100067, "client_type": 2,
                               "password": password, "source": 2}, separators=(',', ':'))
            headers = {
                "User-Agent": MSDK_UA, "Authorization": f"Signature {_gen_sig(body)}",
                "Accept": "application/json", "Content-Type": "application/json; charset=utf-8",
                "Host": host, "Connection": "Keep-Alive",
            }
            sess = _new_session()
            r = sess.post(reg_url, headers=headers, data=body, timeout=12)
            sess.close()
            if r.status_code == 200:
                j = r.json()
                if "data" in j and "uid" in j["data"]:
                    uid = str(j["data"]["uid"])
                    _PW_STASH[uid] = password
                    return uid, password
            time.sleep(random.uniform(0.5, 1.5) * (attempt + 1))
        except Exception:
            time.sleep(random.uniform(0.3, 1.0) * (attempt + 1))
    return None, None

def guest_token(uid, cfg, max_retries=4):
    pw = _PW_STASH.get(str(uid))
    if not pw: return None
    tok_url = cfg["oauth_token"]
    host = tok_url.split("/")[2]
    for attempt in range(max_retries):
        try:
            body = json.dumps({"client_id": 100067, "client_secret": HKEY, "client_type": 2,
                               "password": pw, "response_type": "token", "uid": int(uid)},
                              separators=(',', ':'))
            headers = {
                "User-Agent": MSDK_UA, "Accept": "application/json",
                "Content-Type": "application/json; charset=utf-8",
                "Host": host, "Connection": "Keep-Alive",
            }
            sess = _new_session()
            r = sess.post(tok_url, headers=headers, data=body, timeout=12)
            sess.close()
            if r.status_code == 200:
                j = r.json()
                if "data" in j and "access_token" in j["data"]:
                    d = j["data"]
                    return {"access_token": d["access_token"], "open_id": d.get("open_id", "")}
            time.sleep(random.uniform(0.4, 1.2) * (attempt + 1))
        except Exception:
            time.sleep(random.uniform(0.3, 0.8) * (attempt + 1))
    return None

def PyL(access_token, open_id, server_time_str, cfg):
    city, prov = random.choice(cfg["cities"])
    isp = random.choice(cfg["isps"])
    subnet = random.choice(cfg["ip_subnets"])
    ip = f"{subnet}.{random.randint(1,250)}.{random.randint(1,250)}"
    P = {}
    P[3]  = server_time_str; P[4] = "free fire"; P[5] = 1; P[7] = CLIENT_VERSION
    P[8]  = "Android OS 14 / API-34 (UP1A.231005.007/V816.0.15.0.UNQMIXM)"
    P[9]  = "Handheld"; P[10] = isp; P[11] = "CarrierDataNetwork"
    P[12] = 1666; P[13] = 750; P[14] = "352"
    P[15] = "ARM64 FP ASIMD AES | 2400 | 8"
    P[16] = 5563; P[17] = "Mali-G57 MC2"
    P[18] = "OpenGL ES 3.2 v1.r32p1-01eac0.0a0b917d9265b4c01be9925306306139"
    P[19] = f"Google|{str(uuid.uuid4())}"
    P[20] = ip; P[21] = cfg["lang"]; P[22] = open_id; P[23] = "8"
    P[24] = "Handheld"; P[25] = "Xiaomi 2312DRAABI"
    P[26] = cfg["gateway"]; P[29] = access_token; P[30] = 1
    P[41] = isp; P[42] = "Cellular"
    P[57] = "7428b253defc164018c604a1ebbfebdf"
    P[60] = 109685; P[61] = 58294; P[62] = 797; P[63] = 18000
    P[64] = 58818; P[65] = 109685; P[66] = 58818; P[67] = 109685; P[73] = 2
    P[74] = "/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/lib/arm64"
    P[76] = 1
    P[77] = "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~cqQgpdMykLQEM3odipXatw==/com.dts.freefireth-G6e5yOt1dtuXG5Ambhj18g==/base.apk"
    P[78] = 3; P[79] = 2; P[81] = "64"; P[83] = "2019121229"; P[85] = 3
    P[86] = "OpenGLES2"; P[87] = 4095; P[88] = 8
    P[89] = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    P[90] = city; P[91] = prov; P[92] = 8043; P[93] = "android"
    P[94] = "KqsHT4XbSZhqerDNUhjbS3DxG/4+I62zQU2tZFJN91kBUICAlZ5yujshLKvjlk/KiShfKfis8EeB1PMhFHIodWPncZC4fCHYF3TcTwNj95aWY/S3"
    P[95] = 111207; P[96] = '{"cur_rate":[60,90,120],"support_etc2":false}'
    P[97] = 1; P[98] = 1; P[99] = "4"; P[100] = "4"
    P[102] = "GQ]        e"; P[103] = 1
    P[104] = 45174; P[105] = 1
    P[106] = "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|a4332cb1c1a84e51dd77441e4856ed5a"
    P[107] = "1.9393e7b8e53e8aeb"
    return AES.new(xK, AES.MODE_CBC, xV).encrypt(pad(ProToBuF(P), 16))

def MajorLogin(payload, sync_ts, cfg, max_retries=4):
    host = cfg["login_host"]
    url = f"https://{host}/MajorLogin"
    headers = {
        "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept": "*/*", "Accept-Encoding": "deflate, gzip",
        "X-GA-SV": str(sync_ts), "Authorization": "Bearer ",
        "X-GA": "v1 1", "ReleaseVersion": RELEASE_VERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": UNITY_VERSION,
        "Host": host,
    }
    for attempt in range(max_retries):
        try:
            sess = _new_session()
            R = sess.post(url, headers=headers, data=payload, timeout=12)
            sess.close()
            if R.status_code in (200, 201) and R.content:
                return R.content
            time.sleep(random.uniform(0.4, 1.0) * (attempt + 1))
        except Exception:
            time.sleep(random.uniform(0.3, 0.8) * (attempt + 1))
    return None

def ExtractMajorLogin(ml_resp):
    if len(ml_resp) <= 64: return None
    body = ml_resp[64:] if ml_resp[0] != 0x0a else ml_resp
    f = {}
    pos = 0; n = len(body)
    while pos < n:
        try:
            key = 0; shift = 0
            while True:
                b = body[pos]; pos += 1
                key |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
        except Exception: break
        fn = key >> 3; wt = key & 0x07
        try:
            if wt == 0:
                val = 0; shift = 0
                while True:
                    b = body[pos]; pos += 1
                    val |= (b & 0x7F) << shift
                    if not (b & 0x80): break
                    shift += 7
            elif wt == 2:
                ln = 0; shift = 0
                while True:
                    b = body[pos]; pos += 1
                    ln |= (b & 0x7F) << shift
                    if not (b & 0x80): break
                    shift += 7
                val = body[pos:pos + ln]; pos += ln
            elif wt == 5: val = body[pos:pos + 4]; pos += 4
            elif wt == 1: val = body[pos:pos + 8]; pos += 8
            else: break
        except Exception: break
        f.setdefault(fn, []).append(val)

    jwt_b = f.get(8, [None])[0]
    url_b = f.get(10, [None])[0]
    key_b = f.get(22, [None])[0]
    iv_b  = f.get(23, [None])[0]
    if not jwt_b or not isinstance(key_b, bytes) or not isinstance(iv_b, bytes): return None
    return {"jwt": jwt_b.decode(), "url": url_b.decode() if url_b else None, "key": key_b, "iv": iv_b}

def BuildAuthToken(uid, jwt_str, ts, key, iv, mode="online"):
    ah = f"{int(uid):x}"
    if len(ah) > 16: raise ValueError("uid hex too long")
    ah = ah.zfill(16)
    enc = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(jwt_str.encode(), 16)).hex()
    th = f"{int(ts):x}"
    if len(th) % 2: th = "0" + th
    tsz = f"{len(enc)//2:02x}"
    pad_ = "00000" if mode == "chat" else "0000000000000"
    return f"9015{ah}{th}{pad_}{tsz}{enc}"

def _TuneSock(s):
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 15)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 2)
    except Exception: pass

FIELD22_HEX = (
    "47475245010101008202000048d0c6912766f3f72cedb7201cf7a7098d74888b9eb4070aec58e1cd"
    "29f26559fb3b8d32cc302d17c00fe629c20b94bece7b75867df5d2c63ad694fe754b06ca5f200fc"
    "c316532ee2d705c69d64e873a976d73f1bada85dedb1271bfd90f13e6eb1f607b197ea5741550829"
    "c40b5b9ab59f305fd460c462ac2ba9a50561b453053303105b3329e6aef4bf468da4ae276023c26"
    "fa39932d0ec40d874a849550e72f67b2f1e0974f835df6a8b5f3cd886483abd0da7cbccc6cd4df7"
    "2aa5b104e63ea2bfeaf7b08d5176d2a9b128b8630468f625392397e2e43f63969e842f6e2c001c6"
    "da1cab2660eacaf8fdbc20520e1316a538406c480f3eefae89171f542b6aa5a8da797673764b0b0"
    "5ac26a31511759cbdad6826ab621d208e0cf5282a76eb8453f8f768fd8d52dd408d64c0063149605"
    "de6af9b34bdf22202ea8d132cd797bbfb6ac72455000c493b18085957df0144f73b36b1aec77f8f"
    "5ca3c838d1c2b7e065db59df08b0e8b87dc6769a12ed8ed729c5a3c58468afc6f0c52604a3448b3"
    "dbca6a587ccff08bbdcd22e767169949942742142f52f837bfe97f49c801cad0b2d3fd22101188b"
    "d5e1dafeeabc4259abe0c7f2b96c5ded89eac5843e7cb95177755b6cf63edd6abaccf03fadcb708"
    "4988b2c28d7f3574da8775f6a2de3a429513837ad8319fefa6eb9bfaa1a1a8b06f9d58778c953ab"
    "1fc38b4569879416e65625d15ce233cbfffb2cbd56aeb16e07e05da7a52bff20f1d4e11643a328b"
    "28105ab74256507f9fccab3bfd0575b4b6fb0fdbeb448c9a1e4e780a4dfdabb2b487cd83f427648"
    "16d9a6f3e313349b95ce6fb5ca6dbb60d2f5c3b5157da94c84e2b7ce0e47e5dcbf4d7c146089b1"
    "04979a5627e4f70a0a8d51a9ce358761119e0eb5ec3d2d7fea4f87227f9dfeaeb3a4ccd2b4cd38c"
    "aa754c827d45ff0d00d520db11a49fdb6f0b4010203"
)
KEYSTREAM = [0x30,0x30,0x30,0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,
             0x32,0x30,0x31,0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30,0x31,
             0x37,0x30,0x30,0x30,0x30,0x30,0x32,0x30]

def major_register(open_id, access_token, nickname, sync_ts, cfg, max_retries=4):
    host = cfg["login_host"]
    encoded = "".join(chr(ord(c) ^ KEYSTREAM[i % len(KEYSTREAM)]) for i, c in enumerate(open_id))
    fields = {
        1: nickname, 2: access_token, 3: open_id, 5: 102000007,
        6: 4, 7: 1, 8: 4, 13: 1, 14: encoded.encode('latin1'),
        15: cfg["lang"], 16: 1, 20: CLIENT_VERSION, 21: 1,
        22: bytes.fromhex(FIELD22_HEX),
    }
    proto = _proto(fields)
    payload = _aes_encrypt(proto)
    headers = {
        "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "Accept": "*/*", "X-GA-SV": str(sync_ts),
        "Authorization": "Bearer", "X-GA": "v1 1",
        "ReleaseVersion": RELEASE_VERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": UNITY_VERSION, "Host": host,
        "Connection": "Keep-Alive",
    }
    for attempt in range(max_retries):
        try:
            sess = _new_session()
            r = sess.post(f"https://{host}/MajorRegister", data=payload, headers=headers, timeout=12)
            sess.close()
            if r.status_code == 200:
                aid = _first_varint(r.content, 3)
                if aid: return str(aid)
            time.sleep(random.uniform(0.4, 1.0) * (attempt + 1))
        except Exception:
            time.sleep(random.uniform(0.3, 0.8) * (attempt + 1))
    return None


# ═══════════════ BIO SETTER ═══════════════
def upload_bio(jwt, bio_text, cfg, max_retries=3):
    bio_url = f"https://{cfg['client_host']}/UpdateSocialBasicInfo"
    for attempt in range(max_retries):
        try:
            bio_headers = {
                "Expect": "100-continue",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": RELEASE_VERSION,
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Authorization": f"Bearer {jwt}",
            }
            fields = {2: 17, 5: {}, 6: {}, 8: bio_text, 9: 1, 11: {}, 12: {}}
            raw = _proto(fields)
            encrypted = _aes_encrypt(raw)
            sess = _new_session()
            r = sess.post(bio_url, headers=bio_headers, data=encrypted, timeout=12)
            sess.close()
            if r.status_code == 200:
                return True
            time.sleep(random.uniform(0.4, 1.0) * (attempt + 1))
        except Exception:
            time.sleep(random.uniform(0.3, 0.8) * (attempt + 1))
    return False


# ═══════════════ MASTER GENERATOR ═══════════════
async def generate_one(sem, progress, region_code):
    async with sem:
        # Pick region config
        if region_code == "AUTO":
            actual = random.choice(list(REGIONS.keys()))
        else:
            actual = region_code
        cfg = REGIONS[actual]

        sync_ts, sync_time_str = get_server_time()
        device_id = "02-" + str(uuid.uuid4())

        # Step 1: Guest register
        uid, password = await asyncio.to_thread(guest_register, device_id, cfg)
        if not uid:
            return None

        await asyncio.sleep(random.uniform(0.1, 0.4))

        # Step 2: Get token
        token_data = await asyncio.to_thread(guest_token, uid, cfg)
        if not token_data:
            return None

        await asyncio.sleep(random.uniform(0.1, 0.3))

        open_id      = token_data["open_id"]
        access_token = token_data["access_token"]
        nickname     = generate_nickname()

        # Step 3: Major register
        account_id = await asyncio.to_thread(
            major_register, open_id, access_token, nickname, sync_ts, cfg)
        if not account_id:
            return None

        await asyncio.sleep(random.uniform(0.1, 0.3))

        # Step 4: Major login
        login_payload = await asyncio.to_thread(PyL, access_token, open_id, sync_time_str, cfg)
        ml = await asyncio.to_thread(MajorLogin, login_payload, sync_ts, cfg)
        if not ml:
            return None

        ad = await asyncio.to_thread(ExtractMajorLogin, ml)
        if not ad:
            return None

        jwt = ad["jwt"]; key = ad["key"]; iv = ad["iv"]
        url = ad["url"] or f"https://{cfg['client_host']}"

        # Step 5: GetLoginData → TCP online
        ip, port = None, None
        gl = None
        try:
            headers = {
                "User-Agent": "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
                "Accept": "*/*", "Accept-Encoding": "deflate, gzip",
                "X-GA-SV": str(sync_ts), "Authorization": f"Bearer {jwt}",
                "X-GA": "v1 1", "ReleaseVersion": RELEASE_VERSION,
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Unity-Version": UNITY_VERSION,
            }
            sess = _new_session()
            r = sess.post(f"{url}/GetLoginData", headers=headers, data=login_payload, timeout=10)
            sess.close()
            if r.status_code == 200: gl = r.content
        except Exception: pass

        if gl:
            gl_p = {}
            pos = 0
            while pos < len(gl):
                try:
                    key2 = 0; shift = 0
                    while True:
                        b = gl[pos]; pos += 1
                        key2 |= (b & 0x7F) << shift
                        if not (b & 0x80): break
                        shift += 7
                    fn = key2 >> 3; wt = key2 & 0x07
                    if wt == 0:
                        val = 0; shift = 0
                        while True:
                            b = gl[pos]; pos += 1
                            val |= (b & 0x7F) << shift
                            if not (b & 0x80): break
                            shift += 7
                    elif wt == 2:
                        ln = 0; shift = 0
                        while True:
                            b = gl[pos]; pos += 1
                            ln |= (b & 0x7F) << shift
                            if not (b & 0x80): break
                            shift += 7
                        val = gl[pos:pos + ln]; pos += ln
                    elif wt == 5: val = gl[pos:pos + 4]; pos += 4
                    elif wt == 1: val = gl[pos:pos + 8]; pos += 8
                    else: break
                    gl_p.setdefault(fn, []).append(val)
                except Exception: break

            func_addr = gl_p.get(14, [None])[0]
            if func_addr and isinstance(func_addr, bytes):
                try:
                    ip, port = func_addr.decode().split(":")
                except Exception: pass

        online_status = "OFFLINE"
        if ip and port:
            try:
                s = socket.create_connection((ip, int(port)), timeout=5)
                _TuneSock(s)
                s.settimeout(5)
                auth_hex = BuildAuthToken(account_id, jwt, sync_ts, key, iv, mode="online")
                s.sendall(bytes.fromhex(auth_hex))
                time.sleep(0.25)
                s.close()
                online_status = "ONLINE"
            except Exception: pass

        # Step 6: Bio
        bio_status = "FAILED"
        bio_ok = await asyncio.to_thread(upload_bio, jwt, BIO_TEXT, cfg)
        if bio_ok:
            bio_status = "SUCCESS"

        # Step 7: Save
        acc_data = {
            "uid":           uid,
            "password":      password,
            "account_id":    account_id,
            "name":          nickname,
            "open_id":       open_id,
            "access_token":  access_token,
            "region":        actual,
            "region_name":   cfg["name"],
            "online_status": online_status,
            "bio_status":    bio_status,
            "created_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "credit":        "@Prime_Leader69",
        }
        await _save_safe(acc_data)
        await progress("success", acc_data)
        return acc_data


# ═══════════════ MAIN ═══════════════
async def main():
    banner()

    # Region select
    show_region_menu()
    print()
    raw_region = input(
        f"{C.CYAN}{C.BOLD}┌──[ Region? (number or code, default BD) ]\n└──▶ {C.RESET}"
    ).strip().upper() or "BD"
    region_code = _RMAP.get(raw_region, raw_region if raw_region in REGIONS else "BD")
    if region_code == "AUTO":
        region_label = "AUTO · all regions"
    else:
        region_label = f"{region_code} · {REGIONS[region_code]['name']}"
    print(f"\n{C.CYAN}[*] Server: {C.BOLD}{region_label}{C.RESET}\n")

    try:
        raw = input(
            f"{C.CYAN}{C.BOLD}┌──[ How many accounts to generate? ]\n└──▶ {C.RESET}"
        ).strip()
        target_count = int(raw)
        if target_count <= 0: return
    except Exception:
        print(f"{C.RED}[!] Cancelled{C.RESET}")
        return

    print(f"\n{C.YELLOW}[*] Initializing Master Generator...{C.RESET}")
    print(f"{C.YELLOW}[*] Target: {target_count} accounts (Generate + Active + Bio)...{C.RESET}")
    print(f"{C.DIM}[*] Mode: Anti-Ban Continuous Generation (silent retries){C.RESET}\n")

    success_count = 0
    fail_streak   = 0
    progress_lock = asyncio.Lock()

    async def progress(status, data=None):
        nonlocal success_count, fail_streak
        async with progress_lock:
            if status == "success":
                success_count += 1
                fail_streak = 0
                reg = data.get("region","??")
                print(
                    f"  {C.GREEN}✔{C.RESET} [{success_count}/{target_count}] "
                    f"UID: {C.CYAN}{data['uid']}{C.RESET} | "
                    f"Name: {C.BOLD}{C.WHITE}{data['name']}{C.RESET} | "
                    f"Region: {C.CYAN}{reg}{C.RESET} | "
                    f"Online: {C.GREEN if data['online_status']=='ONLINE' else C.YELLOW}"
                    f"{data['online_status']}{C.RESET} | "
                    f"Bio: {C.GREEN if data['bio_status']=='SUCCESS' else C.RED}"
                    f"{data['bio_status']}{C.RESET}"
                )
            elif status == "fail":
                fail_streak += 1
                if fail_streak % 5 == 0:
                    print(f"  {C.DIM}{C.YELLOW}⚠ {fail_streak} soft-fails (auto-retrying...){C.RESET}")

    sem         = asyncio.Semaphore(3)
    stop_event  = asyncio.Event()

    async def worker(worker_id):
        while not stop_event.is_set():
            if success_count >= target_count: break
            try:
                result = await generate_one(sem, progress, region_code)
                if result is None:
                    await progress("fail")
                    await asyncio.sleep(random.uniform(0.8, 2.0))
            except Exception:
                await progress("fail")
                await asyncio.sleep(random.uniform(0.8, 2.0))

    worker_count = 6
    workers = [asyncio.create_task(worker(i)) for i in range(worker_count)]

    while success_count < target_count:
        await asyncio.sleep(0.5)
        if all(w.done() for w in workers):
            workers = [asyncio.create_task(worker(i)) for i in range(worker_count)]

    stop_event.set()
    for w in workers: w.cancel()
    await asyncio.gather(*workers, return_exceptions=True)

    print(f"\n{C.PURPLE}{C.BOLD}╔══════════════════════════════════════════════════════╗")
    print(f"║ [+] COMPLETE! Total Generated: {success_count}/{target_count}")
    print(f"║ [+] Saved to '{JSON_FILE}' & '{TXT_FILE}'")
    print(f"║ 👑 Credit: @Prime_Leader69")
    print(f"╚══════════════════════════════════════════════════════╝{C.RESET}")


if __name__ == "__main__":
    asyncio.run(main())
