land_crop_recommendations = {
    ('irrigated_land', 'paddy_field'): """
    <b>Land Type</b>: Irrigated Land <br/>
    <b>Suitable Crop</b>: Paddy<br/>
    <b>Water Requirement</b>: High (500-800 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Ensure continuous water supply during the entire growth period.<br/>
    2. Proper land leveling to avoid uneven water distribution.<br/>
    3. Regular weeding to avoid nutrient competition.<br/>
    4. Use disease-resistant rice varieties.<br/>
    5. Timely application of fertilizers, especially nitrogen.<br/>
    """,

    ('irrigated_land', 'cotton_field'): """
    <b>Land Type</b>: Irrigated Land <br/>
    <b>Suitable Crop</b>: Cotton<br/>
    <b>Water Requirement</b>: Moderate (300-500 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Well-drained loamy soils are ideal.<br/>
    2. Ensure regular moisture but avoid waterlogging.<br/>
    3. Timely application of fertilizers (NPK).<br/>
    4. Monitor for pests like bollworms.<br/>
    
    """,

    ('irrigated_land', 'wheat_field'): """
    <b>Land Type</b>: Irrigated Land <br/>
    <b>Suitable Crop</b>: Wheat<br/>
    <b>Water Requirement</b>: Moderate (400-500 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Use certified disease-resistant wheat seeds.<br/>
    2. Proper land preparation and timely sowing.<br/>
    3. Balanced fertilization (NPK) in split doses.<br/>
    4. Monitor rust and leaf spot diseases.<br/>
    
    """,

    ('upland_rainfed_agricultural_land', 'maize_field'): """
    <b>Land Type</b>: Upland Rainfed Agricultural Land <br/>
    <b>Suitable Crop</b>: Maize<br/>
    <b>Water Requirement</b>: Moderate (300-400 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Sow maize at the start of the rainy season.<br/>
    2. Use drought-tolerant maize hybrids.<br/>
    3. Mulch to conserve soil moisture.<br/>
    4. Regular weed control.<br/>
    
    """,

    ('upland_rainfed_agricultural_land', 'jowar_field'): """
    <b>Land Type</b>: Upland Rainfed Agricultural Land <br/>
    <b>Suitable Crop</b>: Jowar (Sorghum)<br/>
    <b>Water Requirement</b>: Low to Moderate (250-350 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Use drought-resistant jowar varieties.<br/>
    2. Minimum tillage to conserve soil moisture.<br/>
    3. Ensure proper spacing to allow airflow.<br/>
    
    """,

    ('lowland_irrigated_agricultural_land', 'wheat_field'): """
    <b>Land Type</b>: Lowland Irrigated Agricultural Land <br/>
    <b>Suitable Crop</b>: Wheat<br/>
    <b>Water Requirement</b>: Moderate (400-500 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Avoid waterlogging.<br/>
    2. Ensure balanced nutrient application.<br/>
    3. Monitor for rust and leaf diseases.<br/>
    
    """,

    ('intensively_irrigated_plains_land', 'cotton_field'): """
    <b>Land Type</b>: Intensively Irrigated Plains Land <br/>
    <b>Suitable Crop</b>: Cotton<br/>
    <b>Water Requirement</b>: Moderate (300-500 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Timely irrigation and proper drainage.<br/>
    2. Pest management (bollworms).<br/>
    3. Crop rotation to maintain soil fertility.<br/>
    
    """,

    ('drought_land', 'jowar_field'): """
    <b>Land Type</b>: Drought Land <br/>
    <b>Suitable Crop</b>: Jowar (Sorghum)<br/>
    <b>Water Requirement</b>: Low (200-300 mm per season)<br/>
    <b>Precautions</b>:<br/>
    1. Use drought-tolerant varieties.<br/>
    2. Mulching to conserve moisture.<br/>
    3. Minimum tillage techniques.<br/>

    """,
}

def get_mismatch_message(land_type):
    suggested_crops = {
        'irrigated_land': ['paddy_field', 'cotton_field', 'wheat_field'],
        'upland_rainfed_agricultural_land': ['maize_field', 'jowar_field'],
        'lowland_irrigated_agricultural_land': ['wheat_field'],
        'intensively_irrigated_plains_land': ['cotton_field'],
        'drought_land': ['jowar_field', 'maize_field']
    }

    crops = suggested_crops.get(land_type, [])
    crops_list = ', '.join(crops)

    return f"""
    <b>Land Type</b>: {land_type}<br/>
    <b>Crop Suitability</b>: This crop is not suitable for this land type.<br/>
    <b>Suggested Crops for This Land</b>: {crops_list if crops else "No suggestions available"}<br/>
    <b>General Precautions</b>:<br/>
    1. Improve soil fertility using organic compost.<br/>
    2. Use drought or flood-resistant crops based on the land type.<br/>
    3. Implement water conservation techniques like mulching.<br/>
    """
