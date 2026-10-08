# Khaadi IPO calculations. All inputs documented in report.
post_sh = 2500.0   # mn shares post-IPO (500mn = 20%)
pre_sh  = 2000.0   # mn shares pre-issue (assumes both tranches primary)
floor = 12.40
pat = {"FY23(Jun)":962,"6M Dec23":365,"CY24":1398,"CY25":1668,"1H26":1606,"CY26E mgmt":3100,"CY27E mgmt":4800}
rev = {"FY23(Jun)":27002,"6M Dec23":13135,"CY24":24598,"CY25":25130,"1H26":17080}
print("== Margins ==")
for k in rev: print(k, f"net margin {pat[k]/rev[k]*100:.1f}%")
print("CY25 op margin", 3200/25130*100, "1H26 op margin", 2600/17080*100, "1H26 GM", 6300/17080*100)
print("Gross/net 1H26", 22252/17080)
print("CY25 rev growth vs CY24", (25130/24598-1)*100)
print("CY24 annual vs FY23", (24598/27002-1)*100)
print("PAT CAGR FY23->CY25 (2.5y)", ((1668/962)**(1/2.5)-1)*100)
print("PAT CY24->CY25", (1668/1398-1)*100)
print("Mgmt CY26 vs CY25", (3100/1668-1)*100, "CY27 vs CY26", (4800/3100-1)*100, "CY25->CY27 CAGR", ((4800/1668)**0.5-1)*100, "multiple", 4800/1668)
print("2H26 implied", 3100-1606)
# EPS
for k,v in pat.items(): print(k, "EPS post", round(v/post_sh,3), "EPS pre", round(v/pre_sh,3))
# Normalised scenarios (my assumptions)
norm = {"CY26 base":2900,"CY27 base":3800,"CY26 bear":2500,"CY27 bear":2800}
print("== Valuation grid ==")
D = 3000.0  # ASSUMED pre-IPO net financial debt (ex-lease), Rs mn -- NOT VERIFIED
EBIT_CY25 = 3200; EBIT_1H26 = 2600
EBIT_CY26E = 5600  # assumption: ~ (2600*2.15) loosely; used only for EV/EBIT illustration
rows=[]
for p in [12.40,13,14,15,16,17,18]:
    mcap = post_sh*p
    pre_price = (floor+p)/2
    proceeds = 250*pre_price + 250*p
    ev = mcap + D - proceeds
    r = dict(price=p, pre_ipo_px=round(pre_price,2), proceeds=round(proceeds), mcap=round(mcap), pre_money=round(pre_sh*p), ev=round(ev),
             pe_cy25=round(mcap/1668,1), pe_cy26m=round(mcap/3100,1), pe_cy27m=round(mcap/4800,1),
             pe_cy26b=round(mcap/2900,1), pe_cy27b=round(mcap/3800,1),
             ev_sales_cy25=round(ev/25130,2), ev_ebit_cy25=round(ev/3200,1), mcap_usd=round(mcap/278,1))
    rows.append(r); print(r)
# Rs10 face-value equivalent
for p in [12.40,15,18]: print("Rs10-equivalent price", p*80, "EPS CY25 Rs10 basis", 1668/(post_sh/80))
# Dividend % of par illustration
for pct in [10,50,100,500,1000]:
    d = 0.125*pct/100
    print(f"{pct}% dividend = Rs{d:.4f}/sh -> yield at 12.4: {d/12.4*100:.2f}%, at 18: {d/18*100:.2f}%")
# IFC cross-check
print("IFC implied post-money group USD mn", 25/0.20)
for p in [12.4,18]: print("pre-money Khaadi PK", p, pre_sh*p, "USD mn", pre_sh*p/278)
# Book value upper bound
eq_dec23 = 8600; ret = 1398+1668+1606
for p in [12.4,15,18]:
    proceeds = 250*(floor+p)/2 + 250*p
    eq_post = eq_dec23+ret+proceeds
    print("price",p,"post equity UB",eq_post,"BVPS",round(eq_post/post_sh,2),"P/B",round(p/(eq_post/post_sh),2))
# Experience store payback sensitivity
capex_store = 3387/8
print("capex per store", capex_store)
for inc_sales in [300,500,800,1200]:
    for m in [0.15,0.20,0.25]:
        print(f"inc sales {inc_sales} store-EBITDA margin {m}: payback yrs {capex_store/(inc_sales*m):.1f}")
