import pandas as pd

def read_data_from_csv(file_path):
    try:
        # Read the CSV file into a DataFrame with 'latin-1' encoding and ';' as delimiter
        df = pd.read_csv(file_path, encoding='latin-1', delimiter=';')
        print("Successfully read the file with latin-1 encoding.")
        print("First few rows of the DataFrame:")
        print(df.head())
        
        # Ensure correct column names and data types if the columns exist
        if 'Coin' not in df.columns:
            print("Error: 'Coin' column is missing in the CSV file.")
            return pd.DataFrame()  # Return an empty DataFrame
        
        df['Fill Price'] = df['Fill Price'].str.replace(r'[^\d.]+', '', regex=True).astype(float)
        df['Amount'] = df['Amount'].str.replace(r'[^\d.]+', '', regex=True).astype(float)
        df['Total'] = df['Total'].str.replace(r'[^\d.]+', '', regex=True).astype(float)
        
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return pd.DataFrame()  # Return an empty DataFrame
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        print("Error: Error tokenizing data. Check the delimiter and the file structure.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def calculate_average_entry_price(df):
    if 'Amount' not in df.columns or 'Total' not in df.columns:
        print("Error: 'Amount' or 'Total' column is missing in the DataFrame.")
        return None, None
    
    total_amount = df['Amount'].sum()
    total_usdt = df['Total'].sum()
    
    if total_amount == 0:
        print("Error: Total amount is zero, cannot calculate average entry price.")
        return None, None
    
    average_entry_price = total_usdt / total_amount
    most_expensive_entry = df['Fill Price'].max() if 'Fill Price' in df.columns else None
    return average_entry_price, most_expensive_entry

def suggest_selling_price(average_entry_price, profit_margin):
    if average_entry_price is None:
        return None
    return average_entry_price * (1 + profit_margin)

def list_coins(df):
    if 'Coin' in df.columns:
        unique_coins = df['Coin'].str.upper().unique()
        print("Available Coins:")
        for coin in unique_coins:
            print(coin)
    else:
        print("Error: 'Coin' column is missing in the CSV file.")

def main():
    # Set the file path directly in the code
    # Se debe modificar la ruta depende de donde se encuentre el archivo
    file_path = r"C:\Users\Santiago HG\Desktop\trades\Track_CSV.csv"  # Adjust the path as needed
    
    df = read_data_from_csv(file_path)
    
    if df.empty:
        print("The CSV file is empty or could not be read. Exiting.")
        return

    # List available coins
    print("\n")
    list_coins(df)
    
    coin = input("Enter the coin you want to analyze: ").strip()
    
    if 'Coin' not in df.columns:
        print("Error: 'Coin' column is missing in the CSV file.")
        return
    
    df_coin = df[df['Coin'].str.upper() == coin.upper()]
    
    if df_coin.empty:
        print(f"No data found for the coin '{coin}'. Exiting.")
        return
    
    average_entry_price, most_expensive_entry = calculate_average_entry_price(df_coin)
    
    if average_entry_price is None:
        print("Error in calculating average entry price. Exiting.")
        return
    
    profit_margins = [0.10, 0.20, 0.50]  # 10%, 20%, 50%
    suggested_prices = {f"{int(margin*100)}%": suggest_selling_price(average_entry_price, margin) for margin in profit_margins}
    
    print(f"\nAnalysis for Coin: {coin.upper()}")
    print(f"Total Amount Purchased: {df_coin['Amount'].sum():.2f}")
    print(f"Total USDT Spent: {df_coin['Total'].sum():.2f}")
    print(f"Average Entry Price: {average_entry_price:.4f} USDT/Coin")
    if most_expensive_entry is not None:
        print(f"Most Expensive Entry: {most_expensive_entry:.4f} USDT/Coin")
    else:
        print("Most Expensive Entry: N/A")
    for margin, price in suggested_prices.items():
        if price is not None:
            print(f"Suggested Selling Price ({margin} profit): {price:.4f} USDT/Coin")

if __name__ == "__main__":
    main()
