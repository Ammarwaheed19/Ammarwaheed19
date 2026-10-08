sh=2500.0
# --- Khaadi 2026-2031 scenarios (PAT Rs mn, revenue Rs mn) ---
sc = {
 "Bear": dict(rev26=31000, rev_g=[0.08,0.08,0.07,0.07,0.07], pat26=2500, pat27=2800, pat_g=0.06, pe=(6,7), payout=0.35),
 "Base": dict(rev26=33000, rev_g=[0.16,0.14,0.13,0.12,0.12], pat26=2900, pat27=3800, pat_g=0.14, pe=(8,10), payout=0.45),
 "Bull": dict(rev26=34000, rev_g=[0.25,0.20,0.18,0.17,0.16], pat26=3100, pat27=4800, pat_g=0.18, pe=(11,13), payout=0.50),
}
res={}
for name,s in sc.items():
    revs=[s["rev26"]]; 
    for g in s["rev_g"]: revs.append(revs[-1]*(1+g))
    pats=[s["pat26"],s["pat27"]]
    for i in range(4): pats.append(pats[-1]*(1+s["pat_g"]))
    years=list(range(2026,2032))
    print(f"\n== {name} ==")
    divs=[]
    for y,r,p in zip(years,revs,pats):
        eps=p/sh; lo,hi=s["pe"]
        print(f"{y}: Rev {r:,.0f}  PAT {p:,.0f}  NetM {p/r*100:.1f}%  EPS {eps:.2f}  P/E {lo}-{hi}x -> Rs{eps*lo:.1f}-{eps*hi:.1f}")
        divs.append(eps*s["payout"])
    eps31=pats[-1]/sh
    res[name]=(eps31*s["pe"][0], eps31*s["pe"][1], sum(divs[1:]))  # dividends paid 2027-2031 approx
    print("2031 price range", res[name], "cum dividends 2027-31 (approx)", round(sum(divs[1:]),2))
# --- IRR from IPO prices (entry Dec-2026, exit Dec-2031, 5 yrs) ---
print("\n== Annualised return to 2031 (price only | incl. dividends, simple) ==")
for name,(lo,hi,cd) in res.items():
    mid=(lo+hi)/2
    line=[]
    for p in [12.40,13,14,15,16,17,18]:
        pr=(mid/p)**(1/5)-1
        tr=((mid+cd)/p)**(1/5)-1
        line.append(f"{p}:{pr*100:.1f}%|{tr*100:.1f}%")
    print(name, f"mid 2031 Rs{mid:.1f}", " ".join(line))
# --- Growth-rate sensitivity grid ---
print("\n== 2031 price by EPS growth (base CY26 EPS 1.16 = 2.9bn/2.5bn) ==")
eps26=2900/sh
for g in [0.05,0.10,0.15,0.20,0.25,0.30]:
    e31=eps26*(1+g)**5
    print(f"g={g*100:.0f}%: EPS31 {e31:.2f} | P/E8 {e31*8:.1f} | P/E10 {e31*10:.1f} | P/E12 {e31*12:.1f} | CAGR from 15 @P/E10 {((e31*10)/15)**0.2*100-100:.1f}%")
print("Historical: PAT CAGR FY23->CY25 24.6% (rate-cut aided); revenue CY24->CY25 +2.2%")
