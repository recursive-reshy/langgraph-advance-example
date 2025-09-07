from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote_plus

load_dotenv()

BRIGHT_DATA_URL = "https://api.brightdata.com/request"

# **kwar is used to allow the function to accept any number of keyword arguments
# i.e _make_api_request( url, headers=headers, params=params )
# Prefix _ is used to indicate that the function is private and should not be used outside of the module
def _make_api_request( url, **kwargs ):
    headers = {
        "Authorization": f"Bearer { os.getenv( 'BRIGHTDATA_API_KEY' ) }",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post( url, headers = headers, **kwargs )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print( f"Error making API request: { e }" )
        return None
    except Exception as e:
        print( f"Unexpected error: { e }" )
        return None

def serp_search( query, engine = "google" ):
    if( engine == "google" ):
        base_url = "https://www.google.com/search"
    elif( engine == "bing" ):
        base_url = "https://www.bing.com/search"
    else:
        raise ValueError( f"Invalid search engine: { engine }" )

    payload = {
        "zone": "langgraph_advance_example",
        # brd_json=1 is used to get the response in JSON format from Bright Data
        "url": f"{ base_url }?q={ quote_plus( query ) }&brd_json=1",
        "format": "raw",
    }

    full_response = _make_api_request( BRIGHT_DATA_URL, json = payload )

    if not full_response:
        print( "No response from Bright Data" )
        return None

    extracted_data = {
        "knowledge": full_response.get( "knowledge", {} ),
        "organic": full_response.get( "organic", [] ),
    }

    return extracted_data