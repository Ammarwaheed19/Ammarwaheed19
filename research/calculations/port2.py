def sip(step, r, m0=35000, years=5):
    rm=(1+r)**(1/12)-1; v=0; inv=0; m=m0
    for y in range(years):
        for _ in range(12): v=v*(1+rm)+m; inv+=m
        m*=1+step
    return inv,v
for st in [0.05,0.10,0.15]:
    for k,r in {"Bear":0.0,"Base":0.14,"Bull":0.24}.items():
        inv,v=sip(st,r); inv2,v2=sip(st,r-0.06)
        print(f"{st:.0%} {k} {r:.0%}: inv {inv:,.0f} val {v:,.0f} profit {v-inv:,.0f} ({(v/inv-1)*100:.0f}%) noDRIP {v2:,.0f}")
# shares accumulated, base, 10% step
w={"FFC":0.25,"OGDC":0.20,"LUCK":0.20,"SYS":0.20,"HINOON":0.15}
px={"FFC":537.8,"OGDC":314.6,"LUCK":411,"SYS":150,"HINOON":925}
pg={"FFC":0.039,"OGDC":0.029,"LUCK":0.127,"SYS":0.127,"HINOON":0.15}  # base price CAGR
dy={"FFC":0.075,"OGDC":0.065,"LUCK":0.025,"SYS":0.02,"HINOON":0.045}
tot=0
for n in w:
    sh=0; m=35000; inv=0
    for t in range(60):
        if t%12==0 and t>0: m*=1.10
        P=px[n]*(1+pg[n])**(t/12)
        # dividends reinvested monthly
        sh+= sh*dy[n]/12*0  # placeholder
        sh+= m*w[n]/P; inv+=m*w[n]
        sh*= (1+dy[n]/12*1.0) if False else 1
    # approximate DRIP: add dividends reinvested at ~half-period
    P5=px[n]*(1+pg[n])**5
    # simulate DRIP properly
    sh2=0; m=35000
    for t in range(60):
        if t%12==0 and t>0: m*=1.10
        P=px[n]*(1+pg[n])**(t/12)
        sh2 += m*w[n]/P
        sh2 += sh2*(dy[n]/12)  # monthly dividend reinvested at current price (approx)
    val=sh2*P5; tot+=val
    print(f"{n}: invested {inv:,.0f} shares(no DRIP) {sh:,.0f} shares(DRIP) {sh2:,.0f} 2031 px {P5:,.0f} value {val:,.0f}")
print("total base value", round(tot))
