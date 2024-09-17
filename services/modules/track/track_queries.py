from firebase_admin import db
from datetime import datetime
from helpers.converter import calculate_distance
from fastapi.responses import JSONResponse

async def get_last_tracker_position_api(userId:str):
    # Attribute
    userId = 'fcd3f23e-e5aa-11ee-892a-3216422910e9'
    ref = db.reference('track_live_'+userId)

    # Order child index
    query = ref.order_by_child('created_at').limit_to_last(1)
    data = query.get()

    if data:
        data_values = list(data.values())
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_values[0],
                "message": "Last track found",
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data":None,
                "message": "No Track found",
            }
        )

async def get_tracks(userId:str):
    # Attribute
    ref = db.reference('track_live_'+userId)

    # Order child index
    query = ref.order_by_child('created_at').limit_to_last(10)
    data = query.get()

    if data:
        data_values = list(data.values())
        return JSONResponse(
            status_code=200, 
            content={
                "data": data_values,
                "message": "Track journey found",
                "count": len(data_values)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "No Track journey found",
                "count":0
            }
        )
    
async def get_tracks_period(userId: str, start_time: datetime = None, end_time: datetime = None):
    # Attribute
    ref = db.reference('track_live_' + userId)
    
    # Order child index
    query = ref.order_by_child('created_at')
    
    # Filter
    if start_time:
        start_time_str = start_time.isoformat(timespec='microseconds')
        query = query.start_at(start_time_str)
    
    if end_time:
        end_time_str = end_time.isoformat(timespec='microseconds')
        query = query.end_at(end_time_str)
    
    data = query.get()
    
    if data:
        data_values = list(data.values())
        return JSONResponse(
            status_code=201, 
            content={
                "data": data_values,
                "message": "Track journey found",
                "count": len(data_values)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "No Track journey found",
                "count": 0
            }
        )
    
async def get_total_distance_by_month_query(userId: str, year: int):
    # Attribute
    ref = db.reference('track_live_' + userId)
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31, 23, 59, 59, 999999)
    
    # Filter
    start_time_str = start_of_year.isoformat(timespec='microseconds')
    end_time_str = end_of_year.isoformat(timespec='microseconds')
    
    # Order child index
    query = ref.order_by_child('created_at').start_at(start_time_str).end_at(end_time_str)
    
    data = query.get()
    
    if data:
        data_values = list(data.values())
        
        # Column builder
        for item in data_values:
            created_at = datetime.fromisoformat(item['created_at'])
            item['month'] = created_at.month
            if 'battery_indicator' in item:
                del item['battery_indicator']
            if 'created_by' in item:
                del item['created_by']
            if 'track_type' in item:
                del item['track_type']
        
        # Order by column builder
        data_values.sort(key=lambda x: x['month'])
        
        # Holder
        month_distances = {}
        
        for i in range(len(data_values) - 1):
            data_values[i]['coordinate_start'] = f"{data_values[i]['track_lat']},{data_values[i]['track_long']}"
            data_values[i]['coordinate_end'] = f"{data_values[i + 1]['track_lat']},{data_values[i + 1]['track_long']}"
            data_values[i]['distance'] = calculate_distance(data_values[i]['coordinate_start'], data_values[i]['coordinate_end'])
            
            month = data_values[i]['month']
            if month in month_distances:
                month_distances[month] += data_values[i]['distance']
            else:
                month_distances[month] = data_values[i]['distance']
        
        if data_values:
            last_item = data_values[-1]
            last_item['coordinate_start'] = f"{last_item['track_lat']},{last_item['track_long']}"
            last_item['coordinate_end'] = None 
            last_item['distance'] = 0 
            month = last_item['month']
            if month in month_distances:
                month_distances[month] += last_item['distance']
            else:
                month_distances[month] = last_item['distance']
        
        # Final res
        formatted_data = [{"context": month, "total": distance} for month, distance in month_distances.items()]
        
        # Column builder
        for item in data_values:
            if 'track_lat' in item:
                del item['track_lat']
            if 'track_long' in item:
                del item['track_long']
            if 'coordinate_start' in item:
                del item['coordinate_start']
            if 'coordinate_end' in item:
                del item['coordinate_end']
            if 'distance' in item:
                del item['distance']
        
        return JSONResponse(
            status_code=200, 
            content={
                "data": formatted_data,
                "data_detail": data_values,
                "message": "Track journey found",
                "count": len(data_values)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data":None,
                "data_detail":None,
                "message": "No Track journey found",
                "count":0
            }
        )
    
