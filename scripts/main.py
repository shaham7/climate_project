import pandas as pd
import numpy as np
from datetime import datetime

# Load data
def load_datasets():
    #TODO load all data sets int a dict and return that, too many data too confusing. 

    temp_df = pd.read_csv('climate_data/global_temperatures.csv')  
    emissions_df = pd.read_csv('climate_data/co2_emissions.csv') 
    gdp_df = pd.read_csv('climate_data/GDP_per_capita.csv')
    renewables_df = pd.read_csv('climate_data/renewable_energy.csv') 
    energy_df = pd.read_csv('climate_data/per_capita_energy_use.csv') 
    pop_df = pd.read_csv('climate_data/population.csv') 
    emissions_per_GDP_df = pd.read_csv('climate_data/Emission_per_GDP.csv') 
    Emission_per_capita_df = pd.read_csv('climate_data/Emission_per_capita.csv') 
    
    return {
        'temperature': temp_df,
        'emissions': emissions_df,
        'gdp': gdp_df,
        'renewables': renewables_df,
        'energy': energy_df,
        'population': pop_df, 
        'Emission_per_GDP': emissions_per_GDP_df,
        'Emission_per_capita': Emission_per_capita_df
    }

# Temprature
def load_and_clean_temperature(temp_df):
    #TODO there is both GISTEMP data and gcag data
    # i will take both seperatly and then fill the missing data in GISTEMP with data in gcag and use GISTEMP as the main 

    gistemp_data = temp_df[temp_df['Source'] == 'GISTEMP'].copy()
    gcag_data = temp_df[temp_df['Source'] == 'gcag'].copy()
    
    temp_clean = gistemp_data.copy()
    missing_years = set(gcag_data['Year']) - set(gistemp_data['Year'])

    gcag_fill = gcag_data[gcag_data['Year'].isin(missing_years)]
    temp_clean = pd.concat([temp_clean, gcag_fill])

    temp_clean = temp_clean.sort_values('Year').reset_index(drop=True)
    
    return temp_clean

