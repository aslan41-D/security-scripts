import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

parser = argparse.ArgumentParser(description="Port Scanner")
parser.add_argument("-i","--ip",required=True,type=str,help="taranacak ip adresini giriniz")
parser.add_argument("-p","--ports",required=True,type=str,help="taranacak port aralığını giriniz")
parser.add_argument("-t","--timeout",type=float,default=1.0,help="timeoutu saniye türünden giriniz")
parser.add_argument("-w","--workers", type=int, default=100,help="thread sayısını ayarlayabilirsiniz.")
args = parser.parse_args() 

def parse_port_range(port_str):
    """
        "1-1024" formatındaki stringi [1, 2, ..., 1024] şeklinde sayı listesine çevirir.
        Hatalı formatlarda ValueError fırlatır.
    """
    try:
        parcalar = port_str.split("-")

        if len(parcalar)!=2:
            raise ValueError("Port aralığı 'başlangıç bitiş' formatında olmalıdır. Örn : 1-1024")

        baslangic = int(parcalar[0])
        bitis = int(parcalar[1])

        if not ( 1 <= baslangic <= 65535) or not (1 <= bitis <= 65535):
            raise ValueError("Port numaraları 1 ile 65535 arasında olmalıdır")

        if baslangic > bitis:
            raise ValueError("Baslangic portu bitis portundan büyük olamaz.")

        return list(range(baslangic,bitis+1)) # baslangic ve bitis portunu sayi listesini döndürür.
    
    
    except ValueError as e:
        if  "invalid literal for int()" in str(e):
            raise ValueError("Port numaraları sadece tam sayılardan oluşmalıdır.")
        else:
            raise ValueError(e)

def scan_port(ip, port, timeout):
    """
        Belirtilen IP ve porta TCP bağlantısı kurmaya çalışır.
        Port açık ise True, kapalı veya zaman aşımına uğradıysa False döner
    """

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sonuc = sock.connect_ex((ip,port))

        if sonuc == 0:
            return True
        else:
            return False
    
    except Exception:
        return False
    finally:
        sock.close()

def main():
    try:
        port_listesi = parse_port_range(args.ports)

    except ValueError as e:
        parser.error(f"Port Hatası : {e}")

    if args.workers <= 0:
        parser.error("Thread sayisi ( --workers) = veya daha kücük olamaz")


    acik_portlar_listesi = []
    toplam_tarandi = 0
    futures = {}

    executor = ThreadPoolExecutor(max_workers=args.workers)

    try:
        for port in port_listesi:
            future = executor.submit(scan_port,args.ip,port,args.timeout)
            futures[future] = port
        for future in as_completed(futures):
            toplam_tarandi+=1
            port = futures[future] 

            try:
                durum = future.result()
                if durum:
                    acik_portlar_listesi.append(port)
            except Exception:
                print(f"Hata : {e}")
    except socket.gaierror:
        print(f"[-] Hata : '{args.ip}' geçerli bir IP adresi veya domain değil.")
        executor.shutdown(wait=False, cancel_futures=True)
        return

    except KeyboardInterrupt:
        print(f"\n[-] Tarama kullanıcı tarafından iptal edildi.")
        executor.shutdown(wait=False, cancel_futures=True)
        
        acik_portlar_listesi.sort()
        port_str_listesi = [str(p) for p in acik_portlar_listesi]
        print(f"[+] Açık portlar: {', '.join(port_str_listesi) if port_str_listesi else 'Yok'}")
        print(f"[!] Özet: Toplam {toplam_tarandi} port tarandı, {len(acik_portlar_listesi)} açık port bulundu.")
        return

    executor.shutdown(wait=True)

    print("-" * 40)
    
    acik_portlar_listesi.sort()
    port_str_listesi = [str(p) for p in acik_portlar_listesi]
    
    print(f"[+] Açık portlar: {', '.join(port_str_listesi) if port_str_listesi else 'Yok'}")
    print(f"Toplam {len(port_listesi)} port tarandı, {len(acik_portlar_listesi)} açık port bulundu.")

if __name__ == "__main__":
    main()
        