async def get_total_distance_by_time_query(userId: str, year: int):
    # Attribute
    ref = db.reference('track_live_' + userId)
    start_of_year = datetime(year, 1, 1)
    end_of_year = datetime(year, 12, 31, 23, 59, 59, 999999)
    
    # Filter
    start_time_str = start_of_year.isoformat(timespec='microseconds')
    end_time_str = end_of_year.isoformat(timespec='microseconds')
    
    # Order child index
    query = ref.order_by_child('created_at').start_at(start_time_str).end_at(end_time_str)
    
    data = query.get()
    
    if data:
        data_values = list(data.values())
        
        # Column builder
        for item in data_values:
            created_at = datetime.fromisoformat(item['created_at'])
            item['hour'] = created_at.hour
            if 'battery_indicator' in item:
                del item['battery_indicator']
            if 'created_by' in item:
                del item['created_by']
            if 'track_type' in item:
                del item['track_type']
        
        # Order by column builder
        data_values.sort(key=lambda x: x['hour'])
        
        # Holder
        hour_distances = {}
        
        for i in range(len(data_values) - 1):
            data_values[i]['coordinate_start'] = f"{data_values[i]['track_lat']},{data_values[i]['track_long']}"
            data_values[i]['coordinate_end'] = f"{data_values[i + 1]['track_lat']},{data_values[i + 1]['track_long']}"
            data_values[i]['distance'] = calculate_distance(data_values[i]['coordinate_start'], data_values[i]['coordinate_end'])
            
            hour = data_values[i]['hour']
            if hour in hour_distances:
                hour_distances[hour] += data_values[i]['distance']
            else:
                hour_distances[hour] = data_values[i]['distance']
        
        if data_values:
            last_item = data_values[-1]
            last_item['coordinate_start'] = f"{last_item['track_lat']},{last_item['track_long']}"
            last_item['coordinate_end'] = None 
            last_item['distance'] = 0 
            hour = last_item['hour']
            if hour in hour_distances:
                hour_distances[hour] += last_item['distance']
            else:
                hour_distances[hour] = last_item['distance']
        
        # Final res
        formatted_data = [{"context": hour, "total": distance} for hour, distance in hour_distances.items()]
        
        # Column builder
        for item in data_values:
            if 'track_lat' in item:
                del item['track_lat']
            if 'track_long' in item:
                del item['track_long']
            if 'coordinate_start' in item:
                del item['coordinate_start']
            if 'coordinate_end' in item:
                del item['coordinate_end']
            if 'distance' in item:
                del item['distance']
        
        return JSONResponse(
            status_code=200, 
            content={
                "data": formatted_data,
                "data_detail": data_values,
                "message": "Track journey found",
                "count": len(data_values)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "data_detail": None,
                "message": "No Track journey found",
                "count": 0
            }
        )

async def get_activity_around_coordinate_query(userId: str, coor: str):
    # Attribute
    ref = db.reference('track_live_' + userId)
    
    # Order child index
    query = ref.order_by_child('created_at')
    
    data = query.get()
    
    if data:
        data_values = list(data.values())
        
        # Column builder
        for item in data_values:
            item['date'] = item['created_at']
            if 'battery_indicator' in item:
                del item['battery_indicator']
            if 'created_by' in item:
                del item['created_by']
            if 'track_type' in item:
                del item['track_type']
        
        # Order by column builder
        data_values.sort(key=lambda x: x['date'])
        
        for i in range(len(data_values)):
            data_values[i]['coordinate_track'] = f"{data_values[i]['track_lat']},{data_values[i]['track_long']}"
            data_values[i]['distance'] = calculate_distance(data_values[i]['coordinate_track'], coor)
        
        # Group by date and lowest distance
        grouped_data = {}
        for item in data_values:
            date = item['date']
            if date not in grouped_data or item['distance'] < grouped_data[date]['distance']:
                grouped_data[date] = item
        
        final_data = list(grouped_data.values())
        
        # Column builder
        for item in final_data:
            if 'track_lat' in item:
                del item['track_lat']
            if 'track_long' in item:
                del item['track_long']
            if 'coordinate_track' in item:
                del item['coordinate_track']
        
        return JSONResponse(
            status_code=200, 
            content={
                "data": final_data,
                "message": "Track activity found",
                "count": len(final_data)
            }
        )
    else:
        return JSONResponse(
            status_code=404, 
            content={
                "data": None,
                "message": "No Track activity found",
                "count":0
            }
        )