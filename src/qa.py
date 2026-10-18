# Layout-QA: python3 src/qa.py  (startet lokalen Server auf docs/, prüft alle Seiten bei 390/820/1280 px)
import subprocess, sys, os, time, glob
from playwright.sync_api import sync_playwright
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","docs")
srv=subprocess.Popen([sys.executable,"-m","http.server","8799"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
CHK="""(()=>{const out=[];
document.querySelectorAll('.row2').forEach((r,k)=>{const ins=[...r.querySelectorAll('input,select')].map(e=>Math.round(e.getBoundingClientRect().top));if(ins.length==2&&Math.abs(ins[0]-ins[1])>2&&r.getBoundingClientRect().width>500)out.push('Eingabefelder nicht auf einer Linie #'+k)});
document.querySelectorAll('input,select,textarea').forEach(e=>{const b=e.getBoundingClientRect(),f=e.closest('form,main');if(f&&b.right>f.getBoundingClientRect().right+1)out.push('Feld ragt heraus '+(e.id||e.name))});
document.querySelectorAll('select').forEach(e=>{if(e.scrollWidth>e.clientWidth+2)out.push('Auswahltext abgeschnitten '+e.id)});
if(document.documentElement.scrollWidth>innerWidth)out.push('horizontales Scrollen');
document.querySelectorAll('img').forEach(i=>{if(!i.complete||i.naturalWidth==0)out.push('Bild fehlt '+i.getAttribute('src'))});
return out})()"""
bad=0
try:
    with sync_playwright() as p:
        b=p.chromium.launch()
        for w,h in [(390,844),(820,1180),(1280,900)]:
            pg=b.new_page(viewport={"width":w,"height":h}); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
            for f in sorted(glob.glob(os.path.join(ROOT,"*.html"))):
                u=os.path.basename(f); pg.goto("http://localhost:8799/"+u); pg.wait_for_timeout(100)
                r=pg.evaluate(CHK)+errs
                if r: bad+=1; print(w,u,r)
                errs.clear()
            pg.close()
        b.close()
finally: srv.terminate()
print("QA ok" if not bad else f"QA: {bad} Probleme"); sys.exit(1 if bad else 0)
