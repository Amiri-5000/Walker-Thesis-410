#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import astropy.units as u
from astropy.constants import m_e
from astropy.coordinates import Distance
import matplotlib.pyplot as plt
from IPython.display import Image

# import agnpy classes
from agnpy.spectra import PowerLaw
from agnpy.emission_regions import Blob
from agnpy.synchrotron import Synchrotron
from agnpy.compton import SynchrotronSelfCompton
from agnpy.utils.plot import plot_sed, load_mpl_rc

load_mpl_rc()

# blob properties
R_b =1e16 * u.cm
V_b = 4 / 3 * np.pi * R_b ** 3
z = Distance(1e27, unit=u.cm).z
delta_D = 10.0
Gamma = 10
B = 1 * u.G

# electron distribution
W_e = 1e48 * u.Unit("erg")

n_e = PowerLaw.from_total_energy(
    W=W_e, V=V_b, p=2.8, gamma_min=1e2, gamma_max=1e7, mass=m_e
)

blob = Blob(R_b, z, delta_D, Gamma, B, n_e=n_e)

#"""
###  various testing prints
print(blob)
#print(n_e)

# we can also print the total electrons number and energy
print(f"total particle number: {blob.N_e_tot:.2e}")
print(f"total energy in electrons: {blob.W_e:.2e}")

# as well as the jet power in particles and magnetic fields (see the documentation for more details)
print(f"jet power in particles: {blob.P_jet_ke:.2e}")
print(f"jet power in magnetic field: {blob.P_jet_B:.2e}")

#"""


synch = Synchrotron(blob)
synch_ssa = Synchrotron(blob, ssa=True)

# let us define now a grid of frequencies over which to calculate the synchrotron SED
nu_syn = np.logspace(8, 23) * u.Hz

# let us compute a synchrotron, and a self-absorbed synchrotron SED
synch_sed = synch.sed_flux(nu_syn)
synch_sed_ssa = synch_ssa.sed_flux(nu_syn)

# fig, ax = plt.subplots(figsize=(8, 6))
# plot_sed(nu_syn, synch_sed, ax=ax, color="k", label="synchr.")
# plot_sed(
#     nu_syn, synch_sed_ssa, ax=ax, ls="--", color="gray", label="self absorbed synchr."
# )
# plt.show()

# simple ssc
ssc = SynchrotronSelfCompton(blob)

# ssc over a self-absorbed synchrotron spectrum
ssc_ssa = SynchrotronSelfCompton(blob, ssa=True)

nu_ssc = np.logspace(15, 30) * u.Hz
sed_ssc = ssc.sed_flux(nu_ssc)
sed_ssc_ssa = ssc_ssa.sed_flux(nu_ssc)

# fig, ax = plt.subplots(figsize=(8, 6))

# plot_sed(nu_ssc, sed_ssc, color="k", label="SSC")
# plot_sed(nu_ssc, sed_ssc_ssa, ls="--", color="gray", label="SSC with SSA")
# plt.show()

# Image("figure_7_4_dermer_2009.png", width=600, height=400)

n_e = PowerLaw.from_total_energy(
    W=W_e, V=V_b, p=2.8, gamma_min=1e2, gamma_max=1e5, mass=m_e
)

blob2 = Blob(R_b, z, delta_D, Gamma, B, n_e=n_e)
synch2 = Synchrotron(blob2)
ssc2 = SynchrotronSelfCompton(blob2)

# fig, ax = plt.subplots(figsize=(8, 6))

# plot_sed(
#     nu_syn,
#     synch.sed_flux(nu_syn),
#     color="k",
#     label=r"${\rm synch},\,\gamma_{\rm max}=10^7$",
# )
# plot_sed(
#     nu_ssc,
#     ssc.sed_flux(nu_ssc),
#     color="k",
#     label=r"${\rm SSC},\,\gamma_{\rm max}=10^7$",
# )
# plot_sed(
#     nu_syn,
#     synch2.sed_flux(nu_syn),
#     color="crimson",
#     label=r"${\rm synch},\,\gamma_{\rm max}=10^5$",
# )
# plot_sed(
#     nu_ssc,
#     ssc2.sed_flux(nu_ssc),
#     color="crimson",
#     label=r"${\rm SSC},\,\gamma_{\rm max}=10^5$",
# )

# # select the same x and y range of the figure
# plt.xlim([1e9, 1e30])
# plt.ylim([1e-12, 1e-9])
# plt.show()

# print(R_b.unit)


"""
def blober(R_b=(1e16 * u.cm), V_b=(4 / 3 * np.pi * R_b ** 3), z=Distance(1e27, unit=u.cm).z, delta_D=10, Gamma=10, B=(1 * u.G), W_e=(1e48 * u.Unit("erg"))):
    n_e = PowerLaw.from_total_energy(
        W=W_e, V=V_b, p=2.8, gamma_min=1e2, gamma_max=1e7, mass=m_e)
    return Blob(R_b, z, delta_D, Gamma, B, n_e=n_e)
"""

blobvars=[R_b]
blobunits=np.array([u.cm,None,None,None,u.G,u.Unit("erg")])
for i in blobvars:
    print(i)
    if u.Unit(i) in blobunits:
        print('True!')
        i=float(input(f"Blob {i}?"))
    else:
        print("not true!")

