import serial
import time

def parse_nmea_sentence(sentence):
    """Parse NMEA sentences to extract useful information."""
    data = sentence.split(',')

    if sentence.startswith('$GPGGA'):
        utc_time = parse_utc_time(data[1])
        return {
            'type': 'GGA',
            'utc_time': utc_time,
            'latitude': f"{data[2]} {data[3]}",
            'longitude': f"{data[4]} {data[5]}",
            'satellites': int(data[7]) if data[7] else 0,
            'altitude': f"{data[9]} {data[10]}"
        }
    elif sentence.startswith('$GPGSV'):
        satellites = extract_satellite_system(data[4:])
        return {
            'type': 'GSV',
            'satellites_in_view': int(data[3]),
            'satellite_systems': satellites
        }
    return None

def extract_satellite_system(satellite_data):
    """Determine the satellite system based on PRN numbers."""
    systems = {'GPS': [], 'GLONASS': [], 'Galileo': [], 'BeiDou': [], 'QZSS': [], 'SBAS': []}
    
    for i in range(0, len(satellite_data), 4):  # Each satellite entry spans 4 fields
        try:
            prn = int(satellite_data[i])
            if 1 <= prn <= 32:
                systems['GPS'].append(prn)
            elif 65 <= prn <= 96:
                systems['GLONASS'].append(prn)
            elif 301 <= prn <= 336:
                systems['Galileo'].append(prn)
            elif 201 <= prn <= 235:
                systems['BeiDou'].append(prn)
            elif 193 <= prn <= 202:
                systems['QZSS'].append(prn)
            elif 120 <= prn <= 158:
                systems['SBAS'].append(prn)
        except ValueError:
            continue
    return systems

def parse_utc_time(utc_str):
    """Convert UTC time from GPS to a readable format."""
    if utc_str:
        hours = int(utc_str[0:2])
        minutes = int(utc_str[2:4])
        seconds = int(utc_str[4:6])
        return f"{hours:02}:{minutes:02}:{seconds:02} UTC"
    return "N/A"

def connect_gps(port='/dev/ttyUSB0', baudrate=9600):
    """Connect to the GPS device via the given serial port."""
    try:
        gps = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to GPS on {port}")
        return gps
    except serial.SerialException as e:
        print(f"Failed to connect to GPS: {e}")
        return None

def monitor_gps(gps):
    """Continuously read data from the GPS device and display it."""
    while True:
        try:
            data = gps.readline().decode('ascii', errors='replace').strip()
            if data:
                parsed_data = parse_nmea_sentence(data)
                if parsed_data:
                    print(parsed_data)
            time.sleep(1)  # Update every second
        except KeyboardInterrupt:
            print("Stopping GPS monitor.")
            break

if __name__ == "__main__":
    port = 'COM4'  # Replace with your GPS device's port on Windows (e.g., 'COM3')
    gps = connect_gps(port)

    if gps:
        monitor_gps(gps)
        gps.close()
