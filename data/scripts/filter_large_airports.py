import pandas as pd

def main():
    airports_df = pd.read_csv('../base/all_airports.csv')

    large_airports_df = airports_df[airports_df['type'] == 'large_airport']

    large_airports_df.to_csv('../base/large_airports.csv', index=False)

if __name__ == "__main__":
    main()
