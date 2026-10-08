# ---- Final-5 expected returns: TR = (1+g)*(PEexit/PEnow)^(1/5) - 1 + DY (approx) ----
stocks = {
 # name: price, EPS base (CY26E/FY26 normalised), DY now, scenarios: (g, PE exit, avg DY)
 "SYS":   dict(px=150, eps=8.3,  sc={"Bear":(0.06,10,0.015),"Base":(0.17,15,0.02),"Bull":(0.25,18,0.02)}),
 "FFC":   dict(px=537.8,eps=60,  sc={"Bear":(0.00,7,0.08),"Base":(0.05,8.5,0.075),"Bull":(0.09,10,0.075)}),
 "OGDC":  dict(px=314.6,eps=46,  sc={"Bear":(-0.03,5,0.06),"Base":(0.04,6.5,0.065),"Bull":(0.08,8,0.07)}),
 "LUCK":  dict(px=411, eps=58,   sc={"Bear":(0.00,5.5,0.02),"Base":(0.10,8,0.025),"Bull":(0.16,10,0.03)}),
 "HINOON":dict(px=925, eps=84,   sc={"Bear":(0.06,8,0.04),"Base":(0.15,11,0.045),"Bull":(0.20,13,0.05)}),
}
w = {"FFC":0.25,"OGDC":0.20,"LUCK":0.20,"SYS":0.20,"HINOON":0.15}
port={}
for n,s in stocks.items():
    pe_now = s["px"]/s["eps"]
    out=[]
    for k,(g,pe,dy) in s["sc"].items():
        eps31 = s["eps"]*(1+g)**5
        p31 = eps31*pe
        pr = (p31/s["px"])**0.2-1
        tr = pr+dy
        out.append(f"{k}: EPS31 {eps31:.1f} P31 Rs{p31:.0f} price-CAGR {pr*100:.1f}% TR~{tr*100:.1f}%")
        port.setdefault(k,0); port[k]+=w[n]*tr
    print(f"{n} px {s['px']} P/E now {pe_now:.1f} | "+" | ".join(out))
print("Portfolio weighted TR:", {k:round(v*100,1) for k,v in port.items()})

# ---- SIP model ----
def sip(step, r_annual, years=5, m0=35000, reinvest=True, dy=0.0):
    rm=(1+r_annual)**(1/12)-1
    v=0; inv=0; m=m0
    for y in range(years):
        for mo in range(12):
            v=v*(1+rm)+m; inv+=m
        m*=1+step
    return inv,v
def xirr_sip(step, fv, years=5, m0=35000):
    lo,hi=-0.5,1.5
    for _ in range(200):
        mid=(lo+hi)/2
        _,v=sip(step,mid,years,m0)
        if v<fv: lo=mid
        else: hi=mid
    return mid
print("\n== Contributions ==")
for st in [0.05,0.10,0.15]:
    m=35000; yrs=[]
    for y in range(5): yrs.append(m); m*=1+st
    print(st, [round(x) for x in yrs], "total", round(sum(x*12 for x in yrs)))
print("\n== Portfolio value after 5 yrs (total return, dividends reinvested) ==")
scen={"Bear":0.02,"Base":0.15,"Bull":0.24}
for st in [0.05,0.10,0.15]:
    for k,r in scen.items():
        inv,v=sip(st,r)
        inv2,v2=sip(st,r-0.06)  # dividends NOT reinvested & spent: approx lose ~6% yield
        print(f"step {st:.0%} {k} r={r:.0%}: invested {inv:,.0f} value {v:,.0f} profit {v-inv:,.0f} ({(v/inv-1)*100:.0f}%) | if divs withdrawn (r-6%) value {v2:,.0f}")
print("\n== Required annual return to hit targets ==")
for st in [0.05,0.10,0.15]:
    for tgt in [5e6,10e6]:
        print(f"step {st:.0%} target {tgt/1e6:.0f}m: required {xirr_sip(st,tgt)*100:.1f}%/yr")
# Required monthly start for 10m at 15% return with 10% step
for r in [0.15,0.20]:
    _,v=sip(0.10,r); print("start needed for 10m at",r, round(35000*10e6/v))
    _,v=sip(0.10,r); print("start needed for 5m at",r, round(35000*5e6/v))
# Strategy comparison: DCA vs keeping 20% cash, simple illustration over a path with a 30% crash in year 2
import math
def path(kind):
    # monthly index path: +1.2%/m, crash -30% over months 13-18, recovery thereafter +1.8%/m
    p=[100.0]
    for t in range(1,61):
        if 13<=t<=18: p.append(p[-1]*(0.7**(1/6)))
        elif t>18: p.append(p[-1]*1.015)
        else: p.append(p[-1]*1.012)
    return p
p=path(0)
def run(strategy, step=0.10, cash_r=0.10):
    units=0; cash=0; m=35000; inv=0; peak=p[0]
    rc=(1+cash_r)**(1/12)-1
    for t in range(60):
        if t%12==0 and t>0: m*=1+step
        inv+=m; cash*=1+rc
        peak=max(peak,p[t]); dd=p[t]/peak-1
        if strategy=="A": units+=m/p[t]
        elif strategy=="B":
            units+=0.8*m/p[t]; cash+=0.2*m
            if dd<=-0.15 and cash>0: units+=cash/p[t]; cash=0
        elif strategy=="C":
            cash+=m
            if t%3==2: units+=cash/p[t]; cash=0
        elif strategy=="D":
            # base 70% invest, 30% to cash; deploy all cash when drawdown >=20%
            units+=0.7*m/p[t]; cash+=0.3*m
            if dd<=-0.20: units+=cash/p[t]; cash=0
    return inv, units*p[60]+cash
for s in "ABCD":
    inv,v=run(s); print(s, round(inv), round(v), f"{(v/inv-1)*100:.1f}%")
# no-crash steady path
p=[100*(1.012**t) for t in range(61)]
for s in "ABCD":
    inv,v=run(s); print("steady",s, round(inv), round(v), f"{(v/inv-1)*100:.1f}%")
