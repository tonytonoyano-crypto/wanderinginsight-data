import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from global_land_mask import globe
exec(open('code/ep01_figures.py').read().split("# 1 global map")[0])
res=json.load(open('assets/ep01/results.json')); la0,lo0,_=res['Eurasia']
R=6371.0088
def gc(a,b,c,d):
    a,b,c,d=map(np.radians,(a,b,c,d)); return 2*R*np.arcsin(np.sqrt(np.sin((c-a)/2)**2+np.cos(a)*np.cos(c)*np.sin((d-b)/2)**2))
def arc(a,b,c,d,n=60):
    p=lambda la,lo: np.array([np.cos(np.radians(la))*np.cos(np.radians(lo)),np.cos(np.radians(la))*np.sin(np.radians(lo)),np.sin(np.radians(la))])
    u,v=p(a,b),p(c,d); w=np.arccos(np.clip(u@v,-1,1)); t=np.linspace(0,1,n)
    pts=(np.sin((1-t)*w)[:,None]*u+np.sin(t*w)[:,None]*v)/np.sin(w)
    return np.degrees(np.arcsin(pts[:,2])),np.degrees(np.arctan2(pts[:,1],pts[:,0]))
LATg,LONg=np.meshgrid(lat,lon,indexing='ij'); ocean=globe.is_ocean(LATg,LONg)
d=gc(la0,lo0,LATg,LONg)
regs={'Arctic':ocean&(LATg>66),'Indian Ocean':ocean&(LATg<30)&(LONg>50)&(LONg<100),'Pacific':ocean&(LONg>118)&(LATg<66)&(LATg>0)}
fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=BG); ax=fig.add_axes([0.04,0.08,0.92,0.76])
sub=D[int((90-75)/0.1):int((90-0)/0.1),int((40+180)/0.1):int((150+180)/0.1)]
ax.imshow(np.ma.masked_invalid(sub),extent=[40,150,0,75],cmap=cm,vmin=0,vmax=2600,aspect='auto'); ax.set_facecolor('#D8E3E0'); ax.set_xticks([]); ax.set_yticks([])
out={}
cols={'Arctic':INK,'Indian Ocean':INK,'Pacific':INK}
for k,m in regs.items():
    i=np.argmin(np.where(m,d,1e9)); a,b=LATg.flat[i],LONg.flat[i]; out[k]=[float(a),float(b),float(d.flat[i])]
    la,lo=arc(la0,lo0,a,b); ax.plot(lo,la,color=INK,lw=3,ls='-' if k!='Pacific' else ':')
    ax.plot([b],[a],'o',ms=10,color=INK)
    off={'Arctic':(-30,3),'Indian Ocean':(-4,-8),'Pacific':(5,-2)}[k]
    ax.text(b+off[0] if k!='Arctic' else b-3,a+off[1],f'{k}: {d.flat[i]:,.0f} km',fontsize=17,weight='bold',color=INK,ha='left' if k!='Arctic' else 'right',bbox=dict(fc=BG,ec='none',alpha=.8,pad=2))
ax.plot(lo0,la0,'*',ms=34,mfc=WARM,mec=INK)
fig.text(0.04,0.93,'The tie that decides the answer',fontsize=34,weight='bold')
fig.text(0.04,0.885,'Eurasia\'s remotest point sits where the Arctic and the Indian Ocean are the same distance away.',fontsize=18)
fig.text(0.04,0.03,'Great-circle arcs drawn to the nearest ocean cell of each ocean (0.1° grid, ±10 km).',fontsize=12)
fig.savefig('assets/ep01/fig4_eurasia_tie.png',facecolor=BG); json.dump(out,open('assets/ep01/tie_distances.json','w')); print(out)
