# [Satellite deploy orbit calculator](https://github.com/Booplicate/satellite-deploy-orbit-calculator) - deploying satellites has never been so easy. Almost like it's not rocket science anymore.

### Description
A tool to calculate an orbit for deployment of N equally spread satellites in a single launch.

### Usage
Help is available via `python stl-dpl.py -h`

Example:
- `python stl-dpl.py --R 600000 --n 3 2863334.06 2863334.06 3531600000000`

Output:
```json
{
    "Ap": 2863334.06,
    "Pe": 1222703.0402694033,
    "T": 14366.283458574184,
    "Target Ap": 2863334.06,
    "Target Pe": 2863334.06,
    "Target T": 21549.425187861274
}
```

From which we can see that the carrier will need an orbit with Ap and Pe 2863334.06 m 1222703.04 m respectively, and its orbital period will be 14366.28 s, about 0.6(6) times of the targeted satelites orbit.

In this case the eccentricity of the target orbit is 0 (circular orbit, Ap is equal to Pe), but it does not have to be, generally.

We also separately specified the radius of the body (`--R`), alternatively it could be included into the Ap and Pe parameters.

Result:
- 3 satelites evenly spread with mean anomaly difference 33.3(3)% from each other
- on a circular orbit with Apogee 2863.334 km
- with the body radius 600 km
- and the body GM (standard gravitational parameter or μ) 3.5316*10^12 m^3/s^2

### Requirements
 - `Python 3.10.9`
