import os
import time
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

PROGRESS_BASE_URL = "https://api.brightdata.com/datasets/v3/progress"
DOWNLOAD_BASE_URL = "https://api.brightdata.com/datasets/v3/snapshot"

def poll_snapshot_status( 
  snapshot_id: str,
  max_attempts: int = 60,
  delay: int = 5 
) -> bool:
    headers = { "Authorization": f"Bearer { os.getenv( 'BRIGHTDATA_API_KEY' ) }" }

    for attempt in range( max_attempts ):
        try: 
            print( f"⏳ Checking snapshot progress... (attempt { attempt + 1 }/{ max_attempts })" )

            response = requests.get( f"{ PROGRESS_BASE_URL }/{ snapshot_id }", headers = headers )
            response.raise_for_status()

            progress_data = response.json()
            status = progress_data.get( "status" )

            if status == "ready":
                print( "✅ Snapshot is ready!" )
                return True
            elif status == "failed":
                print( "❌ Snapshot failed!" )
                return False
            elif status == "running":
                print( "🔄 Snapshot is running..." )
                time.sleep( delay )
            else:
                print( f"🔄 Unkown status (status: { status })" )
                time.sleep( delay )
        except Exception as e:
            print( f"❌ Error checking snapshot progress: { e }" )
            time.sleep( delay )
        
    print( "⏰ Timeout waiting for snapshot completion." )
    return False

def download_snapshot( snapshot_id: str, format: str = "json" ) -> Optional[ List[ Dict[ Any, Any ] ] ]:
    headers = { "Authorization": f"Bearer { os.getenv( 'BRIGHTDATA_API_KEY' ) }" }

    try:
        print("📥 Downloading snapshot data...")

        response = requests.get( f"{ DOWNLOAD_BASE_URL }/{ snapshot_id }?format={ format }", headers = headers )
        response.raise_for_status()

        data = response.json()
        print( f"🎉 Successfully downloaded {len(data) if isinstance(data, list) else 1} items" )

        return data

    except Exception as e:
        print( f"❌ Error downloading snapshot: { e }" )
        return None