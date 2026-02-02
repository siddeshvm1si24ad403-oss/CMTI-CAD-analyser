#!/usr/bin/env python3
"""
STL to GLB Converter
Simple converter for STL files to GLB format

Usage: python stl_to_glb_converter.py input.stl output.glb
"""

import sys
import os

def convert_stl_to_glb(stl_file, glb_file):
    """Convert STL to GLB using trimesh"""
    try:
        import trimesh
        
        print(f"📂 Loading STL file: {stl_file}")
        mesh = trimesh.load(stl_file)
        
        print(f"   Vertices: {len(mesh.vertices):,}")
        print(f"   Faces: {len(mesh.faces):,}")
        
        print(f"💾 Exporting to GLB: {glb_file}")
        mesh.export(glb_file, file_type='glb')
        
        print("✅ Conversion successful!")
        return True
        
    except ImportError:
        print("❌ Error: trimesh not installed")
        print("Install with: pip install trimesh")
        return False
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("""
╔════════════════════════════════════════════════════════════════╗
║              STL to GLB Converter                              ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python stl_to_glb_converter.py input.stl output.glb

Example:
    python stl_to_glb_converter.py model.stl model.glb

Requirements:
    pip install trimesh
        """)
        sys.exit(1)
    
    stl_file = sys.argv[1]
    glb_file = sys.argv[2]
    
    if not os.path.exists(stl_file):
        print(f"❌ Error: File not found: {stl_file}")
        sys.exit(1)
    
    print("="*60)
    print("STL to GLB Conversion")
    print("="*60)
    print(f"Input:  {stl_file}")
    print(f"Output: {glb_file}")
    print("="*60)
    print()
    
    if convert_stl_to_glb(stl_file, glb_file):
        print("\n" + "="*60)
        print(f"✅ GLB file created: {glb_file}")
        print(f"   Size: {os.path.getsize(glb_file) / 1024 / 1024:.2f} MB")
        print("="*60)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
