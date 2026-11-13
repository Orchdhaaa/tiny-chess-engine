import json,os,urllib.request as u  # stdlib-only engine
V=[0,100,320,330,500,900,20000]
ND=(-31,-33,-18,-14,14,18,33,31)
KD=(-17,-16,-15,-1,1,15,16,17)
BD=(-17,-15,15,17)
RD=(-16,-1,1,16)
BUDGET=40000
T=100000
b=[0]*128
w=True
s=0
K=[0,0]
def x(p,ps,k):
 global s
 v=V[abs(p)];s+=k*v*(p>0 or-1)
def parse_fen(pos):
 global b,w,s,K
 q=pos.split();b=[0]*128
 s=0
 for ix,lin in enumerate(q[0].split("/")):
  r=7-ix;f=0
  for c2 in lin:
   if c2.isdigit():
    f+=int(c2)
   else:
    p=(" pnbrqk".find(c2.lower()))*((c2<'a')or-1);ps=r*16+f
    b[ps]=p;x(p,ps,1)
    if p==6:
     K[0]=ps
    if p==-6:
     K[1]=ps
    f+=1
 w=q[1]=='w'
def A(ps,who):
 for d in(-17,-15)if who else(17,15):
  t=ps+d
  if not t&0x88 and b[t]==(1 if who else-1):
   return True
 for dl,pt in((ND,2),(KD,6)):
  for d in dl:
   t=ps+d
   if not t&0x88 and b[t]==(pt if who else-pt):
    return True
 for dl,pt in((BD,3),(RD,4)):
  for d in dl:
   t=ps+d
   while not t&0x88:
    p=b[t]
    if p:
     if p*(1 if who else-1)in(pt,5):
      return True
     break
    t+=d
 return False
def mv(f1,t1,p1=0,f2=0):
 return f1|(t1<<7)|(p1<<14)|(f2<<17)
def D():
 y=[]
 fd=32*w-16;r2=6-5*w
 l2=7*w
 for ps in range(128):
  if ps&0x88:
   continue
  p=b[ps]
  if p==0 or(p>0)!=w:
   continue
  t=abs(p)
  if t==1:
   r=ps>>4;o=ps+fd
   if b[o]==0:
    if(o>>4)==l2:
     y.append(mv(ps,o,5))
    else:
     y.append(mv(ps,o))
     if r==r2:
      t2=o+fd
      if b[t2]==0:
       y.append(mv(ps,t2,0,2))
   for d in(fd-1,fd+1):
    t1=ps+d
    if t1&0x88:
     continue
    t3=b[t1]
    if t3!=0 and(t3>0)!=w:
     if(t1>>4)==l2:
      y.append(mv(ps,t1,5,1))
     else:
      y.append(mv(ps,t1,0,1))
  elif t==2 or t==6:
   for d in(ND if t==2 else KD):
    t1=ps+d
    if t1&0x88:
     continue
    t3=b[t1]
    if t3==0:
     y.append(mv(ps,t1))
    elif(t3>0)!=w:
     y.append(mv(ps,t1,0,1))
  else:
   dl=BD if t==3 else RD if t==4 else BD+RD
   for d in dl:
    t1=ps+d
    while not t1&0x88:
     t3=b[t1]
     if t3==0:
      y.append(mv(ps,t1))
     else:
      if(t3>0)!=w:
       y.append(mv(ps,t1,0,1))
      break
     t1+=d
 return y
def _legal():
 lst=[]
 for m in D():
  u=make(m)
  if u is not None:
   lst.append(m);unmake(u)
 return lst
def make(m):
 global w
 u=(b[:],w,s,K[:]);f1=m&0x7F
 t1=(m>>7)&0x7F;p1=(m>>14)&7
 p=b[f1];cp2=b[t1]
 x(p,f1,-1)
 if cp2:
  x(cp2,t1,-1)
 np2=(p1*(2*w-1))if p1 else p;b[f1]=0
 b[t1]=np2;x(np2,t1,1)
 if abs(p)==6:
  K[1-w]=t1
 w=not w;ks2=K[w]
 if A(ks2,w):
  unmake(u)
  return None
 return u
def unmake(u):
 global w,s
 b[:],w,s,K[:]=u
def uci(m):
 f1=m&0x7F;t1=(m>>7)&0x7F
 p1=(m>>14)&7;sx=chr(97+f1%8)+str((f1>>4)+1)+chr(97+t1%8)+str((t1>>4)+1)
 if p1:
  sx+="nbrq"[p1-2]
 return sx
def E():
 return s if w else-s
N=0
a=False
def S(d,lo,hi,p2):
 global N,a
 N+=1
 if a:
  return 0
 if N>BUDGET and(N&2047)==0:
  a=True
  return 0
 ck2=A(K[1-w],not w)
 if d<=0:return E()
 j=-T-1
 y=D();i=0
 for m in y:
  u=make(m)
  if u is None:
   continue
  i+=1;s2=-S(d-1,-hi,-lo,p2+1)
  unmake(u)
  if a:
   return 0
  if s2>j:
   j=s2
  if s2>lo:
   lo=s2
  if lo>=hi:
   break
 if i==0:
  return-T+p2 if ck2 else 0
 return j
def R():
 global N,a
 y=_legal()
 if not y:
  return None
 j=y[0]
 for d in range(1,6):
  N=0;a=False
  lo=-T-1;cmv=y[0]
  bs=-T-1
  for m in y:
   u=make(m)
   if u is None:
    continue
   s2=-S(d-1,-T-1,-lo,1);unmake(u)
   if a:
    break
   if s2>bs:
    bs=s2;cmv=m
   if s2>lo:
    lo=s2
  if a:
   break
  j=cmv
  if bs>T-1000:
   break
 return j
def choose(pos,v):
 parse_fen(pos);m=R()
 return uci(m)if m else None
def post(path,body):
 rq2=u.Request(os.environ.get("MAKEFUN_ENV_URL")+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 with u.urlopen(rq2)as rs2:
  return json.load(rs2)
def main():
 while True:
  g=post("/game",{})
  if g["status"]=="done":
   break
  while g["status"]=="your_move":
   mv=choose(g["fen"],g["moves"])
   if mv is None:
    return
   g=post("/move",{"game":g["game"],"move":mv})
if __name__=="__main__":
 main()
