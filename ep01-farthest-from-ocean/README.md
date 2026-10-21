# Ep01: Where is the farthest place on land from any ocean?

Code and results behind the WanderingInsight video *The Farthest Place on Land From Any Ocean Is in Northwest China*.

## The answer

Eurasia's remotest point is at about **44.35° N, 82.35° E** in Xinjiang, northwestern China: **2,512 km (1,561 miles)** from the nearest ocean. It sits there because two oceans tie. The nearest Arctic Ocean coast is 2,512 km away and the nearest Indian Ocean coast is 2,513 km away.

## The rules we used

Change these and the point moves. That's the point of publishing the code.

- **Land/sea mask:** GLOBE-derived global land mask (about 1 km), via the [`global-land-mask`](https://pypi.org/project/global-land-mask/) Python package.
- **Grid:** one point every 0.1° (about 7 miles).
- **Distance:** great-circle distance to the nearest coastal ocean cell, on a sphere of radius 6,371 km.
- **What counts as ocean:** seas connected to the ocean (the Mediterranean, Black Sea, Baltic, Hudson Bay and the Gulf of Ob) count as ocean.
- **What counts as land:** lakes count as land, and so do the Caspian and the Aral Sea. Antarctica's ice sheet counts as land.
- **"Half of all land":** an *area-weighted* median, which leaves out Antarctica. Each grid cell is weighted by cos(latitude), because cells shrink towards the poles. Without the weighting you'd get 374 km. With it you get 427 km (265 miles), the figure in the video.

## Every number in the video

| In the video | From `assets/ep01/results.json` |
|---|---|
| Farthest point: about 1,560 miles from any sea | `Eurasia_mi`: 1,560.7 |
| A tie: Arctic vs Indian Ocean | `tie_distances.json`: 2,511.8 km vs 2,513.2 km |
| Half of all land within about 265 miles of the sea | `median_land_distance_mi`: 265.6 |
| About one fifth of land beyond 600 miles | `share_land_beyond_600mi_%`: 21.4 |
| Fewer than one in twenty places beyond 1,000 miles | `share_land_beyond_1000mi_%`: 4.6 |
| About 1.5% beyond 1,250 miles | `share_land_beyond_1250mi_%`: 1.4 |
| Remotest points on other continents | `Africa`, `North America`, `South America`, `Australia`, `Antarctica` (km) |

We checked our Eurasian point against Garcia-Castellanos & Lombardo (2007), *Poles of Inaccessibility: A Calculation Algorithm for the Remotest Places on Earth*, Scottish Geographical Journal 123(3): 227–233.

## Change the rules yourself

| Script | What it does | Result |
|---|---|---|
| `code/ep01_variant_ob.py` | Treats the Gulf of Ob as land, as older estimates did | Point moves to 44.45° N, 82.15° E; 2,528 km |
| `code/ep01_variant_arctic.py` | Ignores the Arctic Ocean entirely (north of 66° N) | Point jumps north to 49.25° N; 2,984 km |

## Run it

```bash
pip install -r ../requirements.txt
cd ep01-farthest-from-ocean
python code/ep01_ocean_distance.py   # about 20 s; writes results.json and the distance grid
python code/ep01_figures.py          # four charts
python code/ep01_fig4b.py            # the tie map with arcs to each ocean
python code/ep01_variant_ob.py       # rule changes
python code/ep01_variant_arctic.py
python code/ep01_flood_anim.py       # optional: 96 frames of the "flooding" map animation
```

Run the scripts from inside this folder, because they use relative paths. `ep01_ocean_distance.py` has to run first, since it builds the distance grid the others read.

Found a definition that moves the point somewhere new? Open an issue or tell us in the video's comments.
