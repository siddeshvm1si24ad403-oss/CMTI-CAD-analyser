"""
Test script for 3D file conversion pipeline
This demonstrates the conversion process outside of Streamlit
"""

import trimesh
import numpy as np
from pathlib import Path

def create_sample_stl(output_path="sample_cube.stl"):
    """Create a sample STL file for testing"""
    # Create a simple cube mesh
    vertices = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top
    ])
    
    faces = np.array([
        [0, 1, 2], [0, 2, 3],  # bottom
        [4, 6, 5], [4, 7, 6],  # top
        [0, 4, 5], [0, 5, 1],  # front
        [1, 5, 6], [1, 6, 2],  # right
        [2, 6, 7], [2, 7, 3],  # back
        [3, 7, 4], [3, 4, 0]   # left
    ])
    
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(output_path)
    print(f"✅ Created sample STL: {output_path}")
    return output_path

def test_conversion_pipeline(stl_file):
    """Test the conversion pipeline: STL -> OBJ -> GLB"""
    print("\n🔄 Testing conversion pipeline...")
    
    # Step 1: Load STL
    print("\n1️⃣ Loading STL file...")
    mesh = trimesh.load(stl_file)
    print(f"   Vertices: {len(mesh.vertices)}")
    print(f"   Faces: {len(mesh.faces)}")
    
    # Step 2: Convert to OBJ
    print("\n2️⃣ Converting to OBJ...")
    obj_file = str(Path(stl_file).with_suffix('.obj'))
    mesh.export(obj_file)
    print(f"   ✅ Saved: {obj_file}")
    
    # Step 3: Convert to GLB
    print("\n3️⃣ Converting to GLB...")
    glb_file = str(Path(stl_file).with_suffix('.glb'))
    mesh.export(glb_file, file_type='glb')
    print(f"   ✅ Saved: {glb_file}")
    
    # Step 4: Extract geometric data
    print("\n4️⃣ Extracting geometric data...")
    print(f"   Volume: {mesh.volume:.4f}")
    print(f"   Surface Area: {mesh.area:.4f}")
    print(f"   Bounds: {mesh.bounds}")
    print(f"   Centroid: {mesh.centroid}")
    print(f"   Is Watertight: {mesh.is_watertight}")
    print(f"   Is Convex: {mesh.is_convex}")
    
    print("\n✅ Conversion pipeline test complete!")
    return obj_file, glb_file

def analyze_mesh_features(mesh):
    """Analyze and print mesh features"""
    print("\n📊 Mesh Analysis:")
    print(f"   Vertices: {len(mesh.vertices):,}")
    print(f"   Faces: {len(mesh.faces):,}")
    print(f"   Edges: {len(mesh.edges):,}")
    print(f"   Volume: {mesh.volume:.4f} cubic units")
    print(f"   Surface Area: {mesh.area:.4f} square units")
    print(f"   Euler Number: {mesh.euler_number}")
    
    # Calculate genus (number of holes)
    genus = 1 - (mesh.euler_number / 2)
    print(f"   Genus (holes): {int(genus)}")
    
    # Bounding box
    bounds = mesh.bounds
    dimensions = bounds[1] - bounds[0]
    print(f"\n📐 Dimensions:")
    print(f"   X: {dimensions[0]:.4f}")
    print(f"   Y: {dimensions[1]:.4f}")
    print(f"   Z: {dimensions[2]:.4f}")
    
    # Bounding box volume
    bbox_volume = mesh.bounding_box.volume
    if mesh.is_volume and mesh.volume > 0:
        fill_ratio = (mesh.volume / bbox_volume) * 100
        print(f"\n🎯 Space Utilization:")
        print(f"   Model fills {fill_ratio:.2f}% of bounding box")
    
    print(f"\n✓ Quality Checks:")
    print(f"   Watertight: {'✅ Yes' if mesh.is_watertight else '❌ No'}")
    print(f"   Convex: {'✅ Yes' if mesh.is_convex else '❌ No'}")

if __name__ == "__main__":
    print("="*60)
    print("3D File Conversion Pipeline Test")
    print("="*60)
    
    # Create sample file
    sample_file = create_sample_stl()
    
    # Test conversion
    obj_file, glb_file = test_conversion_pipeline(sample_file)
    
    # Analyze the mesh
    mesh = trimesh.load(sample_file)
    analyze_mesh_features(mesh)
    
    print("\n" + "="*60)
    print("Test completed successfully!")
    print("="*60)
    print("\nGenerated files:")
    print(f"  - {sample_file} (STL)")
    print(f"  - {obj_file} (OBJ)")
    print(f"  - {glb_file} (GLB)")
    print("\nYou can now test these files with the Streamlit app!")
