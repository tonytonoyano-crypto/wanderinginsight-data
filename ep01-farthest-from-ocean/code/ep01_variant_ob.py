import json, numpy as np, sys
sys.argv=['x']
exec(open('code/ep01_ocean_distance.py').read().split("ocean=~land")[0])
ocean=~land
# Variant: treat the Gulf of Ob as land (as the pre-2007 estimate did)
ob=(LON>=64)&(LON<=76)&(LAT>=65)&(LAT<=73)
ocean_v=ocean&~ob
Dv=dist_to(ocean_v,land|(ocean&ob),LAT,LON)
sel=(LON>=-10)&(LON<=180)&(LAT>=5)&(LAT<=80)&~np.isnan(Dv)&~(ob)
i=np.nanargmax(np.where(sel,Dv,-1))
r={'variant_gulf_of_ob_as_land':[float(LAT.flat[i]),float(LON.flat[i]),float(Dv.flat[i])]}
# top-5 distinct candidates by distance for default
D=np.load('assets/ep01/D_land_to_ocean.npy')
print(r)
json.dump(r,open('assets/ep01/results_variant.json','w'))
np.save('assets/ep01/D_variant_ob.npy',Dv.astype('float32'))
