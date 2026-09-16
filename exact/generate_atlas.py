#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

N=360
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
DATA.mkdir(exist_ok=True)

def order_mod(a):
    if math.gcd(a,N)!=1:
        return ''
    x=1
    for k in range(1,13):
        x=x*a%N
        if x==1:
            return k
    raise AssertionError(a)

def is_nilpotent(x):
    y=x%N
    for _ in range(1,5):
        if y==0:
            return True
        y=y*x%N
    return False

def support_label(e):
    bits=(e%8!=0,e%9!=0,e%5!=0)
    return ''.join(p for p,b in zip(('2','3','5'),bits) if b) or 'empty'

def phi(m):
    return sum(math.gcd(a,m)==1 for a in range(1,m+1))

def vp(d,p):
    a=0
    while d%p==0:
        a+=1
        d//=p
    return a

fields=['r','gcd360','mod8','mod9','mod5','mod30','prime_capable','unit_order',
        'mirror','square','cube','pow4','pow6','pow12','pow13','support_idempotent',
        'support','regular','nilpotent']
with (DATA/'residue-atlas.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=fields)
    w.writeheader()
    for r in range(N):
        p12=pow(r,12,N); p13=pow(r,13,N)
        w.writerow({
            'r':r,'gcd360':math.gcd(r,N),'mod8':r%8,'mod9':r%9,'mod5':r%5,
            'mod30':r%30,'prime_capable':int(math.gcd(r,N)==1),'unit_order':order_mod(r),
            'mirror':(-r)%N,'square':pow(r,2,N),'cube':pow(r,3,N),'pow4':pow(r,4,N),
            'pow6':pow(r,6,N),'pow12':p12,'pow13':p13,'support_idempotent':p12,
            'support':support_label(p12),'regular':int(p13==r),'nilpotent':int(is_nilpotent(r))
        })

divs=[d for d in range(1,N+1) if N%d==0]
with (DATA/'gcd-strata.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['d','size','phi_360_over_d'])
    for d in divs:
        size=sum(math.gcd(x,N)==d for x in range(N))
        w.writerow([d,size,phi(N//d)])

with (DATA/'relation-strata.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['d','degree_per_vertex','ordered_pairs'])
    for d in divs:
        degree=sum(math.gcd(t,N)==d for t in range(N))
        w.writerow([d,degree,N*degree])

idempotents=[x for x in range(N) if x*x%N==x]
with (DATA/'ideal-lattice.csv').open('w',newline='',encoding='utf-8') as f:
    fields=['d','v2','v3','v5','ideal_size','quotient_size','generator_shell_size',
            'annihilator_d','annihilator_size','overlap_gcd','direct_summand',
            'idempotent_generator','maximal','minimal_nonzero']
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
    for d in divs:
        ann=N//d
        idem=[e for e in idempotents if math.gcd(e,N)==d]
        w.writerow({
            'd':d,'v2':vp(d,2),'v3':vp(d,3),'v5':vp(d,5),
            'ideal_size':N//d,'quotient_size':d,'generator_shell_size':phi(N//d),
            'annihilator_d':ann,'annihilator_size':d,'overlap_gcd':math.gcd(d,ann),
            'direct_summand':int(math.gcd(d,ann)==1),
            'idempotent_generator':idem[0] if idem else '',
            'maximal':int(d in (2,3,5)),
            'minimal_nonzero':int(d in (180,120,72)),
        })

units=[x for x in range(N) if math.gcd(x,N)==1]
power={str(k):sorted({pow(x,k,N) for x in units}) for k in range(1,13)}
(DATA/'unit-power-images.json').write_text(json.dumps(power,indent=2)+'\n',encoding='utf-8')
print('generated residue/gcd/relation/ideal tables and unit-power-images.json')
