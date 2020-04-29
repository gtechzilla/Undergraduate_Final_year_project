import requests,csv,os,json
import pandas as pd

mat_id=[]

prop_band=[]
prop_energy=[]
prop_energy_per_atom=[]
#prop_elastic_anisotropy=[]
with open ('../material-data/mp-ids-3402.csv') as csv_file:
        csv_reader = csv.reader(csv_file,delimiter = ',')
        for row in csv_reader:
            row = " ".join(str(x) for x in row)
            #use your api key provided by materials project
            r = f"https://www.materialsproject.org/rest/v2/materials/{row}/vasp?API_KEY=pI0GK1Uq3pmI2bp1L84U"
            req= requests.get(r)
            if req.status_code == requests.codes.ok:
                data = req.json()
                mat_id.append(row)
                print(row)
                for i in data['response']:
                        mat_id_web=i["material_id"]
                        band_gap = i["band_gap"]
                        prop_band.append(band_gap)
                        energy = i["energy"]
                        prop_energy.append(energy)
                        energy_per_atom = i["energy_per_atom"]
                        prop_energy_per_atom.append(energy_per_atom)
                        #elastic_anisotropy = i["elastic_anisotropy"]
                        #prop_elastic_anisotropy.append(elastic_anisotropy)
                        if row == mat_id_web:
                              cif = i["cif"]
                              cif_name = row+".cif"
                              print(cif_name)
                              f = open(cif_name,'w')
                              f.writelines(cif)
                              f.close()
                        else:
                              cif = i["cif"]
                              cif_name = mat_id_web +".cif"
                              print(cif_name)
                              f = open(cif_name,'w')
                              f.writelines(cif)
                              f.close()
#making dictionaries for the various properties
d_band_gap={"mat_id":mat_id,"prop":prop_band}
d_energy={"mat_id":mat_id,"prop":prop_energy}
d_energy_per_atom={"mat_id":mat_id,"prop":prop_energy_per_atom}
#d_elastic_anisotropy={"mat_id":mat_id,"prop":prop_elastic_anisotropy}

#converting ditionaries to panda dataframes
df_band_gap = pd.DataFrame.from_dict(d_band_gap,orient='index').transpose()
df_energy = pd.DataFrame.from_dict(d_energy,orient='index').transpose()
df_energy_per_atom = pd.DataFrame.from_dict(d_energy_per_atom,orient='index').transpose()
#df_elastic_anisotropy = pd.DataFrame([d_elastic_anisotropy])
#converting the dataframes to csv files
df_band_gap.to_csv(r'band.csv',index=None,header=True)
df_energy.to_csv(r'energy.csv',index=None,header=True)
df_energy_per_atom.to_csv(r'energy_per_atom.csv',index=None,header=True)
#df_elastic_anisotropy.to_csv(r'elastic_anisotropy.csv',index=None,header=True)
print("COMPLETED SUCCESFULLY")
