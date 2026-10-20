"""Build the reproducible observational case and figures for test3."""
from __future__ import annotations

import gzip, hashlib, json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplcache"))

import gsw
import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr

DATA = ROOT / "data" / "test3_wave_case"
ASSETS = ROOT / "assets" / "waves"
ASSETS.mkdir(parents=True, exist_ok=True)
BUOY = DATA / "44088h2024.txt.gz"
ARGO = DATA / "D2902695_039.nc"


def style():
    for f in (Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf")):
        if f.exists():
            fm.fontManager.addfont(str(f)); plt.rcParams["font.family"] = fm.FontProperties(fname=str(f)).get_name(); break
    plt.rcParams.update({"figure.facecolor":"#f6fbfd","axes.facecolor":"#f6fbfd","axes.edgecolor":"#9bb4c7","axes.labelcolor":"#183b56","xtick.color":"#526d80","ytick.color":"#526d80","axes.unicode_minus":False,"figure.dpi":150,"savefig.dpi":210})


def qc_chars(a): return np.char.strip(np.asarray(a).astype("U"))


def choose(ds, name):
    raw=np.asarray(ds[name].values[0],float); q=qc_chars(ds[f"{name}_QC"].values[0]); out=np.where(np.isin(q,["1","2"]),raw,np.nan)
    if f"{name}_ADJUSTED" in ds and f"{name}_ADJUSTED_QC" in ds:
        adj=np.asarray(ds[f"{name}_ADJUSTED"].values[0],float); aq=qc_chars(ds[f"{name}_ADJUSTED_QC"].values[0]); out=np.where(np.isin(aq,["1","2"]),adj,out)
    return out


def load_buoy():
    with gzip.open(BUOY,"rt") as f: df=pd.read_csv(f,sep=r"\s+",skiprows=[1])
    df.columns=[c.lstrip("#") for c in df.columns]
    df["time"]=pd.to_datetime(dict(year=df.YY,month=df.MM,day=df.DD,hour=df.hh,minute=df.mm),utc=True)
    for c,bad in [("WVHT",99),("DPD",99),("APD",99)]: df[c]=pd.to_numeric(df[c],errors="coerce").where(lambda x:x<bad)
    return df.dropna(subset=["WVHT","DPD"]).sort_values("time")


def load_argo():
    with xr.open_dataset(ARGO,decode_cf=True) as ds:
        p,t,sp=choose(ds,"PRES"),choose(ds,"TEMP"),choose(ds,"PSAL")
        lon=float(ds.LONGITUDE.values[0]); lat=float(ds.LATITUDE.values[0]); when=pd.Timestamp(ds.JULD.values[0]).isoformat()
    ok=np.isfinite(p+t+sp)&(p>=0)&(p<=1000)&(sp>0)&(sp<42); p,t,sp=p[ok],t[ok],sp[ok]
    order=np.argsort(p); p,t,sp=p[order],t[order],sp[order]; p,idx=np.unique(p,return_index=True); t,sp=t[idx],sp[idx]
    grid=np.arange(max(5,np.ceil(p.min()/5)*5),min(1000,np.floor(p.max()/5)*5)+1,5.0)
    ti=np.interp(grid,p,t); spi=np.interp(grid,p,sp); sa=gsw.SA_from_SP(spi,grid,lon,lat); ct=gsw.CT_from_t(sa,ti,grid)
    sigma=gsw.sigma0(sa,ct); n2,pmid=gsw.Nsquared(sa,ct,grid,lat); depth=-gsw.z_from_p(grid,lat); dmid=-gsw.z_from_p(pmid,lat)
    return pd.DataFrame({"pressure_dbar":grid,"depth_m":depth,"practical_salinity":spi,"conservative_temperature_degC":ct,"sigma0_kg_m3":sigma}), pd.DataFrame({"pressure_mid_dbar":pmid,"depth_mid_m":dmid,"N2_s-2":n2,"N_cph":np.where(n2>0,np.sqrt(n2)*3600/(2*np.pi),np.nan),"buoyancy_period_min":np.where(n2>0,2*np.pi/np.sqrt(n2)/60,np.nan)}), lon,lat,when


def save_observation_figure(buoy,prof,nf,lang):
    zh=lang=="zh"; fig,ax=plt.subplots(1,3,figsize=(15.8,5.4),constrained_layout=True)
    monthly=buoy.set_index("time")["WVHT"].resample("MS").agg(["median",lambda x:x.quantile(.95)]); monthly.columns=["median","p95"]
    ax[0].plot(monthly.index,monthly["median"],"o-",color="#0a7c91",lw=2,label="月中位数" if zh else "Monthly median")
    ax[0].plot(monthly.index,monthly["p95"],"o-",color="#e26b4a",lw=2,label="月95百分位" if zh else "Monthly 95th percentile")
    ax[0].set(title="(a) 实测有效波高" if zh else "(a) Observed significant wave height",ylabel="有效波高 Hs (m)" if zh else "Significant wave height, Hs (m)"); ax[0].legend(frameon=False,fontsize=8); ax[0].grid(alpha=.25); ax[0].tick_params(axis="x",rotation=35)
    ax[1].plot(prof.sigma0_kg_m3,prof.depth_m,color="#334e9b",lw=2.4); ax[1].invert_yaxis(); ax[1].grid(alpha=.25); ax[1].set(title="(b) Argo 密度分层" if zh else "(b) Argo density stratification",xlabel=r"位势密度异常 $\sigma_0$ (kg m$^{-3}$)" if zh else r"Potential-density anomaly $\sigma_0$ (kg m$^{-3}$)",ylabel="深度 (m)" if zh else "Depth (m)")
    good=nf["N2_s-2"]>0; ax[2].plot(nf.loc[good,"N_cph"],nf.loc[good,"depth_mid_m"],color="#8b3faa",lw=2.4); ax[2].fill_betweenx(nf.loc[good,"depth_mid_m"],0,nf.loc[good,"N_cph"],color="#c99adb",alpha=.3); ax[2].invert_yaxis(); ax[2].grid(alpha=.25); ax[2].set(title="(c) 内波的恢复频率" if zh else "(c) Internal-wave restoring frequency",xlabel="浮力频率 N (周/小时)" if zh else "Buoyancy frequency, N (cycles h$^{-1}$)",ylabel="深度 (m)" if zh else "Depth (m)")
    title="表面波观测与内波分层条件" if zh else "Observed Surface Waves and the Stratification That Supports Internal Waves"
    fig.suptitle(title,fontsize=17,fontweight="bold",color="#0b3049")
    fig.text(.5,.005,("NOAA NDBC 44088（2024）和南海 Argo 2902695（2017-03-16）。Argo剖面说明分层条件，并不单独证明传播内波。" if zh else "NOAA NDBC 44088 (2024) and South China Sea Argo 2902695 (16 Mar 2017). The Argo profile diagnoses wave-supporting stratification; it does not alone prove a propagating internal wave."),ha="center",fontsize=8.5,color="#506b78")
    out=ASSETS/("test3_surface_internal_observations.png" if zh else "test3_surface_internal_observations-en.png"); fig.savefig(out,bbox_inches="tight"); plt.close(fig); return out


def save_concept_figure(lang):
    zh=lang=="zh"; fig,ax=plt.subplots(1,3,figsize=(15.8,5.3),constrained_layout=True)
    x=np.linspace(0,10,500); surf=.55*np.sin(2*np.pi*x/3.2); interface=-2+.8*np.sin(2*np.pi*x/5)
    ax[0].fill_between(x,surf,1.5,color="#d8eef5"); ax[0].fill_between(x,interface,surf,color="#62b6cb",alpha=.8); ax[0].fill_between(x,-4,interface,color="#224e75",alpha=.9); ax[0].plot(x,surf,color="#066e88",lw=2); ax[0].plot(x,interface,color="#ffca5c",lw=2.3); ax[0].text(5,.92,"表面重力波" if zh else "surface gravity wave",ha="center"); ax[0].text(5,-2.85,"界面内波" if zh else "interfacial internal wave",ha="center",color="white"); ax[0].set(xlim=(0,10),ylim=(-4,1.5),title="(a) 发生位置" if zh else "(a) Where waves occur"); ax[0].axis("off")
    T=np.linspace(3,20,150); cp=9.81*T/(2*np.pi); h1,h2,drho,rho0=50,150,2,1025; ci=np.sqrt(9.81*drho/rho0*h1*h2/(h1+h2)); ax[1].plot(T,cp,lw=2.5,color="#087c91",label="深水表面波相速" if zh else "Deep-water surface phase speed"); ax[1].axhline(ci,color="#9a43a6",lw=2.4,label="两层内波长波速度" if zh else "Two-layer internal long-wave speed"); ax[1].set(xlabel="周期 (s)" if zh else "Period (s)",ylabel="速度 (m s$^{-1}$)" if zh else "Speed (m s$^{-1}$)",title="(b) 速度尺度" if zh else "(b) Speed scales"); ax[1].legend(frameon=False,fontsize=8); ax[1].grid(alpha=.25)
    z=np.linspace(0,1,300); ax[2].plot(np.sin(np.pi*z),z,lw=2.5,label="模态1" if zh else "Mode 1"); ax[2].plot(np.sin(2*np.pi*z),z,lw=2.5,label="模态2" if zh else "Mode 2"); ax[2].plot(np.sin(3*np.pi*z),z,lw=2.5,label="模态3" if zh else "Mode 3"); ax[2].axvline(0,color="#8294a1",lw=.8); ax[2].invert_yaxis(); ax[2].set(xlabel="水平流速/位移结构（归一化）" if zh else "Normalized velocity/displacement structure",ylabel="归一化深度" if zh else "Normalized depth",title="(c) 连续分层中的垂向模态" if zh else "(c) Vertical modes in continuous stratification"); ax[2].legend(frameon=False,fontsize=8); ax[2].grid(alpha=.22)
    fig.suptitle("表面重力波与内波：概念和尺度" if zh else "Surface Gravity Waves and Internal Waves: Concepts and Scales",fontsize=17,fontweight="bold",color="#0b3049")
    fig.text(.5,.01,(f"示例：10 s深水表面波 c={9.81*10/(2*np.pi):.2f} m/s；两层内波 c={ci:.2f} m/s（h₁=50 m, h₂=150 m, Δρ=2 kg/m³）。" if zh else f"Examples: 10 s deep-water surface wave c={9.81*10/(2*np.pi):.2f} m/s; two-layer internal wave c={ci:.2f} m/s (h1=50 m, h2=150 m, Δrho=2 kg/m³)."),ha="center",fontsize=8.5,color="#506b78")
    out=ASSETS/("test3_wave_concepts.png" if zh else "test3_wave_concepts-en.png"); fig.savefig(out,bbox_inches="tight"); plt.close(fig); return out,ci


def main():
    style(); buoy=load_buoy(); prof,nf,lon,lat,when=load_argo()
    buoy[["time","WVHT","DPD","APD"]].to_csv(ASSETS/"test3_ndbc_44088_2024_wave_summary.csv",index=False)
    merged=pd.merge_asof(prof.sort_values("pressure_dbar"),nf.sort_values("pressure_mid_dbar"),left_on="pressure_dbar",right_on="pressure_mid_dbar",direction="nearest"); merged.to_csv(ASSETS/"test3_argo_stratification_profile.csv",index=False)
    for lang in ("en","zh"): save_observation_figure(buoy,prof,nf,lang)
    _,ci=save_concept_figure("en"); save_concept_figure("zh")
    npos=nf.loc[nf["N2_s-2"]>0,"N2_s-2"]; summary={
      "surface_case":{"station":"NOAA NDBC 44088 - New York Harbor Entrance","year":2024,"valid_records":int(len(buoy)),"median_Hs_m":float(buoy.WVHT.median()),"p95_Hs_m":float(buoy.WVHT.quantile(.95)),"maximum_Hs_m":float(buoy.WVHT.max()),"median_dominant_period_s":float(buoy.DPD.median())},
      "internal_case":{"argo_file":ARGO.name,"longitude_E":lon,"latitude_N":lat,"time":when,"stable_fraction":float((nf["N2_s-2"]>0).mean()),"maximum_N2_s-2":float(npos.max()),"minimum_buoyancy_period_min":float(2*np.pi/np.sqrt(npos.max())/60)},
      "worked_example":{"surface_period_s":10,"surface_phase_speed_m_s":9.81*10/(2*np.pi),"surface_wavelength_m":9.81*10**2/(2*np.pi),"h1_m":50,"h2_m":150,"density_difference_kg_m3":2,"rho0_kg_m3":1025,"reduced_gravity_m_s2":9.81*2/1025,"internal_longwave_speed_m_s":ci},
      "sources":{"ndbc":"https://www.ndbc.noaa.gov/data/historical/stdmet/44088h2024.txt.gz","argo_gdac":"https://data-argo.ifremer.fr/dac/csio/2902695/profiles/D2902695_039.nc","teos10":"https://www.teos-10.org/pubs/gsw/html/gsw_Nsquared.html"},
      "sha256":{"ndbc":hashlib.sha256(BUOY.read_bytes()).hexdigest(),"argo":hashlib.sha256(ARGO.read_bytes()).hexdigest()}}
    (ASSETS/"test3_wave_case_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__": main()
