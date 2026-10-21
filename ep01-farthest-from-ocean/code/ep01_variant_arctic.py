import json, numpy as np
exec(open('code/ep01_ocean_distance.py').read().split("ocean=~land")[0])
ocean=~land
arc=ocean&(LAT>=66)
ocean_v=ocean&~arc
Dv=dist_to(ocean_v,land|arc,LAT,LON)
sel=(LON>=-10)&(LON<=180)&(LAT>=5)&(LAT<=66)&~np.isnan(Dv)
i=np.nanargmax(np.where(sel,Dv,-1))
r={'variant_ignore_arctic_ocean':[float(LAT.flat[i]),float(LON.flat[i]),float(Dv.flat[i])]}
print(r); json.dump(r,open('assets/ep01/results_variant_arctic.json','w'))
np.save('assets/ep01/D_variant_arctic.npy',Dv.astype('float32'))
