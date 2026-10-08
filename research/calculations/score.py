W=[15,12,10,18,5,10,10,8,5,7]
C=["Growth","Returns","Cash/BS","Valuation","Dividend","Moat/TAM","Visibility/Catalysts","Governance","Macro fit","Liquidity/Downside"]
S={
"OGDC":[4,7,5,9,7,6,6,5,8,8],
"FFC":[5,9,8,7,9,8,6,7,5,8],
"SYS":[9,7,7,5,3,8,7,7,9,6],
"LUCK":[6,6,6,8,4,8,7,8,5,7],
"HINOON":[8,8,7,7,7,7,8,8,4,5],
"MEBL":[6,10,8,5,6,9,6,8,5,8],
"ILP":[8,7,5,7,5,7,7,7,9,6],
"SAZEW":[8,8,6,9,4,5,6,6,3,4],
"UBL":[6,8,7,8,8,7,5,7,5,8],
"INDU":[4,7,8,9,9,4,3,8,3,6],
"PPL":[4,6,5,8,6,6,6,5,8,8],
"MARI":[5,8,8,6,5,7,7,6,8,7],
"EFERT":[4,8,7,6,8,7,4,7,4,8],
"HUBC":[4,7,4,8,9,5,4,6,6,7],
"FCCL":[5,6,6,7,4,6,6,6,4,7],
"MCB":[4,7,8,7,8,7,4,8,5,8],
"AIRLINK":[6,5,4,7,4,4,5,5,3,5],
"TGL":[3,6,6,8,5,5,4,6,4,4],
"PAEL":[5,4,3,6,2,5,5,4,4,4],
"KHAADI@15":[6,6,5,4,3,6,6,4,4,4],
}
assert sum(W)==100
out=[]
for k,v in S.items():
    tot=sum(w*s for w,s in zip(W,v))/10
    out.append((tot,k,v))
for i,(t,k,v) in enumerate(sorted(out,reverse=True),1):
    print(i,k,round(t,1),v)
