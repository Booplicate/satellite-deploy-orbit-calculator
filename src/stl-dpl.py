
__author__ = "Booplicate"
__version__ = "0.1.0"


import argparse
import json
import sys
from math import (
    pow,
    sqrt,
    # pi,
    tau
)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Satellite deploy orbit calculator. "
            "This helps calculate an orbit for deployment of N number of satellites all equally spread.\n"
            "The satellites must be deployed every time the carrier spacecraft passes its Ap"
        )
    )

    parser.add_argument("Ap", type=float, help="the target orbit apoapsis")
    parser.add_argument("Pe", type=float, help="the target orbit periapsis")
    parser.add_argument(
        "GM",
        type=float,
        help="the standard gravitational parameter of the astronomical body, aka μ"
    )
    parser.add_argument(
        "--R",
        type=float,
        default=0.0,
        help="the radius of the astronomical body (this is NOT required if Ap and Pe include it)"
    )
    parser.add_argument(
        "--n",
         type=int,
         default=3,
         help="the number of satellites to deploy, by default 3 (this is the minimum required for linking them together)"
    )
    # NOTE: I think it is impossible to achieve such an orbit
    parser.add_argument(
        "--preserve-order",
        action="store_true",
        help=argparse.SUPPRESS
        # help=(
        #     "by default the final order of the satellites after deployment is reversed.\n"
        #     "Consider you release the satellites in the following order: #1, #2, #3. "
        #     "Then their order from the top view of the orbit will be (counting clockwise): #3, #2, #1.\n"
        #     "Otherwise (if not reversed), they will be in the order of deployment (#1, #2, #3).\n"
        #     "In the later case, the main downside is that each satellite will have to carry extra fuel "
        #     "as their initial Pe will be lower than in the case of reversed deployment, where for "
        #     "the reversed approach the carrier spacecraft will carry the fuel to raise the Pe higher for all the satellites, "
        #     "which is usually more desirable. WARNING: using this flag can lead to Pe being negative or too low in atmosphere "
        #     "and thereby not suitable for use for some bodies/orbits combinations"
        # )
    )

    args = parser.parse_args()

    if args.Ap < args.Pe:
        raise ValueError("Apoapsis cannot be lower than periapsis")

    if args.Ap <= 0.0 or args.Pe <= 0.0:
        raise ValueError("Apoapsis and periapsis must be greater than 0")

    if args.GM <= 0.0:
        raise ValueError("GM must be greater than 0")

    if args.R <= 0.0:
        raise ValueError("Radius must be greater than 0")

    if args.n <= 1:
        raise ValueError("At least 2 satellites is required")

    return args


def cbrt(x) -> float:
    return pow(x, 1/3)

def calculate_semi_maj_axis(ap: float, pe: float) -> float:
    """
    Calculates semi-major axis of an orbit using its ap

    IN:
        ap - apoapsis
        pe - periapsis
    """
    return (ap + pe) / 2

def calculate_orbital_period(a: float, GM: float) -> float:
    """
    Calculates orbital period T

    IN:
        a - semi-major axis
        GM - GM, gravy const * mass
    """
    return sqrt(pow(a, 3) / GM) * tau

def calculate_pe(ap: float, GM: float, T: float) -> float:
    """
    Calculates periapsis for the period with the given apoapsis

    IN:
        ap - apoapsis
        GM - GM, gravy const * mass
        T - orbital period
    """
    # 2 * cbrt(GM * pow(T, 2) / pow(tau, 2)) - ap
    return 2 * cbrt(GM * pow(T/tau, 2)) - ap


def main():
    args = parse_args()

    R: float = args.R
    ap: float = args.Ap + R
    pe: float = args.Pe + R
    GM: float = args.GM
    TOTAL_SATELLITES: int = args.n

    if not args.preserve_order:
        T_FACTOR = 1 - 1 / TOTAL_SATELLITES
    else:
        T_FACTOR = 1 / TOTAL_SATELLITES

    target_orbit_a = calculate_semi_maj_axis(ap, pe)
    target_orbit_T = calculate_orbital_period(target_orbit_a, GM)

    deploy_orbit_T = target_orbit_T * T_FACTOR

    deploy_orbit_ap = ap - R
    deploy_orbit_pe = calculate_pe(ap, GM, deploy_orbit_T) - R

    target_orbit_ap = ap - R
    target_orbit_pe = pe - R

    rv = {
        "Ap": deploy_orbit_ap,
        "Pe": deploy_orbit_pe,
        "T": deploy_orbit_T,
        "Target Ap": target_orbit_ap,
        "Target Pe": target_orbit_pe,
        "Target T": target_orbit_T
    }

    json.dump(rv, sys.stdout, indent=4)

    return


if __name__ == "__main__":
    main()
