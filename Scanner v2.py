import socket
import requests
import whois
import geocoder


GREEN = "\033[1;92m"
WHITE = "\033[97m"
RESET = "\033[0m"

def MainColor(text):
    start_color = (5, 168, 5)  
    end_color = (118, 255 ,118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    gradient_chars = '┴┼┘┤└┐─┬├┌└│]░▒░▒█▓▄▌▀()'
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in gradient_chars:
                color_index = (i + j) % num_colors
                color = colors[color_index]
                result.append(text_color(*color) + char + "\0330m")
            else:
                result.append(char)
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)



def MainColor2(text):
    start_color = (5, 168, 5)  
    end_color = (118, 255 ,118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            color_index = (i + j) % num_colors
            color = colors[color_index]
            result.append(text_color(*color) + char + "\033[0m")
        
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)







def checkports(ip, port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.1)
    try:
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(GREEN+f"[OPEN] Port {port}"+RESET)
        else:
            print(f"[CLOSED] Port {port}")
        sock.close()
    except:
        pass

def coords(ip):
    try:
        ip_addr = socket.gethostbyname(ip)
        g = geocoder.ipinfo(ip_addr)
        print(MainColor2("Coortdinates of IP-adress:", g.latlng))
        print(MainColor2("Approximate location of IP:", g.city))
    except:
        print("!Dont forget to validate information!")

def who1(ip):
    try:
        w = whois.whois(ip)
        print(MainColor2("Whois 1:"))
        for key in ['domain_name', 'registrar', 'creation_date', 'expiration_date', 'name_servers']:
            if key in w:
                print(f"{key}: {w[key]}")
    except:
        print("No information was founded.")

def who2(ip):
    try:
        ip_addr = socket.gethostbyname(ip)
        r = requests.get(f"https://ipinfo.io/{ip_addr}/json").json()
        print(MainColor2("Whois 2:"))
        print("IP:", r.get("ip"))
        print("City:", r.get("city"))
        print("Region:", r.get("region"))
        print("Country:", r.get("country"))
        print("Organisation:", r.get("org"))
        print("Coordintes:", r.get("loc"))
        print("Zip-code:", r.get("postal"))
        print("timezone:", r.get("timezone"))
        print("Hostname:", r.get("hostname"))
    except:
        print("Whois №2 unable to get info.")

# MAIN 
print(MainColor2("""

   ___           __    ____                                  ___ 
  / _ \___  ____/ /_  / __/______ ____  ___  ___ ____  _  __|_  |
 / ___/ _ \/ __/ __/ _\ \/ __/ _ `/ _ \/ _ \/ -_) __/ | |/ / __/ 
/_/   \___/_/  \__/ /___/\__/\_,_/_//_/_//_/\__/_/    |___/____/ 
                                                                     
                  by Sam Howard
                                                """))


while True:
    ip = input(MainColor2("-Input IP or domen: "))
    try:
        ip_addr = socket.gethostbyname(ip)
    except:
        print(GREEN+"Wrong IP or domen."+RESET)
        continue

    # Ports to check
    ports = [7, 20, 21, 22, 23, 25, 53, 69, 79, 80, 81, 88, 110, 115, 143, 389, 443, 587, 993, 995, 2083, 2087, 2222, 3128, 3306, 5432, 8080, 8083]

    print(MainColor2("\n=== Scanning ports ==="))
    for p in ports:
        checkports(ip_addr, p)

    print(MainColor2("\n=== Geolocation of IP ==="))
    coords(ip)

    print(MainColor2("\n=== Whois information ==="))
    who1(ip)
    who2(ip)

    cont = input(MainColor2("\nNext scan?(yes/no): ").lower())
    if cont not in ['yes', 'y']:
        print("Exiting...")
        break
