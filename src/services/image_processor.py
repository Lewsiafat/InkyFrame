"""Image processing service for optimizing photos for Inky display."""
from pathlib import Path
from PIL import Image
import numpy

from src.config import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    THUMBNAIL_WIDTH,
    THUMBNAIL_HEIGHT,
    OPTIMIZED_DIR,
    THUMBNAILS_DIR
)


# Inky Spectra 6 color palettes
DESATURATED_PALETTE = [
    [0, 0, 0],        # Black
    [255, 255, 255],  # White
    [255, 255, 0],    # Yellow
    [255, 0, 0],      # Red
    [0, 0, 255],      # Blue
    [0, 255, 0],      # Green
]

SATURATED_PALETTE = [
    [0, 0, 0],        # Black
    [161, 164, 165],  # White (saturated)
    [208, 190, 71],   # Yellow (saturated)
    [156, 72, 75],    # Red (saturated)
    [61, 59, 94],     # Blue (saturated)
    [58, 91, 70],     # Green (saturated)
]


class ImageProcessor:
    """Service for processing and optimizing images for Inky display."""
    
    @staticmethod
    def _palette_blend(saturation: float) -> list[int]:
        """
        Blend desaturated and saturated palettes based on saturation level.
        
        Args:
            saturation: Saturation level (0.0 to 1.0)
            
        Returns:
            Blended palette as flat list of RGB values
        """
        palette = []
        for i in range(6):
            rs, gs, bs = [c * saturation for c in SATURATED_PALETTE[i]]
            rd, gd, bd = [c * (1.0 - saturation) for c in DESATURATED_PALETTE[i]]
            palette.extend([int(rs + rd), int(gs + gd), int(bs + bd)])
        return palette
    
    @staticmethod
    def optimize_for_display(
        input_path: Path,
        photo_id: str,
        saturation: float = 0.5
    ) -> Path:
        """
        Optimize image for Inky display.
        
        Args:
            input_path: Path to original image
            photo_id: Photo UUID
            saturation: Saturation level (0.0 to 1.0)
            
        Returns:
            Path to optimized image
        """
        # Load image
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to fit display while maintaining aspect ratio
        img.thumbnail((DISPLAY_WIDTH, DISPLAY_HEIGHT), Image.Resampling.LANCZOS)
        
        # Create new image with exact display dimensions (letterbox if needed)
        optimized = Image.new('RGB', (DISPLAY_WIDTH, DISPLAY_HEIGHT), (255, 255, 255))
        
        # Calculate position to center the image
        x_offset = (DISPLAY_WIDTH - img.width) // 2
        y_offset = (DISPLAY_HEIGHT - img.height) // 2
        
        # Paste resized image onto white background
        optimized.paste(img, (x_offset, y_offset))
        
        # Create palette image for quantization
        palette_image = Image.new("P", (1, 1))
        palette = ImageProcessor._palette_blend(saturation)
        palette_image.putpalette(palette)
        
        # Quantize to 6 colors with dithering
        optimized = optimized.quantize(
            colors=6,
            palette=palette_image,
            dither=Image.Dither.FLOYDSTEINBERG
        )
        
        # Convert back to RGB for saving
        optimized = optimized.convert('RGB')
        
        # Save optimized image
        output_path = OPTIMIZED_DIR / f"{photo_id}.jpg"
        optimized.save(output_path, 'JPEG', quality=95)
        
        return output_path
    
    @staticmethod
    def create_thumbnail(input_path: Path, photo_id: str) -> Path:
        """
        Create thumbnail for gallery display.
        
        Args:
            input_path: Path to original image
            photo_id: Photo UUID
            
        Returns:
            Path to thumbnail image
        """
        # Load image
        img = Image.open(input_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to thumbnail size while maintaining aspect ratio
        img.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)
        
        # Create new image with exact thumbnail dimensions
        thumbnail = Image.new('RGB', (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (255, 255, 255))
        
        # Calculate position to center the image
        x_offset = (THUMBNAIL_WIDTH - img.width) // 2
        y_offset = (THUMBNAIL_HEIGHT - img.height) // 2
        
        # Paste resized image onto white background
        thumbnail.paste(img, (x_offset, y_offset))
        
        # Save thumbnail
        output_path = THUMBNAILS_DIR / f"{photo_id}.jpg"
        thumbnail.save(output_path, 'JPEG', quality=85)
        
        return output_path
    
    @staticmethod
    async def process_upload(input_path: Path, photo_id: str) -> tuple[Path, Path]:
        """
        Process uploaded image: create optimized version and thumbnail.
        
        Args:
            input_path: Path to original uploaded image
            photo_id: Photo UUID
            
        Returns:
            Tuple of (optimized_path, thumbnail_path)
        """
        # Create optimized version
        optimized_path = ImageProcessor.optimize_for_display(input_path, photo_id)
        
        # Create thumbnail
        thumbnail_path = ImageProcessor.create_thumbnail(input_path, photo_id)
        
        return optimized_path, thumbnail_path
