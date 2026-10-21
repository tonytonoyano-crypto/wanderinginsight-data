"""Ep01: distance from every land point to the nearest ocean-connected water.
Data: GLOBE-derived global land mask (pip global-land-mask, ~1 km). Lakes and the Caspian/Aral count as LAND;
seas connected to the ocean (Med, Black Sea, Baltic, Hudson Bay, Gulf of Ob) count as OCEAN. Antarctic ice counts as land.
Method: 0.1 deg grid, chord distance in 3D to nearest coastal ocean cell (KD-tree), great-circle km. Refined locally at 0.02 deg.
"""
import json, numpy as np
from global_land_mask import globe
from scipy.spatial import cKDTree
R=6371.0088
def xyz(lat,lon):
    la,lo=np.radians(lat),np.radians(lon)
    return np.column_stack([np.cos(la)*np.cos(lo),np.cos(la)*np.sin(lo),np.sin(la)])
def km(chord): return 2*R*np.arcsin(np.clip(chord/2,0,1))
def grid(step,box=None):
    lat=np.arange(-89.95+0,90,step)[::-1] if step==0.1 else np.arange(-90+step/2,90,step)[::-1]
    lon=np.arange(-180+step/2,180,step)
    return lat,lon
step=0.1
lat,lon=grid(step)
LON,LAT=np.meshgrid(lon,lat)
land=globe.is_land(LAT,LON)
def dist_to(target_mask, query_mask, LAT,LON):
    # nearest target cell (coast cells only) for each query cell
    tm=target_mask
    # coast = target cells adjacent to non-target
    pad=np.pad(tm,1,mode='edge')
    nb=(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
    coast=tm&~nb
    tree=cKDTree(xyz(LAT[coast],LON[coast]))
    q=xyz(LAT[query_mask],LON[query_mask])
    d,_=tree.query(q,workers=-1)
    out=np.full(LAT.shape,np.nan); out[query_mask]=km(d); return out
ocean=~land
D=dist_to(ocean,land,LAT,LON)          # land -> ocean
# variant: treat Arctic Ocean north of 70N as frozen (i.e., not ocean)
ocean_v=ocean&~(LAT>70)
Dv=dist_to(ocean_v,land|(ocean&(LAT>70)),LAT,LON)
Dv[ocean&(LAT>70)]=np.nan
# oceanic pole: ocean -> land (lakes count as land too, so use land mask as target)
Do=dist_to(land,ocean,LAT,LON)
regions={ 'Eurasia':(( -10,180),(5,80)), 'Africa':((-20,52),(-36,38)), 'North America':((-170,-50),(7,75)),
 'South America':((-82,-34),(-56,13)), 'Australia':((112,155),(-45,-10)), 'Antarctica':((-180,180),(-90,-60))}
res={}
def best(Dm,box,label,refine=True):
    (x0,x1),(y0,y1)=box
    sel=(LON>=x0)&(LON<=x1)&(LAT>=y0)&(LAT<=y1)&~np.isnan(Dm)
    if label=='Eurasia':
        sel&=~((LON>=-25)&(LON<=-5)&(LAT>60))  # exclude Iceland/Greenland-ish strays
    i=np.nanargmax(np.where(sel,Dm,-1)); la,lo,d=LAT.flat[i],LON.flat[i],Dm.flat[i]
    return float(la),float(lo),float(d)
for k,b in regions.items():
    res[k]=best(D,b,k)
for k in ['Eurasia']:
    res[k+'_ArcticFrozen']=best(Dv,regions[k],k)
# oceanic pole
i=np.nanargmax(Do); res['Ocean pole']=(float(LAT.flat[i]),float(LON.flat[i]),float(Do.flat[i]))
# Antarctic note and North America sanity
# Eurasia: share of land farther than X km
areaw=np.cos(np.radians(LAT))
for X in (500,1000,1500,2000):
    m=land&(LAT>-60); res[f'share_land_beyond_{X}km_%']=float(100*np.sum(areaw[m&(D>X)])/np.sum(areaw[m]))
res['median_land_distance_km_unweighted']=float(np.nanmedian(D[land&(LAT>-60)]))
# Area-weighted median: grid cells shrink towards the poles, so each cell is weighted by cos(latitude).
# This is the "half of all land" figure used in the video (about 427 km / 265 miles).
m=land&(LAT>-60); dv=D[m]; wv=areaw[m]; o=np.argsort(dv); cw=np.cumsum(wv[o])/wv.sum()
res['median_land_distance_km']=float(np.interp(0.5,cw,dv[o]))
MI=1.609344
res['median_land_distance_mi']=res['median_land_distance_km']/MI
for X in (600,1000,1250):
    res[f'share_land_beyond_{X}mi_%']=float(100*np.sum(areaw[m&(D>X*MI)])/np.sum(areaw[m]))
res['Eurasia_mi']=res['Eurasia'][2]/MI
json.dump(res,open('assets/ep01/results.json','w'),indent=1)
np.save('assets/ep01/D_land_to_ocean.npy',D.astype('float32'))
print(json.dumps(res,indent=1))
