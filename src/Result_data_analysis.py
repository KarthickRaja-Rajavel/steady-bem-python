import pandas as pd
import matplotlib.pyplot as plt


python_Cp = pd.read_excel("Result data/Cp vs TSR (python).xlsx", decimal=",")
python_Ct = pd.read_excel("Result data/Ct vs TSR (python).xlsx", decimal=",")
Qblade_Cp = pd.read_csv("Result data/Cp vs TSR (QBlade).csv", sep=";", skiprows=2, encoding="latin1")
Qblade_Ct = pd.read_csv("Result data/Ct vs TSR (QBlade).csv", sep=";", skiprows=2, encoding="latin1")
Qblade_Cp = Qblade_Cp.iloc[:, :2]
Qblade_Ct = Qblade_Ct.iloc[:, :2]

print (Qblade_Cp)
print (Qblade_Ct)

plt.plot(Qblade_Cp.iloc[:,0], Qblade_Cp.iloc[:,1], label = "Qblade Cp")
plt.plot(python_Cp.iloc[:,0], python_Cp.iloc[:,1], label = "Python BEM Cp")
plt.title("Power coefficient", fontweight = "bold", y = 1.02)
plt.xlabel("Tip Speed Ratio (λ)")
plt.ylabel("Cp", rotation = 0)
plt.grid()
plt.legend()
plt.show()

plt.plot(Qblade_Ct.iloc[:,0], Qblade_Ct.iloc[:,1], label = "Qblade Ct")
plt.plot(python_Ct.iloc[:,0], python_Ct.iloc[:,1], label = "Python BEM Ct")
plt.title("Thrust coefficient", fontweight = "bold", y = 1.02)
plt.xlabel("Tip Speed Ratio (λ)")
plt.ylabel("Ct", rotation = 0)
plt.grid()
plt.legend()
plt.show() 