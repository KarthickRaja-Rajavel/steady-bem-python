from math import atan,sqrt,pi,sin,cos,acos,exp
import pandas as pd
import numpy as np
import os
import bisect
import matplotlib.pyplot as plt


# 1. CODE FOR BEM INPUT

b = int(input("Enter number of blades (B):"))
R = float(input("Enter rotor radius [m] (R) :"))
# omega_rpm = float(input("Enter rotational speed [rpm] (ω) :"))
# omega = omega_rpm*(2*pi/60)
v1 = float(input("Enter wind speed far in front of turbine [m/s] (v1) :"))
rho = float(input("Enter air density {standard air density = 1.225} [kg/m^3] (ρ) :"))
n = int(input("Enter number of blade elements in your rotor :"))
nu = 1.5 * 10**-5  # kinematic viscocity
s1 = float(input("Enter Tip speed ratio start : "))
s2 = float(input("Enter Tip speed ratio end : "))
s3 = float(input("Enter Tip speed ratio delta : "))

TSR = []
TSR = np.arange(s1,s2+s3,s3)
omega = []
for i in range(len(TSR)):
    omega.append ((TSR[i]*v1)/R)

chord = []
radius = []
span = []
pitch = []

for i in range (n) :
    c = float(input(f"Enter chord length of the blade element {i+1} [m] (c) :"))
    chord.append (c)
    r = float(input(f"Enter the mid-radius of the blade element {i+1} [m] (r) :"))
    radius.append (r)
    dr = float(input(f"Enter the span length of element {i+1} [m] (dr) :"))
    span.append (dr)
    θ = float(input(f"Enter pitch angle of element {i+1} [°] θ) :"))
    pitch.append(θ)
#print (chord,radius,span,pitch)


# 2. CODE FOR INSTRUCTING REYNOLDS NUMBER FOR POLAR DATA

def Reynolds (v1,omega) :
    Re_list = []
    for i in range(len(radius)):
        v_rel = sqrt((v1*(2/3))**2 + (radius[i]*omega)**2)
        Re = chord[i] * v_rel / nu
        Re_list.append(Re)

    return min(Re_list), max(Re_list)
           
print ("Please ensure polar data available for the following Reynolds number range in Polar dataset folder" )

for x in range(len(omega)):    
    Re1,Re2 = Reynolds (v1,omega[x])
    print ("For TSR = ",TSR[x]," Re_min = ",Re1," ; Re_max = ",Re2)

input("Press Enter to continue..")


# 3. CODE FOR HANDLING OF POLAR FILES 

def load_polar_database(folder_path, max_files=10):

    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    if len(files) > max_files:
        raise ValueError(f"Too many files! Max allowed = {max_files}, found = {len(files)}")

    lift_data = {}
    drag_data = {}

    # helper function: extract Reynolds number - Polar_Re500k_Lift.csv
    def extract_Re(filename):
        re_str = filename.split("Re")[1].split("_")[0]

        if "k" in re_str:
            return float(re_str.replace("k", "")) * 1e3
        elif "M" in re_str:
            return float(re_str.replace("M", "")) * 1e6
        else:
            return float(re_str)

    # STEP 1: classify files
    for f in files:
        path = os.path.join(folder_path, f)
        df = pd.read_csv(path, sep=";", skiprows=2 , encoding="latin1")
        df = df.iloc[:, :2] 
        df.columns = ["alpha", "value"]
        Re = extract_Re(f)


        if "CL" in f.upper() or "LIFT" in f.upper():
            lift_data[Re] = df

        elif "CD" in f.upper() or "DRAG" in f.upper():
            drag_data[Re] = df

        else:
            raise ValueError(f"Cannot classify file (CL/CD missing): {f}")

    # STEP 2: merge into final database
    polars = {}

    for Re in lift_data:

        if Re not in drag_data:
            raise ValueError(f"Missing Cd file for Re = {Re}")

        lift = lift_data[Re]
        drag = drag_data[Re]
        lift = lift.rename(columns={"value": "Cl"})
        drag = drag.rename(columns={"value": "Cd"})
        # merge on alpha
        merged = pd.merge(lift, drag, on="alpha")  # Warning : Ensure alpha values are same for both lift and drag data

        polars[Re] = merged

    # STEP 3: sort by Reynolds number
    polars = dict(sorted(polars.items()))
    return polars

