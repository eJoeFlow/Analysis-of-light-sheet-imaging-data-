import napari
import numpy as np
import pandas as pd
from skimage import measure
from sklearn.decomposition import PCA

# Voxel size (scale) in micrometers (z, y, x)
voxel_size = (0.554, 0.2347120, 0.2347120)

# Access the current Napari viewer
viewer = napari.current_viewer()

try:
    # Access 'stardistlabels' from the existing viewer
    stardist_labels_layer = viewer.layers['stardistlabels']
except KeyError:
    raise KeyError("The 'stardistlabels' does not exist. Please make sure this layer is loaded.")

# Extract data from the layer
label_image_stack = stardist_labels_layer.data

# Function to perform PCA and get orientation axes and lengths
def get_pca_results(coords):
    pca = PCA(n_components=3)
    pca.fit(coords)
    # Eigenvalues give us measures for the axes lengths (variance along each axis)
    axes_lengths = np.sqrt(pca.explained_variance_)
    orientation_axes = pca.components_
    return orientation_axes, axes_lengths

# Prepare a list to store region properties
data = []

# Compute region properties for the 3D labeled image
regions = measure.regionprops(label_image_stack)

# Gather region properties
for i, region in enumerate(regions):
    # Calculate volume
    volume = region.area * np.prod(voxel_size)  # Convert voxel count to micrometers^3

    # Calculate orientation and axes lengths using PCA
    coords = region.coords * voxel_size  # Scale the coordinates
    orientation_axes, axes_lengths = get_pca_results(coords)

    # Get centroid
    centroid = np.array(region.centroid) * voxel_size

    # Append data
    data.append({
        'Object': i + 1,
        'Volume (micrometers^3)': volume,
        'Orientation Axes': orientation_axes.tolist(),  # Convert ndarray to list for CSV
        'Axes Lengths (micrometers)': axes_lengths.tolist(),  # Record the axes lengths
        'Centroid (micrometers)': centroid.tolist()     # Convert ndarray to list for CSV
    })

# Convert the list to a pandas DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
csv_filename = 'E:/JoachimPhysicsGuy/Edna/CFIM15gastruloids/bach1/region_properties_3d_noChiron_s04_806_decon_stitched_aligned-c0.csv'
df.to_csv(csv_filename, index=False)

print(f"Region properties with axes lengths (without area) have been saved to {csv_filename}")
