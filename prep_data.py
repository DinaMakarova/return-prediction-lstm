def clean_data(df):  
    """
    Function to clean data
    
    Parameters
    ----------
    x : Stock dataframe

    Returns
    -------
    Clean dataframe with three columns: Date, Price, Volume 

    """
    df = df.drop(columns=["Open", "High", "Low"], axis=1)
    df["Close/Last"] = df["Close/Last"].astype(str).str.replace('$', '')
    df["Close/Last"] = df["Close/Last"].astype(float)
    df = df.rename({"Close/Last": "Price"}, axis=1)

    return df


def generate_return(df):
    """
    Function to calculate returns

    Parameters
    ----------
    x : Stock

    Returns
    -------
    Closing price today / closing price yesterday

    """                    
    return df['Price'] / df['Price'].shift() - 1


def standardise_return(ret):
    """
    Function to standardise returns
 
    Parameters
    ----------
    x : Return column of the stock

    Returns
    -------
    (stock return - mean of stock returns) / standard deviation of stock returns

    """
    return (ret-ret.mean()) / ret.std()

def standardise_volume(vol):
    """
    Function to standardise volume
    
    Parameters
    ----------
    x : Volume column of the stock

    Returns
    -------
   (stock volume - mean of stock volume with rolling window of 50 days) 
   / 
   standard deviation of stock volume with rolling window of 50 days

    """
    return (vol-vol.rolling(50).mean()) / vol.rolling(50).std()