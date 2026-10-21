import json, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
BG='#F4EBD9'; INK='#2B2A28'; ACC='#1F6F78'; WARM='#B5502B'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK})
D=np.load('assets/ep01/D_land_to_ocean.npy'); res=json.load(open('assets/ep01/results.json'))
lat=np.arange(-89.95,90,0.1)[::-1]; lon=np.arange(-179.95,180,0.1)
cm=LinearSegmentedColormap.from_list('p',['#EFE3C6','#D9C99A','#B9A06A','#8C8A5A','#4F7A6A','#1F6F78','#12404A'])
def base(figsize=(19.2,10.8)):
    fig=plt.figure(figsize=figsize,dpi=100,facecolor=BG); return fig
# 1 global map
fig=base(); ax=fig.add_axes([0.02,0.11,0.96,0.76])
Dm=np.ma.masked_invalid(D)
im=ax.imshow(Dm[int((90-83)/0.1):int((90+60)/0.1)],extent=[-180,180,-60,83],cmap=cm,vmin=0,vmax=2600,aspect='auto',interpolation='nearest')
ax.set_facecolor('#D8E3E0'); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
pts={'Eurasia':('Eurasia\n2,510 km',WARM),'North America':('North America\n1,640 km',WARM),'Africa':('Africa\n1,820 km',WARM),'South America':('South America\n1,530 km',WARM),'Australia':('Australia\n940 km',WARM)}
for k,(t,c) in pts.items():
    la,lo,d=res[k]; ax.plot(lo,la,'o',ms=11,mfc=INK,mec=BG,mew=2); ax.annotate(t,(lo,la),xytext=(lo+6,la+8),fontsize=15,color=INK,weight='bold')
fig.text(0.03,0.93,'How far from the ocean can you get on land?',fontsize=34,weight='bold')
fig.text(0.03,0.89,'Distance from every land point to the nearest ocean-connected water. Dots mark each continent\'s remotest point.',fontsize=17)
cax=fig.add_axes([0.62,0.075,0.33,0.016]); cb=fig.colorbar(im,cax=cax,orientation='horizontal'); cb.set_label('km to nearest ocean (capped at 2,600)',fontsize=12); cb.ax.tick_params(labelsize=11)
fig.text(0.03,0.012,'Method: ~1 km global land mask, 0.1° grid, great-circle distance. Lakes and the Caspian count as land; the Mediterranean, Black Sea, Baltic and Arctic count as ocean.',fontsize=11)
fig.savefig('assets/ep01/fig1_global_map.png',facecolor=BG); plt.close(fig)
# 2 share beyond X
fig=base(); ax=fig.add_axes([0.08,0.12,0.86,0.72]); ax.set_facecolor(BG)
land=~np.isnan(D); LAT=np.repeat(lat[:,None],len(lon),1); w=np.cos(np.radians(LAT)); m=land&(LAT>-60)
xs=np.arange(0,2600,25); ys=[100*w[m&(D>x)].sum()/w[m].sum() for x in xs]
ax.fill_between(xs,ys,color=ACC,alpha=.25); ax.plot(xs,ys,color=ACC,lw=4)
for x in (500,1000,2000):
    y=100*w[m&(D>x)].sum()/w[m].sum(); pct=f'{y:.0f}' if y>=10 else f'{y:.1f}'
    ax.plot([x],[y],'o',ms=12,color=WARM); ax.annotate(f'{pct}% of land is\nmore than {x:,} km\nfrom the ocean',(x,y),xytext=(x+60,y+8),fontsize=17,weight='bold')
med=res['median_land_distance_km']  # area-weighted median, from ep01_ocean_distance.py
ax.axvline(med,color=INK,ls='--',lw=2); ax.text(med+15,3,f'half of all land:\n{med:.0f} km ({med/1.609344:.0f} mi)',fontsize=15)
ax.set_xlabel('distance to nearest ocean (km)',fontsize=16); ax.set_ylabel('% of land area (excluding Antarctica)',fontsize=16)
for s in ('top','right'): ax.spines[s].set_visible(False)
ax.tick_params(labelsize=14); ax.set_ylim(0,100); ax.set_xlim(0,2600)
fig.text(0.08,0.92,f'Half of all land is within about {round(med,-1):.0f} km ({5*round(med/1.609344/5):.0f} miles) of the ocean',fontsize=32,weight='bold')
fig.savefig('assets/ep01/fig2_share_beyond.png',facecolor=BG); plt.close(fig)
# 3 bar of poles
fig=base(); ax=fig.add_axes([0.2,0.14,0.74,0.68]); ax.set_facecolor(BG)
names=['Eurasia','Africa','North America','South America','Antarctica*','Australia']
vals=[res['Eurasia'][2],res['Africa'][2],res['North America'][2],res['South America'][2],res['Antarctica'][2],res['Australia'][2]]
order=np.argsort(vals); ax.barh(np.array(names)[order],np.array(vals)[order],color=[ACC if n!='Antarctica*' else '#9AA7A5' for n in np.array(names)[order]],height=.65)
for i,v in enumerate(np.array(vals)[order]): ax.text(v+25,i,f'{v:,.0f} km',va='center',fontsize=18,weight='bold')
ax.set_xlim(0,3100); ax.tick_params(labelsize=18); ax.set_xlabel('distance from the continent\'s remotest point to the ocean (km)',fontsize=15)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.text(0.04,0.92,'Remotest point on each continent',fontsize=32,weight='bold'); fig.text(0.04,0.04,'*Antarctica counts the ice sheet as land.',fontsize=12)
fig.savefig('assets/ep01/fig3_poles_bar.png',facecolor=BG); plt.close(fig)
# 4 Eurasia tie map
fig=base(); ax=fig.add_axes([0.04,0.08,0.92,0.76]); sub=D[int((90-75)/0.1):int((90-0)/0.1),int((40+180)/0.1):int((150+180)/0.1)]
ax.imshow(np.ma.masked_invalid(sub),extent=[40,150,0,75],cmap=cm,vmin=0,vmax=2600,aspect='auto'); ax.set_facecolor('#D8E3E0'); ax.set_xticks([]); ax.set_yticks([])
la,lo,d=res['Eurasia']; ax.plot(lo,la,'*',ms=30,mfc=WARM,mec=INK)
ax.annotate('Remotest point in Eurasia\n44.4°N, 82.4°E · 2,510 km\nArctic and Indian Ocean\nare almost exactly tied',(lo,la),xytext=(lo+14,la+14),fontsize=18,weight='bold',arrowprops=dict(arrowstyle='-',color=INK,lw=2))
fig.text(0.04,0.92,'The tie that decides the answer',fontsize=32,weight='bold')
fig.savefig('assets/ep01/fig4_eurasia_tie.png',facecolor=BG); plt.close(fig)
print('ok')
