
# Data extracted from operational_research/src/data/geographic.py

# 38 Demand Zones (Southern Ontario)
# Format: (id, name, lat, lon, pop)
DEMAND_ZONES = [
    # Greater Toronto Area
    ("3520", "Toronto", 43.6532, -79.3832, 2794356),
    ("3521", "Peel", 43.7315, -79.7624, 1451022),
    ("3519", "York", 43.9954, -79.4658, 1173334),
    ("3524", "Durham", 43.9489, -78.8878, 696992),
    ("3525", "Halton", 43.4917, -79.8788, 596637),
    
    # Golden Horseshoe
    ("3526", "Hamilton", 43.2557, -79.8711, 569353),
    ("3528", "Niagara", 43.0896, -79.0849, 477941),
    ("3530", "Waterloo", 43.4643, -80.5204, 587165),
    ("3529", "Wellington", 43.7501, -80.2552, 247486),
    ("3531", "Brant", 43.1394, -80.2644, 144489),
    
    # Southwest Ontario
    ("3539", "Middlesex", 42.9849, -81.2453, 500569),
    ("3534", "Oxford", 43.0552, -80.7648, 121781),
    ("3536", "Elgin", 42.7748, -81.0649, 93529),
    ("3537", "Essex", 42.2793, -83.0154, 427811),
    ("3538", "Lambton", 42.9745, -82.3890, 128154),
    ("3540", "Chatham-Kent", 42.4040, -82.1910, 104316),
    
    # Central Ontario
    ("3543", "Simcoe", 44.3894, -79.6903, 507508),
    ("3544", "Muskoka", 45.0001, -79.3000, 64175),
    ("3546", "Kawartha Lakes", 44.3500, -78.7500, 77929),
    ("3547", "Peterborough", 44.3091, -78.3197, 149439),
    ("3548", "Northumberland", 44.0996, -78.1739, 89365),
    ("3549", "Hastings", 44.4834, -77.4901, 145746),
    
    # Eastern Ontario
    ("3551", "Prince Edward", 43.9754, -77.2502, 25704),
    ("3553", "Lennox and Addington", 44.4500, -77.0000, 45305),
    ("3510", "Ottawa", 45.4215, -75.6972, 1017449),
    ("3506", "Renfrew", 45.4713, -76.8890, 108280),
    ("3507", "Lanark", 45.0500, -76.2500, 74242),
    ("3509", "Leeds and Grenville", 44.6500, -75.7500, 105070),
    ("3502", "Prescott and Russell", 45.4000, -75.0000, 96750),
    ("3501", "Stormont, Dundas, Glengarry", 45.0500, -74.8000, 115063),
    ("3511", "Frontenac", 44.2312, -76.4860, 161225),
    
    # Grey-Bruce
    ("3541", "Grey", 44.4002, -80.8001, 102076),
    ("3542", "Bruce", 44.4998, -81.4002, 73396),
    ("3522", "Dufferin", 43.9500, -80.1500, 67182),
    
    # Haldimand-Norfolk
    ("3527", "Haldimand-Norfolk", 42.8833, -80.0667, 116903),
    
    # Northern Fringe
    ("3552", "Parry Sound", 45.3389, -79.9333, 45205),
    ("3554", "Nipissing", 46.3167, -79.4667, 85037),
    ("3557", "Greater Sudbury", 46.4917, -81.0000, 166004),
]

# 12 Candidate Warehouses
# Format: (id, name, lat, lon)
CANDIDATE_WAREHOUSES = [
    ("WH01", "Brampton", 43.7315, -79.7624),
    ("WH02", "Mississauga", 43.6435, -79.6193),
    ("WH03", "Vaughan", 43.8563, -79.5085),
    ("WH04", "Ajax/Pickering", 43.8509, -79.0204),
    ("WH05", "Milton", 43.5183, -79.8774),
    ("WH06", "Hamilton", 43.2132, -79.9875),
    ("WH07", "St. Catharines", 43.1594, -79.2469),
    ("WH08", "Cambridge", 43.3616, -80.3144),
    ("WH09", "London", 42.9849, -81.2453),
    ("WH10", "Ottawa", 45.2974, -75.9109),
    ("WH11", "Kingston", 44.2312, -76.4860),
    ("WH12", "Windsor", 42.3149, -83.0364),
]

# Optimal 7 Warehouses (from N=7 solution)
OPTIMAL_SET = {
    'WH02', # Mississauga
    'WH03', # Vaughan
    'WH10', # Ottawa
    'WH01', # Brampton
    'WH08', # Cambridge
    'WH04', # Ajax
    'WH12'  # Windsor
}

# Mapping: Zone ID -> Assigned Warehouse ID
# (Derived from typical closest-assignment logic for visualization)
ZONE_ASSIGNMENTS = {} 
# We will calculate this dynamically in the scene script for visual simplicity
