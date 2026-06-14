# steady-bem-python
Python implementation of a steady Blade Element Momentum (BEM) solver for wind turbine performance prediction.

The solver computes aerodynamic performance and blade-element loading using Reynolds-dependent airfoil polars, Prandtl tip-loss corrections, and iterative solution of axial and tangential induction factors.

## Features

* Steady-state Blade Element Momentum (BEM) formulation
* Reynolds-number-dependent polar interpolation
* Prandtl tip-loss correction
* Iterative solution of induction factors
* Power coefficient (Cp) prediction
* Thrust coefficient (Ct) prediction
* Spanwise thrust distribution
* Validation against QBlade

## Repository Structure

```text
src/
data/
validation/
results/
figures/
```

## Validation

The solver was validated against a simple test turbine model developed in QBlade.

### Power Coefficient Comparison

![image alt](figures/Power coefficient (Qblade vs Python).png)

### Thrust Coefficient Comparison

[Insert Ct figure here]

The results demonstrate good agreement with QBlade over the investigated TSR range. Differences are attributed to modeling assumptions and implementation details associated with the steady-state BEM formulation.

## Input Data

The solver requires:

* Blade geometry

  * chord distribution
  * radial positions
  * blade pitch angles
* Airfoil polar data
* Operating conditions

  * wind speed
  * air density
  * TSR range

## Running the Solver

1. Place airfoil polar files inside the Polar dataset folder.
2. Verify the folder path in the source code if necessary.
3. Run:

```python
python steady_state_bem_solver.py
```

4. Enter the required turbine geometry and operating conditions.

## Results

The solver generates:

* Cp versus TSR
* Ct versus TSR
* Spanwise thrust distribution
* Turbine thrust
* Turbine torque
* Turbine power

## Limitations

* Steady-state formulation only
* No dynamic stall model
* No yawed-flow modeling
* No aeroelastic coupling

## Author

Karthick [Surname]

Master's Student – Renewable Energy Engineering
