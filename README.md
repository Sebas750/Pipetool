# Pipetool
Aplication to simulate inharmonicities of wind instruments

# Dependencies

- Python 3.10.12
- matplotlib 3.8.2
- numpy 1.26.2
- openwind 0.10.3
- ttkboostrap 1.10.1

# Conditions to compute Embouchure impedance

To be able to unlock the Embouchure impedance button, the following conditions must be met:

Bore section:

1. The start position of the first row must be negative.
2. The end position of the first row must be 0.
3. The start and end radius/diameter must be equal.
4. The sectrion type of the first row must be "conical".
5. The start position of the second row must be 0.
6. the radius/diamter of the start of the second row must be greater o equal to the end radius/diameter of the first row.

Holes:

1. The label of the first hole (first row) must be "HJ".
2. The position of the first hole must be 1.


Finger chart.

1. For all notes, HJ must be marked as closed -> ●