# Emission
def clean_emissions_data(emissions_df):
    #TODO shoud chose only selected countries with top emission because its too many data and too many inconsistancies to focus on otherwise. 
    # have to melt the data frame to keep consiancy remember to check datatypes

    emissions_df = emissions_df.dropna(subset=['Country'])
    
    countries_of_interest = [ 'China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'GLOBAL TOTAL']
    emissions_clean = emissions_df[emissions_df['Country'].isin(countries_of_interest)]
    emissions_clean['Country'] = emissions_clean['Country'].replace('GLOBAL TOTAL', 'World')

    year_columns = [str(year) for year in range(1970, 2024)]
    emissions_melted = pd.melt( emissions_clean, id_vars=['Country'], value_vars=year_columns, var_name='Year', value_name='Emissions' )
   
    emissions_melted['Year'] = emissions_melted['Year'].astype(int)
    emissions_melted = emissions_melted.sort_values(['Country', 'Year'])
    
    return emissions_melted

# GDP
def clean_gdp_data(gdp_df):
    # TODO remove unwated data, select the wanted country, melt for consistancy, check datatypes

    gdp_df = gdp_df[gdp_df['Country'].notna()].copy()
    gdp_df = gdp_df[~gdp_df['Country'].str.contains('International Monetary Fund', na=False)]
    
    countries_of_interest = ['China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran' ]
    gdp_clean = gdp_df[gdp_df['Country'].isin(countries_of_interest)]

    year_columns = [str(year) for year in range(1980, 2024)]
    gdp_melted = pd.melt(gdp_clean, id_vars=['Country'], value_vars=year_columns, var_name='Year', value_name='GDP_per_capita')
    
    gdp_melted['GDP_per_capita'] = gdp_melted['GDP_per_capita'].str.replace(',', '')
    gdp_melted['GDP_per_capita'] = pd.to_numeric(gdp_melted['GDP_per_capita'], errors='coerce')
    gdp_melted['Year'] = gdp_melted['Year'].astype(int)
    
    return gdp_melted

# Renewables
def clean_renewables_data(renewables_df):
    # TODO keep only wanted conutries and world data, rename columns, check datatypes
    
    countries_of_interest = ['China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'World']
    renewables_clean = renewables_df[renewables_df['Entity'].isin(countries_of_interest)].copy()
    
    renewables_clean = renewables_clean.rename(columns={'Entity': 'Country','Renewables (% equivalent primary energy)': 'Renewable_Share'})
    
    return renewables_clean[['Country', 'Year', 'Renewable_Share']]

# Energy cons
def clean_energy_data(energy_df):
    # TODO select wanted countries, change colomn name, check datatypes 
    
    countries_of_interest = ['China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'World']
    energy_clean = energy_df[energy_df['Entity'].isin(countries_of_interest)].copy()
    
    energy_clean = energy_clean.rename(columns={'Entity': 'Country', 'Primary energy consumption per capita (kWh/person)': 'Energy_per_capita'})
    
    return energy_clean[['Country', 'Year', 'Energy_per_capita']]

# Energy cons
def clean_population_data(pop_df):
    # TODO select wanted countries, change colomn name, melt data, check datatypes 
    
    countries_of_interest = ['China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'World']
    pop_clean = pop_df[pop_df['Country Name'].isin(countries_of_interest)].copy()
    pop_clean = pop_clean.rename(columns={'Country Name': 'Country'})

    year_columns = [str(year) for year in range(1980, 2024)]
    pop_melted = pd.melt(pop_clean, id_vars=['Country'], value_vars=year_columns, var_name='Year', value_name='Population')

    pop_melted['Population'] = pd.to_numeric(pop_melted['Population'], errors='coerce')
    pop_melted['Year'] = pop_melted['Year'].astype(int)
    
    return pop_melted[['Country', 'Year', 'Population']]

# Emission per GDP 
def clean_Emission_per_GDP_data(emissions_per_GDP_df):
    #TODO shoud chose only selected countries with top emission because its too many data and too many inconsistancies to focus on otherwise. 
    # have to melt the data frame to keep consiancy remember to check datatypes

    emissions_per_GDP_df = emissions_per_GDP_df.dropna(subset=['Country'])
    
    countries_of_interest = [ 'China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'GLOBAL TOTAL']
    emissions_per_GDP_clean = emissions_per_GDP_df[emissions_per_GDP_df['Country'].isin(countries_of_interest)]
    emissions_per_GDP_clean['Country'] = emissions_per_GDP_clean['Country'].replace('GLOBAL TOTAL', 'World')

    year_columns = [str(year) for year in range(1990, 2024)]
    emissions_per_GDP_melted = pd.melt( emissions_per_GDP_clean, id_vars=['Country'], value_vars=year_columns, var_name='Year', value_name='Emissions_per_GDP' )
   
    emissions_per_GDP_melted['Year'] = emissions_per_GDP_melted['Year'].astype(int)
    emissions_per_GDP_melted = emissions_per_GDP_melted.sort_values(['Country', 'Year'])
    
    return emissions_per_GDP_melted

# Emission per capita 
def clean_Emission_per_capita_data(emissions_per_capita_df):
    #TODO shoud chose only selected countries with top emission because its too many data and too many inconsistancies to focus on otherwise. 
    # have to melt the data frame to keep consiancy remember to check datatypes

    emissions_per_capita_df = emissions_per_capita_df.dropna(subset=['Country'])
    
    countries_of_interest = [ 'China', 'Russia', 'United States', 'India', 'Germany', 'Japan', 'Indonesia', 'Saudi Arabia', 'South Korea', 'Iran', 'GLOBAL TOTAL']
    emissions_per_capita_clean = emissions_per_capita_df[emissions_per_capita_df['Country'].isin(countries_of_interest)]
    emissions_per_capita_clean['Country'] = emissions_per_capita_clean['Country'].replace('GLOBAL TOTAL', 'World')

    year_columns = [str(year) for year in range(1990, 2024)]
    emissions_per_capita_melted = pd.melt( emissions_per_capita_clean, id_vars=['Country'], value_vars=year_columns, var_name='Year', value_name='Emissions_per_capita' )
   
    emissions_per_capita_melted['Year'] = emissions_per_capita_melted['Year'].astype(int)
    emissions_per_capita_melted = emissions_per_capita_melted.sort_values(['Country', 'Year'])
    
    return emissions_per_capita_melted

# unify data
def create_unified_dataset():
    # TODO load all data, clean each dataset, 

    datasets = load_datasets()

    # Load all datasets
    temp_df = datasets["temperature"]
    emissions_df = datasets["emissions"]
    gdp_df = datasets["gdp"]
    renewables_df = datasets["renewables"]
    energy_df = datasets["energy"]
    pop_df = datasets["population"]
    emissions_per_GDP = datasets["Emission_per_GDP"]
    emissions_per_capita = datasets["Emission_per_capita"]

    # Clean individual datasets
    temp_clean = load_and_clean_temperature(temp_df)
    emissions_clean = clean_emissions_data(emissions_df)
    gdp_clean = clean_gdp_data(gdp_df)
    renewables_clean = clean_renewables_data(renewables_df)
    energy_clean = clean_energy_data(energy_df)
    population_clean = clean_population_data(pop_df)
    emissions_per_GDP_clean = clean_Emission_per_GDP_data(emissions_per_GDP)
    emissions_per_capita_clean = clean_Emission_per_capita_data(emissions_per_capita)

    # merging
    unified_df = emissions_clean.copy()
    unified_df = unified_df.merge( gdp_clean, on=['Country', 'Year'], how='left' 
                                  ).merge( renewables_clean, on=['Country', 'Year'], how='left'
                                          ).merge( energy_clean, on=['Country', 'Year'], how='left'
                                                  ).merge( population_clean, on= ['Country', 'Year'], how='left'
                                                          ).merge( emissions_per_GDP_clean, on= ['Country', 'Year'], how='left'
                                                                  ).merge( emissions_per_capita_clean, on= ['Country', 'Year'], how='left')
    
    unified_df = unified_df.merge( temp_clean[['Year', 'Mean']].rename(columns={'Mean': 'Global_Temperature'}), on='Year', how='left')
    
    return unified_df


# datasets = load_datasets()
# emissions_per_GDP = datasets["Emission_per_GDP"]
# emissions_per_GDP_clear = clean_Emission_per_GDP_data(emissions_per_GDP)

def save_processed_data(unified_df, output_path='processed_data.csv'):
    # TODO save data 
    unified_df.to_csv(output_path, index=False)
    
    # summary stats for referance
    summary_stats = unified_df.describe()
    summary_stats.to_csv('summary_statistics.csv')

if __name__ == "__main__":

    unified_df = create_unified_dataset()
    save_processed_data(unified_df)
    
    # print("Data processing completed successfully!")
    # print("\nDataset shape:", unified_df.shape)
    # print("\nColumns:", unified_df.columns.tolist())
    # print("\nDate range:", unified_df['Year'].min(), "to", unified_df['Year'].max())
    # print("\nCountries included:", unified_df['Country'].unique().tolist())

print(unified_df.describe())
