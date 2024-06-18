from database.DB_connect import DBConnect
from model.location import Location


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getProvider():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct nwhl.Provider as prov
from nyc_wifi_hotspot_locations nwhl order by nwhl.Provider"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["prov"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(provvider):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct nwhl.Location,AVG(nwhl.Latitude) as Latitude,AVG(nwhl.Longitude)  as Longitude
from nyc_wifi_hotspot_locations nwhl 
where nwhl.Provider=%s
group by nwhl.Location """

        cursor.execute(query,(provvider,))

        for row in cursor:
            result.append(Location(**row))

        cursor.close()
        conn.close()
        return result