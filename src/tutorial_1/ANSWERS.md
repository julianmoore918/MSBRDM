# Answers to Questions

## Exercise 1

### Q2

Every elementary rotation R_x, R_y, R_z has det = +1. Since det(AB) = det(A)·det(B), any composition of rotations also has det = +1. This is the closure property of SO(3) = {R | RRᵀ = I, det R = +1}.

The frames O3 and O5 have det(R) = −1. They are left-handed (z ≠ x × y), so R ∉ SO(3). It is an improper rotation, which includes a reflection. Therefore H = [[R, t], [0, 1]] ∉ SE(3), which requires R ∈ SO(3). No sequence of basic rotations can produce these frames; a reflection such as diag(1, 1, −1) is needed.

## Exercise 2

### Q4

HS1 rotates about the current (moving) axes x0 → y0′ → z0″, so the rotations are post-multiplied: R1 = Rx(90) @ Ry(45) @ Rz(30).
HS2 rotates about the fixed axes x0 → y0 → z0, so the rotations are pre-multiplied: R2 = Rz(30) @ Ry(45) @ Rx(90).

Rotation matrices do not commute, so with the same three angles R1 ≠ R2 and the two pentagons end up with different orientations. R1 can also be written as a fixed-axes rotation, but with other angles (45°, −30°, 90°). The translations are both along the fixed axes; they only differ in the sign of y (+0.75 vs −0.75), which places the pentagons on opposite sides.

Implementation: for cleaner code I added the helper function Rzyx(phi, theta, psi) = RotZ(phi) @ RotY(theta) @ RotX(psi) to rotation.py (roll-pitch-yaw, eq. (10)). It directly gives the fixed-axes sequence HS2 = Rzyx(30°, 45°, 90°). HS1 (current axes) has the reverse order Rx · Ry · Rz, so with Rzyx it needs the equivalent fixed-axes angles Rzyx(45°, −30°, 90°) (obtained with R2EulerA and checked to give the same matrix as RotX(90) @ RotY(45) @ RotZ(30)).

Aspect ratio: yes, preserved. HS1 and HS2 are in SE(3) (R ∈ SO(3), last row [0 0 0 1]), i.e. rigid transformations:

|(R p1 + t) − (R p2 + t)| = |R (p1 − p2)| = |p1 − p2|

Distances and angles are kept, so all sides stay L = 1 and the pentagon stays regular; it is only moved and rotated.

### Q5

A last row [a b c d] makes HS3 a projective (non-SE(3)) transform:
HS3 [p; 1] = [R p + t; w], with w = a·x + b·y + c·z + d. After dividing by w:

- a = b = c = 0: uniform scaling by 1/d (shape kept, size changes).
- a, b, c ≠ 0: w differs per vertex → perspective distortion, aspect ratio not preserved.
- a only: no effect, since all vertices have x = 0.

### Extra task

Premultiply N·HS2: the top three rows stay [R t], only the last row changes.
The plot only uses the top rows, so nothing changes.

Postmultiply HS2·N: the top block becomes [R + t·[a b c], d·t], so each vertex
moves to p' = R p + w·t with w = a·x + b·y + c·z + d.
- a = b = c = 0: w = d for all vertices → pentagon only shifted along t
  (d = 0: no translation). Aspect ratio preserved.
- b, c ≠ 0: w differs per vertex → each vertex shifted by a different amount
  along t → sheared, sides no longer equal. Aspect ratio not preserved.
- a has no effect, since all vertices have x = 0.

