#!/usr/bin/env python3
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

N=360
ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'certificates'/'core-v3.json'

def phi(m):
    return sum(math.gcd(a,m)==1 for a in range(1,m+1))

def order_mod(a):
    assert math.gcd(a,N)==1
    x=1
    for k in range(1,100):
        x=x*a%N
        if x==1:return k
    raise AssertionError

def subgroup(gens):
    s={1}; changed=True
    while changed:
        changed=False
        for a in tuple(s):
            for g in gens:
                b=a*g%N
                if b not in s:
                    s.add(b); changed=True
    return s

def ideal(d):
    return {(d*j)%N for j in range(N//math.gcd(d,N))}

def ann_set(S):
    return {a for a in range(N) if all(a*x%N==0 for x in S)}

R=list(range(N))
G=[x for x in R if math.gcd(x,N)==1]
assert len(G)==96
assert Counter(order_mod(x) for x in G)=={1:1,2:15,3:2,4:16,6:30,12:32}

D=[d for d in range(1,N+1) if N%d==0]
assert len(D)==24
strata={d:{x for x in R if math.gcd(x,N)==d} for d in D}
for d in D:
    assert len(strata[d])==phi(N//d)
    if d<N:
        assert strata[d]=={(d*u)%N for u in range(N//d) if math.gcd(u,N//d)==1}

for d in D:
    S=strata[d]
    if not S: continue
    a=next(iter(S))
    assert {u*a%N for u in G}==S

# Complete ideal/annihilator dictionary.
Id={d:ideal(d) for d in D}
assert len({frozenset(v) for v in Id.values()})==24
for d in D:
    I=Id[d]
    assert len(I)==N//d
    assert strata[d]=={x for x in R if ideal(math.gcd(x,N))==I and math.gcd(x,N)==d}
    assert ann_set(I)==Id[N//d]
    assert len(ann_set(I))==d
    for x in strata[d]:
        Rx={a*x%N for a in R}
        Ax={a for a in R if a*x%N==0}
        assert Rx==I
        assert Ax==Id[N//d]
        assert len(Ax)==d
        assert len(Rx)*len(Ax)==N
        # additive order of x
        k=1
        while k*x%N:
            k+=1
        assert k==N//d

for d in D:
    for e in D:
        isum={(a+b)%N for a in Id[d] for b in Id[e]}
        assert isum == Id[math.gcd(d,e)]
        assert Id[d] & Id[e] == Id[math.lcm(d,e)]
        prod={a*b%N for a in Id[d] for b in Id[e]}
        assert prod==Id[math.gcd(d*e,N)]
        assert ann_set(isum) == ann_set(Id[d]) & ann_set(Id[e])
        anns_sum={(a+b)%N for a in ann_set(Id[d]) for b in ann_set(Id[e])}
        assert ann_set(Id[d] & Id[e]) == anns_sum

E_all={x for x in R if x*x%N==x}
unitary=[d for d in D if math.gcd(d,N//d)==1]
assert unitary==[1,5,8,9,40,45,72,360]
idem_by_d={}
for d in unitary:
    cand=[e for e in E_all if math.gcd(e,N)==d]
    assert len(cand)==1
    idem_by_d[d]=cand[0]
    e=cand[0]
    assert Id[d]=={a*e%N for a in R}
    assert math.gcd((1-e)%N,N)==N//d
assert set(idem_by_d.values())==E_all

# Additive character orthogonal complement: k is orthogonal to I_d iff k in I_{N/d}.
for d in D:
    I=Id[d]
    ortho={k for k in R if all((k*x)%N==0 for x in I)}
    assert ortho==Id[N//d]

Nil={(30*j)%N for j in range(12)}
assert len(Nil)==12
assert {a*b%N for a in Nil for b in Nil}=={0,180}
assert {a*b*c%N for a in Nil for b in Nil for c in Nil}=={0}
Sq0={(60*j)%N for j in range(6)}
assert all(a*b%N==0 for a in Sq0 for b in Sq0)

# Jacobson radical / socle and maximal-minimal annihilator pairing.
J=Id[30]
Soc=Id[12]
assert J==Nil
assert ann_set(J)==Soc
soc_sum={(a+b+c)%N for a in Id[180] for b in Id[120] for c in Id[72]}
assert soc_sum==Soc
for m,mini in ((2,180),(3,120),(5,72)):
    assert ann_set(Id[m])==Id[mini]
    assert ann_set(Id[mini])==Id[m]

K={(1+30*j)%N for j in range(12)}
assert K=={u for u in G if u%30==1}
assert subgroup([31,91])==K
assert order_mod(31)==6 and order_mod(91)==2
for u in G:
    assert {(u+30*j)%N for j in range(12)}=={u*k%N for k in K}
for j in range(12):
    for k in range(12):
        lhs=(1+30*j)*(1+30*k)%N
        rhs=(1+30*((j+k+6*j*k)%12))%N
        assert lhs==rhs

Q={u*u%N for u in G}
assert Q=={1,49,121,169,241,289}
C={(1+60*j)%N for j in range(6)}
assert C=={1,61,121,181,241,301}
assert subgroup([49])==Q and subgroup([61])==C
assert Q&C=={1,121,241}

unit_sizes={k:len({pow(u,k,N) for u in G}) for k in range(1,13)}
assert [unit_sizes[k] for k in range(1,13)]==[96,6,32,3,96,2,96,3,32,6,96,1]

M={pow(x,13,N) for x in R}
assert len(M)==175
assert M=={x for x in R if pow(x,13,N)==x}
for x in R:
    r=pow(x,13,N); n=(x-r)%N
    assert n in Nil and r*n%N==0

E={pow(x,12,N) for x in R}
assert E=={0,1,81,136,145,216,225,280}
assert all(e*e%N==e for e in E)

ring_sizes={k:len({pow(x,k,N) for x in R}) for k in range(1,25)}
assert [ring_sizes[k] for k in range(1,25)]==[360,36,75,16,175,12,175,16,75,24,175,8,175,24,75,16,175,12,175,16,75,24,175,8]

U30=[r for r in range(30) if math.gcd(r,30)==1]
assert U30==[1,7,11,13,17,19,23,29]
gaps=[(U30[(i+1)%8]-U30[i])%30 for i in range(8)]
assert gaps==[6,4,2,4,2,4,6,2]
prime_cap=[r for r in R if math.gcd(r,N)==1]
assert all(sum((r+30*j)%N in prime_cap for j in range(12))==12 for r in U30)

for h in range(N):
    brute=sum(math.gcd(r,N)==1 and math.gcd(r+h,N)==1 for r in R)
    prod=12
    for p in (2,3,5):
        prod*=p-len({0%p,h%p})
    assert brute==prod

for a in range(1,13):
    for b in range(1,13):
        lhs={pow(x,a,N)*pow(y,b,N)%N for x in G for y in G}
        d=math.gcd(a,b,12)
        rhs={pow(x,d,N) for x in G}
        assert lhs==rhs


# Multiplicative quotient by unit/associate shells and uniform fibers.
shell_fiber_values={}
for d in D:
    for e in D:
        g=math.gcd(d*e,N)
        counts=Counter((x*y)%N for x in strata[d] for y in strata[e])
        assert set(counts)==strata[g]
        expected=len(strata[d])*len(strata[e])//len(strata[g])
        assert set(counts.values())=={expected}
        shell_fiber_values[(d,e)]=(g,expected)

# Ring-theoretic irreducibles: keep separate from ordinary integer primes.
factor_pairs={z:[] for z in R}
for a in R:
    for b in R:
        factor_pairs[a*b%N].append((a,b))

def associates(a,b):
    return math.gcd(a,N)==math.gcd(b,N)

def is_irreducible(x):
    if x==0 or x in G:
        return False
    return all(associates(x,a) or associates(x,b) for a,b in factor_pairs[x])

def is_very_strong_irreducible(x):
    if x==0 or x in G:
        return False
    return all(((a in G)+(b in G))==1 for a,b in factor_pairs[x])

irreducibles={x for x in R if is_irreducible(x)}
very_strong={x for x in R if is_very_strong_irreducible(x)}
assert irreducibles==strata[2]|strata[3]|strata[5]
assert very_strong==strata[2]|strata[3]
assert len(irreducibles)==104 and len(very_strong)==80

unique_factorization_shells=[d for d in D if d not in (1,N) and all((N//d)%p==0 for p in (2,3,5))]
assert unique_factorization_shells==[2,3,4,6,12]

H=subgroup([37,71])
assert len(H)==8 and H&K=={1}
assert {h%30 for h in H}==set(U30)
assert {h*k%N for h in H for k in K}==set(G)

payload={
  'modulus':360,
  'divisor_count':len(D),
  'ideal_count':len(D),
  'annihilator_pairs':[[d,N//d] for d in D if d<=N//d],
  'direct_summand_ideal_divisors':unitary,
  'idempotent_generators_by_ideal':{str(d):idem_by_d[d] for d in unitary},
  'jacobson_radical_generator':30,
  'socle_generator':12,
  'maximal_minimal_annihilator_pairs':[[2,180],[3,120],[5,72]],
  'shell_product_rule':'target_d=gcd(d*e,360)',
  'shell_product_rows':len(D)*len(D),
  'ring_prime_strata':[2,3,5],
  'very_strong_irreducible_strata':[2,3],
  'unique_irreducible_factorization_strata':unique_factorization_shells,
  'unit_count':len(G),
  'unit_order_counts':dict(sorted(Counter(order_mod(x) for x in G).items())),
  'unit_power_image_sizes':unit_sizes,
  'square_hexagon':sorted(Q),
  'congruence_hexagon':sorted(C),
  'hexagon_intersection':sorted(Q&C),
  'nilradical':sorted(Nil),
  'nilradical_square':sorted({a*b%N for a in Nil for b in Nil}),
  'regular_skeleton_size':len(M),
  'support_idempotents':sorted(E),
  'ring_power_image_sizes':ring_sizes,
  'mod30_units':U30,
  'mod30_wheel_gaps':gaps,
  'status':'PASS'
}
raw=json.dumps(payload,sort_keys=True,indent=2).encode()
CERT.parent.mkdir(exist_ok=True)
CERT.write_bytes(raw+b'\n')
print('PASS')
print('certificate:',CERT.relative_to(ROOT))
print('sha256:',hashlib.sha256(raw+b'\n').hexdigest())