folder_path = r"\Polar dataset" #----- please update valid folder path to access polar data
polars = load_polar_database(folder_path, max_files=32)


# 4. CODE FOR POLAR INTERPOLATION 

def interpolation(Re, alpha):
    Re_list = sorted(polars.keys())
    pos = bisect.bisect_left(Re_list, Re)

    if pos == 0 or pos == len(Re_list):
        raise ValueError("Re out of bounds")

    Re_low = Re_list[pos - 1]
    Re_high = Re_list[pos]

    df_low = polars[Re_low]
    df_high = polars[Re_high]

    # weight (standard form)
    w = (Re - Re_low) / (Re_high - Re_low)

    # interpolate in alpha first (within each Re)
    Cl_low = np.interp(alpha, df_low["alpha"], df_low["Cl"])
    Cd_low = np.interp(alpha, df_low["alpha"], df_low["Cd"])

    Cl_high = np.interp(alpha, df_high["alpha"], df_high["Cl"])
    Cd_high = np.interp(alpha, df_high["alpha"], df_high["Cd"])

    # interpolate in Reynolds number
    Cl = (1 - w) * Cl_low + w * Cl_high
    Cd = (1 - w) * Cd_low + w * Cd_high

    return Cl, Cd

#print (polars)
print("\n--- Geometry and Polar dataset import complete ---\n")
input("Press Enter to start BEM solver...")


# 5. CODE FOR BEM CORE LOOPING STRUCTURE

