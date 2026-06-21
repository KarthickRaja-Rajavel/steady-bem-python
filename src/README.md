# 🚀 How to Run

## 1. Install Python

Python 3.8 or higher is recommended.

Check your Python version:

```bash
python --version
```

## 2. Install Required Packages

Install the required Python libraries:

```bash
pip install numpy pandas matplotlib openpyxl
```

## 3. Download the Project

Either clone the repository using Git:

```bash
git clone <repository-url>
```

or download the repository as a ZIP file and extract it.

## 4. Configure the Polar Dataset Path

Before running the solver, update the `folder_path` variable in the source code (Line 128) so that it points to the location of your `Polar dataset` folder.

Example:

```python
folder_path = r"./Polar dataset"
```

## 5. Define Turbine and Blade Geometry

Run the code and enter the turbine parameters as prompted.

You will also need to:

* Specify the blade discretization (number of blade elements).
* Manually define the blade geometry for each element:

  * Chord length
  * Mid-radius position
  * Element span length
  * Pitch angle

> **Note:** Blade element specifications should be provided in **midpoint form**. Refer to **Table 3 of the Validation Report** for an example of the required format.

## 6. Verify Polar Data Availability

The code will calculate and display the required Reynolds number range for the simulation.

Ensure that the corresponding polar data files are available in the `Polar dataset` folder.

Polar files must follow the naming convention below:

```text
Polar_Re500k_Lift.csv
Polar_Re500k_Drag.csv
Polar_Re1M_Lift.csv
Polar_Re1M_Drag.csv
...
```

where:

* `Re500k` represents a Reynolds number of 500,000.
* `Re1M` represents a Reynolds number of 1,000,000.
* `Lift` files contain lift coefficient (Cl) data.
* `Drag` files contain drag coefficient (Cd) data.

> **Important:** The current implementation is configured for polar files exported from QBlade. If a different polar file format is used, modify the `load_polar_database()` function (starting around Line 68) accordingly.

## 7. Run the Solver

Once the required polar data are available, continue with the simulation.

The solver will:

* Compute turbine performance over the specified TSR range.
* Generate:

  * Cp vs TSR plots
  * Ct vs TSR plots
  * Radial thrust distribution plots for each TSR
* Export Excel files containing:

  * Cp results
  * Ct results

The generated Excel files can be used for further analysis and post-processing.
