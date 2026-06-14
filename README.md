# steady-bem-python
Python implementation of a steady Blade Element Momentum (BEM) solver for wind turbine performance prediction.

The solver computes aerodynamic performance and blade-element loading using Reynolds-dependent airfoil polars, Prandtl tip-loss corrections, and iterative solution of axial and tangential induction factors.

## Features

* Steady-state Blade Element Momentum (BEM) formulation
* Reynolds-number-dependent polar interpolation
* Prandtl tip-loss correction
* Glauert high-loading correction
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

The solver was validated against a simple test turbine model developed in QBlade. Power coefficient (Cp) and thrust coefficient (Ct) predictions from the Python BEM solver were compared against QBlade results over a TSR range of 1–12.

### Power Coefficient Comparison

![image alt](https://github.com/KarthickRaja-Rajavel/steady-bem-python/blob/main/figures/Power%20coefficient%20(Qblade%20vs%20Python).png?raw=true)

### Thrust Coefficient Comparison

![image alt](https://github.com/KarthickRaja-Rajavel/steady-bem-python/blob/main/figures/Thrust%20coefficient%20(Qblade%20vs%20Python).png?raw=true)

Good agreement with QBlade is observed for TSR ≤ 5. At higher TSR, the Python BEM solver shows noticeable overprediction of Cp and Ct, probably due to simplifications in the steady-state BEM formulation and differences in induction and high-loading (Glauert) corrections compared to QBlade, and the absence of hub loss factor.

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

## Results

The solver generates:

* Cp versus TSR
* Ct versus TSR
* Spanwise thrust distribution
* Turbine thrust
* Turbine torque
* Turbine power

## Limitations

* Steady-state BEM formulation (no unsteady aerodynamic effects)
* Limited to rotors with single-airfoil type
* Single operating wind speed per simulation run

## Author

R.Karthick Raja Rajavel    
Scientific Assistant, in.RET    
MEng Student – Renewable Energy Systems     
Hochschule Nordhausen
