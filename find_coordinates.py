from PIL import Image, ImageOps
import numpy as np

def find_bright_spots(image_path):
    img = Image.open(image_path).convert('L') # Convert to grayscale
    img_data = np.asarray(img)
    
    # Threshold to find bright spots (cities)
    threshold = 150 # Lower threshold to catch dimmer cities
    indices = np.argwhere(img_data > threshold)
    
    if len(indices) == 0:
        print("No bright spots found.")
        return

    # Use scipy.ndimage to find clusters (connected components)
    from scipy.ndimage import label, center_of_mass
    
    labeled_array, num_features = label(img_data > threshold)
    
    if num_features == 0:
        print("No bright spots found.")
        return

    centroids_rc = center_of_mass(img_data > threshold, labeled_array, range(1, num_features+1))
    
    # Get sizes
    sizes = [np.sum(labeled_array == i) for i in range(1, num_features+1)]
    
    # Zip centroids with sizes
    # centroids_rc is (row, col)
    city_data = []
    for i in range(num_features):
        city_data.append({
            "centroid": centroids_rc[i],
            "size": sizes[i],
            "id": i+1
        })
        
    # Sort by size descending
    city_data.sort(key=lambda x: x["size"], reverse=True)
    
    # Keep top 10 largest spots
    top_cities = city_data[:10]
    
    # Sort these top cities by longitude (x) for easier identification
    # centroid is (y, x)
    top_cities.sort(key=lambda p: p["centroid"][1]) 
    
    height, width = img_data.shape
    print(f"Image Dimensions: {width}x{height}")
    
    # Convert to Manim Coordinates
    # Manim Frame Height = 8 (default scene height is actually 8)
    # Image in Manim is scaled to HEIGHT = 7.5
    # So 7.5 units = height pixels
    
    scale_factor = 7.5 / height
    
    manim_coords = []
    print("\nFound Top 10 Major Cities (by text size/brightness):")
    for i, city in enumerate(top_cities):
        y_img, x_img = city["centroid"]
        size = city["size"]
        
        # Center of image is (width/2, height/2)
        x_from_center = x_img - (width / 2)
        y_from_center = (height / 2) - y_img 
        
        manim_x = x_from_center * scale_factor
        manim_y = y_from_center * scale_factor
        
        print(f"City (Size {size}): Pixel({x_img:.1f}, {y_img:.1f}) -> Manim[{manim_x:.2f}, {manim_y:.2f}, 0]")
        manim_coords.append((manim_x, manim_y))
        
    return manim_coords

if __name__ == "__main__":
    try:
        find_bright_spots("assets/southern_ontario_map.png")
    except Exception as e:
        print(f"Error: {e}")
