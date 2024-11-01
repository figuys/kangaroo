# Import required libraries in Python equivalent for operations.
from random import randint

from code.keyhuntPy.Kangaroo import PollardKangaroo

from code.keyhuntPy.ECPoint import ECPoint

# Elliptic Curve j parameters
# Constants are defined for secp256k1 curve
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Field prime
A = 0  # Curve coefficient A for secp256k1
B = 7  # Curve coefficient B for secp256k1
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798  # Generator point x-coordinate
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8  # Generator point y-coordinate
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # Order of the group


# A simple class to represent Points on the curve (with point at infinity as None)


# Function to perform modular inverse
def mod_inv(a, p):
    """Compute the modular inverse of a modulo p."""
    return pow(a, p - 2, p)


# Function to add two points on the secp256k1 curve
def ec_add(p1, p2, P):
    if p1.is_infinity():
        return p2
    if p2.is_infinity():
        return p1

    if p1.x == p2.x and p1.y != p2.y:
        # Point at infinity
        return ECPoint(None, None)

    if p1.x == p2.x:
        # Doubling case
        s = (3 * p1.x ** 2) * mod_inv(2 * p1.y, P) % P
    else:
        # General addition case
        s = (p2.y - p1.y) * mod_inv(p2.x - p1.x, P) % P

    x3 = (s ** 2 - p1.x - p2.x) % P
    y3 = (s * (p1.x - x3) - p1.y) % P
    return ECPoint(x3, y3)


# Function to perform scalar multiplication on the secp256k1 curve
def scalar_mult(k, point, P):
    result = ECPoint(None, None)  # Start with the point at infinity
    addend = point

    while k:
        if k & 1:
            result = ec_add(result, addend, P)
        addend = ec_add(addend, addend, P)
        k >>= 1

    return result
# Modify the Pollard Kangaroo class for smaller steps and predefined jump table to improve performance

# Initialize the optimized algorithm with curve parameters
pollard_kangaroo_opt = PollardKangaroo(N, G, max_steps=100)

# Sample parameters for a small test run
target_value = 50  # Hypothetical target for easier testing
start_point = scalar_mult(randint(1, N), G, P)  # Random start for wild kangaroo

# Run the tame kangaroo (controlled jumps towards target value)
pollard_kangaroo_opt.tame_positions = {}  # Initialize storage for tame kangaroo positions
tame_point, tame_steps = pollard_kangaroo_opt.tame_kangaroo(G, target_value)

# Run the wild kangaroo (random jumps to find the tame kangaroo)
wild_steps = pollard_kangaroo_opt.wild_kangaroo(start_point)

tame_point, tame_steps, wild_steps  # Display results from tame and wild kangaroos


# Testing the defined functions with secp256k1 generator point G
G = ECPoint(Gx, Gy)
test_scalar = 2
result_point = scalar_mult(test_scalar, G, P)

result_point  # Display the result of scalar multiplication (2 * G)
