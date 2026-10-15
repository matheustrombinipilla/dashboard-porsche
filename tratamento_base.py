import pandas as pd, json, re
SRC='planilha_original.xlsx'  # coloque a planilha original na mesma pasta do script
df=pd.read_excel(SRC,dtype=str)

# conferência: preço sanitizado x preço bruto interpretado de forma independente
def parse_raw(s):
    s=s.lower().replace('usd','').replace('dollars','').replace('$','').strip()
    k=s.endswith('k'); s=s.rstrip('k').strip()
    if re.fullmatch(r'\d{1,3}(\.\d{3})+',s): s=s.replace('.','')
    s=s.replace(',','')
    try: return float(s)*(1000 if k else 1)
    except ValueError: return float('nan')
raw=df.sale_price.map(parse_raw); san=df.SalesPriceSanitized.astype(float)
print('preços em texto por extenso (não conferidos):',raw.isna().sum()); print(df.loc[raw.isna(),['sale_price','SalesPriceSanitized']].to_string())
bad=df[(raw-san).abs()>1]
print('divergências preço bruto x sanitizado:',len(bad)); print(bad[['sale_price','SalesPriceSanitized']].head())

def fam(m):
    for f in ('911','718','Cayenne','Macan','Panamera','Taycan'):
        if m.startswith(f): return f
    raise ValueError(m)
STATUS={'Delivered':'Entregue','In Transit':'A caminho','Shipped':'A caminho','Awaiting Delivery':'A caminho','Awaiting Pickup':'A caminho',
        'Pending':'Em análise','Pending Approval':'Em análise','Pending Review':'Em análise','Awaiting Review':'Em análise','Cancelled':'Cancelada'}
out=pd.DataFrame({
 'id':df.sale_id.astype(int),
 'modelo':df.PorscheModelSanitized,
 'familia':df.PorscheModelSanitized.map(fam),
 'ano':df.ModelYearSanitized.astype(int),
 'preco':df.SalesPriceSanitized.astype(float).round(0).astype(int),
 'milhas':df.VehicleMileageSanitized.astype(float).round(0).astype(int),
 'pagamento':df.PayMethodSanitized,
 'cidade':df.CitySanitized,
 'estado':df.StateSanitized,
 'status_original':df.DeliveryStatusSanitized,
 'status':df.DeliveryStatusSanitized.map(STATUS),
 'data_valida':df.SaleDateSanitized.where(df.SaleDateSanitized!='INVALID',''),
})
assert out.status.notna().all() and out.isna().sum().sum()==0
out.to_csv('base_tratada.csv',index=False)
json.dump(out.drop(columns=['data_valida']).to_dict('records'),open('data.json','w'),ensure_ascii=False,separators=(',',':'))
print(out.shape, out.preco.sum(), out.groupby('status').preco.agg(['count','sum']))
print(out.groupby('familia').preco.agg(['count','sum','mean']).round(0))
print(out.groupby('pagamento').preco.agg(['count','sum','mean']).round(0).sort_values('sum',ascending=False))
inv=(out.data_valida=='').sum(); fut=(out.data_valida>'2026-10-14').sum(); print('datas inválidas',inv,'futuras',fut)
