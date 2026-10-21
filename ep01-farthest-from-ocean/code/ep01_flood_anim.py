import numpy as np, matplotlib, json, os
os.makedirs('assets/ep01/flood',exist_ok=True)
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
BG='#F4EBD9'; INK='#2B2A28'; WARM='#B5502B'
D=np.load('assets/ep01/D_land_to_ocean.npy'); res=json.load(open('assets/ep01/results.json'))
cm=LinearSegmentedColormap.from_list('p',['#EFE3C6','#D9C99A','#B9A06A','#8C8A5A','#4F7A6A','#1F6F78','#12404A'])
sub=D[int((90-83)/0.1):int((90+60)/0.1)]
water=np.isnan(sub)
N=96
fig=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=BG)
ax=fig.add_axes([0.02,0.02,0.96,0.80]); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
t=fig.text(0.03,0.93,'Distance from the nearest ocean',fontsize=34,weight='bold',color=INK)
c=fig.text(0.97,0.93,'',fontsize=34,weight='bold',color=INK,ha='right')
for i in range(N):
    e=i/(N-1); r=2600*(e**1.2)
    img=np.where(water,np.nan,np.where(sub<=r,sub,np.nan))
    ax.clear(); ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor('#D8E3E0')
    for s in ax.spines.values(): s.set_visible(False)
    base=np.where(water,np.nan,1.0)
    ax.imshow(np.ma.masked_invalid(base),extent=[-180,180,-60,83],cmap=LinearSegmentedColormap.from_list('b',['#E9E1CF','#E9E1CF']),aspect='auto',interpolation='nearest')
    ax.imshow(np.ma.masked_invalid(img),extent=[-180,180,-60,83],cmap=cm,vmin=0,vmax=2600,aspect='auto',interpolation='nearest')
    c.set_text(f'{int(r):,} km')
    if i>=N-8:
        la,lo,d=res['Eurasia']; ax.plot(lo,la,'*',ms=34,mfc=WARM,mec=INK)
        ax.annotate('2,512 km',(lo,la),xytext=(lo+8,la+10),fontsize=22,weight='bold',color=INK)
    fig.savefig(f'assets/ep01/flood/f{i:03d}.png',facecolor=BG)
print('frames ok')
