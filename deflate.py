import tifffile

# Load your original masks file
masks = tifffile.imread('4d_noChiron_S01_711_decon_stitched_aligned-c0_cp_masks.tif')

# Save compressed version
tifffile.imwrite('4d_noChiron_S01_711_decon_stitched_aligned-c0_cp_masks_compressed.tiff', masks, compression='deflate')
