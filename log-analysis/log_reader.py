import argparse
import os
import sys

parser = argparse.ArgumentParser(description="Log Analiz Aracı")
parser.add_argument("dosya",type=str,help="Okunacak log dosyasının yolu")
parser.add_argument("--threshold",type=int,default=0,help="Minimum istek sınırı")
args = parser.parse_args() 

file_path = args.dosya

if os.path.exists(file_path):
    pass
else:
    print("Dosya yolu bulunamadı !")
    sys.exit()

ip_counter = {}

with open(file_path ,"r") as file :
    for satir in file:
        parcalar = satir.split()

        if not parcalar :
            continue

        ip = parcalar[0]

        if ip not in ip_counter:
            ip_counter[ip] = 1
        else:
            ip_counter[ip] = ip_counter[ip] + 1
    
fitrelenmis_ve_siralanmis = sorted([item for item in ip_counter.items() if item[1] >= args.threshold], key=lambda x: x[1], reverse=True)


for anahtar , deger in fitrelenmis_ve_siralanmis:
        print(f"IP : {anahtar} => {deger} requests ")