T = []
M = []
P = []
Power = []
Thrust = []
for x in range(len(omega)) :  # --- TSR loop   
    T1 = []
    M1 = []
    P1 = []   
    for i in range (n) :      # --- Elements loop
        # initial guess
        a = 0
        a_prime = 0
        max_iteration = 200

        for iteration in range(max_iteration) :   # --- iteration loop

            phi_rad = atan(((1-a)*v1)/((1+a_prime)*omega[x]*radius[i])) # inflow angle
            phi_deg = np.degrees(phi_rad)
            alpha = phi_deg - pitch[i]  # angle of attack
            v_rel = sqrt((v1*(1-a))**2 + (radius[i]*omega[x]*(1 + a_prime))**2)  # relative velocity
            Re = (chord[i]*v_rel)/(nu)  # Reynolds number 
            Cl,Cd = interpolation(Re,alpha) 
            Cn = Cl*cos(phi_rad) + Cd*sin(phi_rad)
            Ct = Cl*sin(phi_rad) - Cd*cos(phi_rad)
            sldt = (chord[i]*b)/(2*pi*radius[i])

            # Stability conservation code for Tip loss factor F
            eps = 1e-4
            sin_phi = max(abs(sin(phi_rad)), eps)

            # Prandtl tip-loss exponent
            f = (b/2) * (R - radius[i]) / (radius[i] * sin_phi) # f must be positive , sin_phi must be positive [only magnitude matters]

            # exponential term
            exp_term = exp(-f)  # for positive f, exp_term is between 0 and 1
            exp_term = min(max(exp_term,0),1) # additional security to keep exp_term between 0 and 1

            F = (2/pi) * acos(exp_term)   # acos must take (-1 to +1) as input

            a_old = a
            a_prime_old = a_prime
            tolerance = 1e-4
            ct_eps = 1e-6
            Ct_safe = Ct if abs(Ct) > ct_eps else ct_eps * (1 if Ct >= 0 else -1) # Preventing Ct = 0 in denominator
            cn_eps = 1e-6
            Cn_safe = Cn if abs(Cn) > cn_eps else cn_eps * (1 if Cn >= 0 else -1) # Preventing Cn = 0 in denominator
            relax = 0.2 # relaxation factor to prevent oscillations in iterations
            if (a_old > 0.2):
                 a_c = 0.2
                 K = (4 * F * (sin(phi_rad)**2)) / (sldt * Cn_safe)
                 a_new = 0.5 * ( 2 + K * (1 - 2 * a_c) - sqrt((K * (1 - 2 * a_c) + 2)**2 + 4 * (K * a_c**2 - 1)))
                 a_prime_new = 1/(((F*4*sin(phi_rad)*cos(phi_rad))/(sldt*Ct_safe))-1)
                 a = (1 - relax)*a_old + relax*a_new
                 a_prime = (1 - relax)*a_prime_old + relax*a_prime_new
            else :
                a_new = 1/((4 * F * (sin(phi_rad)**2)) / (sldt * Cn_safe)+1)
                a_prime_new = 1/(((F*4*sin(phi_rad)*cos(phi_rad))/(sldt*Ct_safe))-1)
                a = (1 - relax)*a_old + relax*a_new
                a_prime = (1 - relax)*a_prime_old + relax*a_prime_new

            residual = max(abs(a-a_old),abs(a_prime-a_prime_old))
            if (residual < tolerance):
                print ("Element",i+1," converged at iteration :",iteration+1)
                dt = F*Cn_safe*0.5*rho*(v1)**2*(1-a)**2*chord[i]*b*(span[i]/(sin(phi_rad))**2)   # Normal force
                T1.append(dt)
                dm = F*Ct_safe*0.5*rho*v1*(1-a)*omega[x]*(radius[i])**2*(1+a_prime)*chord[i]*b*(span[i]/(sin(phi_rad)*cos(phi_rad))) # Torque
                M1.append(dm)
                dp = dm*omega[x]
                P1.append(dp)
                break
        else :
            raise ValueError(f"Element {i} convergence failed !") 


    Thrust1 = sum(T1)
    Moment = sum(M1)
    Power1 = sum(P1)
    Power.append(Power1)
    Thrust.append(Thrust1)
    T.append(T1)
    M.append(M1)
    P.append(P1)

    print ("The computed thrust force of the turbine at TSR ",TSR[x]," :", Thrust1)
    print ("The computed moment of the turbine at TSR ",TSR[x]," :", Moment)
    print ("The computed power of the turbine at TSR ",TSR[x]," :", Power1)

#print (T,M,P)


# 6. CODE FOR POST-PROCESSING RESULTS

# Cp vs Tsr - output 1

Power_wind = 0.5*rho*pi*R**2*v1**3
cp_list = []

for i in range(len(TSR)):
    cp_list.append(Power[i]/Power_wind)

plt.plot(TSR,cp_list)
plt.title("Cp vs TSR")
plt.xlabel("TSR (λ)")
plt.ylabel("Cp", rotation = 0)
plt.grid(True)
plt.show()

excelcp = pd.DataFrame ({
    "TSR" : TSR,
    "Cp"  : cp_list
})

excelcp.to_excel("Cp vs TSR.xlsx", index=False)

# Ct vs Tsr - output 2

Force_wind = 0.5*rho*pi*R**2*v1**2
ct_list = []

for i in range(len(TSR)):
    ct_list.append(Thrust[i]/Force_wind)

plt.plot(TSR,ct_list)
plt.title("Ct vs TSR")
plt.xlabel("TSR (λ)")
plt.ylabel("Ct", rotation = 0)
plt.grid(True)
plt.show()

excelct = pd.DataFrame ({
    "TSR" : TSR,
    "Ct"  : ct_list
})

excelct.to_excel("Ct vs TSR.xlsx", index=False)

# Elementwise Thrust distribution at each TSR value - output 3

elements = list(range(1,n+1))

z=1
for i in T :
    ii = str(z)
    plt.plot(elements,i)
    plt.title("Thrust distribution at TSR = "+ ii)
    plt.xlabel("elemennt (n)")
    plt.ylabel("Thrust (T)")
    plt.grid(True)
    plt.show()
    z=z+1