#testdic=dict(inp=input("test input: "),default=1e16)
#print(f"input: {testdic["inp"]}, default: {testdic["default"]}")

def inputchecker(obj):
    while obj==obj:
        if isinstance(obj["inp"], (float,int))==False:
            check=input(f"{obj['name']} given not a number, will use default. Continue? Y/N: ")
            if check=="Y":
                obj=obj["default"]
                print(type(obj))
                break
            elif check=="N":
                if obj["unit"]!=None:
                    unit=obj["unit"]
                    obj=eval(input(f"{obj['name']} input? [default: {obj['default']}]: "))*unit
                else:
                    obj=eval(input(f"{obj['name']} input? [default: {obj['default']}]: "))
                print(type(obj))
            else:
                print("Invalid.")
        else:
            break

R_bi=dict(inp=eval('input(f"Blob radius? [default: {R_b}]: ")'),
          default=R_b,name="Blob radius", unit=u.cm)
inputchecker(R_bi)

zi=dict(inp=eval('input(f"Blob redshift? [default: {z:.4f}]: ")'),
        default=f'{z:.4f}',name="Blob redshift", unit=None)
inputchecker(zi)

delta_Di=dict(inp=eval('input(f"Doppler of jet? [default: {delta_D}]: ")'),
              default=delta_D,name="Jet doppler", unit=None)
inputchecker(delta_Di)

Gammai=dict(inp=eval('input(f"Max Lorentz factor of electrons? [default: {Gamma}]: ")'),
            default=Gamma,name="Max electrons' Lorentz factor", unit=None)
inputchecker(Gammai)

BlobGamMin=dict(inp=eval('input("fMin Lorentz factor of stream particles? [default: 1e2]: ")'),
                default=1e2,name="Minimum stream Lorentz factor", unit=None)
inputchecker(BlobGamMin)

BlobGamMax=dict(inp=eval('input(f"Max Lorentz factor of stream particles? [default: 1e7]: ")'),
                default=1e7,name="Maximum stream Lorentz factor", unit=None)
inputchecker(BlobGamMax)

Bi=dict(inp=eval('input(f"Magnetic field strength? [default: {B}]: ")'),
        default=B,name="Mag. field strength", unit=u.G)
inputchecker(Bi)

W_ei=dict(inp=eval('input(f"Total energy distributed? [default: {W_e}]: ")'),
          default=W_e,name="Distributed energy", unit=u.Unit("erg"))
inputchecker(W_ei)

V_bi=4 / 3 * np.pi * (R_bi) ** 3


n_ealt = PowerLaw.from_total_energy(
    W=W_ei, V=V_bi, p=2.8, gamma_min=BlobGamMin, gamma_max=BlobGamMax, mass=m_e
)
bloby=Blob(R_bi, zi, delta_Di, Gammai, Bi, n_e=n_ealt)
print(bloby.gamma_e_size)


#synchrotron radiation calculation(?)
synch_alt = Synchrotron(bloby) 
print(synch_alt)

#synchro. self absorption
synch_ssa_alt = Synchrotron(bloby, ssa=True) 

# simple self compton process calc
ssc_alt = SynchrotronSelfCompton(bloby) 

# self comp. over a self-absorbed synchrotron spectrum
ssc_ssa_alt = SynchrotronSelfCompton(bloby, ssa=True) 

#synchrotron rad. frequency
nu_syn_alt = np.logspace(8, 23) * u.Hz 

#synchrotron E-distribution  (based on synch. func. E-dist. flux w/ freq.)
synch_sed_alt = synch_alt.sed_flux(nu_syn_alt) 

#self absorption E-dist.  (based on self absorption E-dist. flux w/ freq.)
synch_sed_ssa_alt = synch_ssa_alt.sed_flux(nu_syn_alt)

#self compton freq.
nu_ssc_alt = np.logspace(15, 30) * u.Hz 

#self compton E-dist  (based on self compton E-dist. flux w/ freq.)
sed_ssc_alt = ssc_alt.sed_flux(nu_ssc_alt) 

#self compton AND absorption  (based on self compton AND absorption E-dist. flux w/ freq.)
sed_ssc_ssa_alt = ssc_ssa_alt.sed_flux(nu_ssc_alt) 


#plotting
fig, ax = plt.subplots(figsize=(8, 6))

plot_sed(
    nu_syn_alt,
    synch_alt.sed_flux(nu_syn_alt),
    color="k",
    label=r"${\rm input-synch},\,\gamma_{\rm max}=$"+f"{BlobGamMax}",
)
plot_sed(
    nu_ssc_alt,
    ssc_alt.sed_flux(nu_ssc_alt),
    color="k",
    label=r"${\rm input-SSC},\,\gamma_{\rm max}=10^7$"+f"{BlobGamMax}",
)

# plot_sed(
#     nu_syn,
#     synch.sed_flux(nu_syn),
#     color="k",
#     label=r"${\rm synch},\,\gamma_{\rm max}=10^7$",
# )
# plot_sed(
#     nu_ssc,
#     ssc.sed_flux(nu_ssc),
#     color="k",
#     label=r"${\rm SSC},\,\gamma_{\rm max}=10^7$",


plt.xlim([1e7, 1e30])
plt.ylim([1e-12, 1e-9])
plt.show()


#synch_alt.sed_flux(nu_syn_alt)
