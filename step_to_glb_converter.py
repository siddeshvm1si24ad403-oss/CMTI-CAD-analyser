#!/usr/bin/env python3
"""
Direct STEP to GLB Converter
Converts STEP files directly to GLB format for the 3D CAD Viewer

Usage: python step_to_glb_converter.py input.step output.glb
"""

import sys
import os
import tempfile

def convert_step_to_glb_freecad(step_file, glb_file):
    """Convert STEP to GLB using FreeCAD"""
    try:
        print("🔄 Attempting conversion with FreeCAD...")
        
        # Try to import FreeCAD
        freecad_paths = [
            '/Applications/FreeCAD.app/Contents/Resources/lib',  # macOS
            '/usr/lib/freecad/lib',  # Linux
            '/usr/lib/freecad-python3/lib',  # Linux alternative
            'C:\\Program Files\\FreeCAD\\bin',  # Windows
        ]
        
        for path in freecad_paths:
            if os.path.exists(path) and path not in sys.path:
                sys.path.append(path)
        
        import FreeCAD
        import Import
        import Mesh
        
        print("✅ FreeCAD found!")
        
        # Create temporary STL file
        temp_stl = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        stl_path = temp_stl.name
        temp_stl.close()
        
        print(f"📂 Loading STEP file: {step_file}")
        
        # Import STEP file
        Import.insert(step_file, "TempDoc")
        doc = FreeCAD.ActiveDocument
        
        if not doc:
            doc = FreeCAD.newDocument("TempDoc")
            Import.insert(step_file, "TempDoc")
        
        # Export to STL
        print("💾 Converting to mesh format...")
        objs = [obj for obj in doc.Objects]
        Mesh.export(objs, stl_path)
        
        # Now convert STL to GLB using trimesh
        print("🔄 Converting to GLB format...")
        import trimesh
        mesh_data = trimesh.load(stl_path)
        mesh_data.export(glb_file, file_type='glb')
        
        # Clean up
        try:
            os.remove(stl_path)
            FreeCAD.closeDocument("TempDoc")
        except:
            pass
        
        print(f"✅ SUCCESS! GLB file created: {glb_file}")
        return True
        
    except ImportError as e:
        print(f"❌ FreeCAD not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def convert_step_to_glb_cadquery(step_file, glb_file):
    """Convert STEP to GLB using CadQuery"""
    try:
        print("🔄 Attempting conversion with CadQuery...")
        import cadquery as cq
        import trimesh
        
        print("✅ CadQuery found!")
        
        # Create temporary STL file
        temp_stl = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        stl_path = temp_stl.name
        temp_stl.close()
        
        print(f"📂 Loading STEP file: {step_file}")
        
        # Import STEP and export to STL
        result = cq.importers.importStep(step_file)
        result.val().exportStl(stl_path)
        
        # Convert STL to GLB
        print("🔄 Converting to GLB format...")
        mesh_data = trimesh.load(stl_path)
        mesh_data.export(glb_file, file_type='glb')
        
        # Clean up
        try:
            os.remove(stl_path)
        except:
            pass
        
        print(f"✅ SUCCESS! GLB file created: {glb_file}")
        return True
        
    except ImportError:
        print("❌ CadQuery not found")
        return False
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def convert_step_to_glb_cli(step_file, glb_file):
    """Convert STEP to GLB using FreeCAD command line"""
    try:
        print("🔄 Attempting conversion with FreeCAD CLI...")
        import subprocess
        import trimesh
        
        # Create temporary STL file
        temp_stl = tempfile.NamedTemporaryFile(suffix='.stl', delete=False)
        stl_path = temp_stl.name
        temp_stl.close()
        
        # Create conversion script
        conversion_script = f"""
import FreeCAD
import Import
import Mesh

Import.insert("{step_file}", "TempDoc")
doc = FreeCAD.ActiveDocument
if doc:
    objs = [obj for obj in doc.Objects]
    Mesh.export(objs, "{stl_path}")
    FreeCAD.closeDocument("TempDoc")
"""
        
        script_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        script_path = script_file.name
        script_file.write(conversion_script)
        script_file.close()
        
        print(f"📂 Loading STEP file: {step_file}")
        
        # Try different FreeCAD command names
        freecad_commands = [
            'freecadcmd',
            'FreeCADCmd',
            '/Applications/FreeCAD.app/Contents/MacOS/FreeCAD',
            'freecad',
        ]
        
        success = False
        for cmd in freecad_commands:
            try:
                result = subprocess.run(
                    [cmd, script_path],
                    capture_output=True,
                    timeout=120,  # 2 minute timeout for large files
                    text=True
                )
                
                if result.returncode == 0 and os.path.exists(stl_path) and os.path.getsize(stl_path) > 0:
                    print("✅ FreeCAD CLI conversion successful!")
                    
                    # Convert STL to GLB
                    print("🔄 Converting to GLB format...")
                    mesh_data = trimesh.load(stl_path)
                    mesh_data.export(glb_file, file_type='glb')
                    
                    success = True
                    break
            except FileNotFoundError:
                continue
            except subprocess.TimeoutExpired:
                print(f"⏱️ Timeout with {cmd}")
                continue
            except Exception as e:
                continue
        
        # Clean up
        try:
            os.remove(stl_path)
            os.remove(script_path)
        except:
            pass
        
        if success:
            print(f"✅ SUCCESS! GLB file created: {glb_file}")
            return True
        else:
            print("❌ FreeCAD CLI not found or failed")
            return False
            
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def print_usage():
    """Print usage instructions"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║           Direct STEP to GLB Converter                         ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python step_to_glb_converter.py input.step output.glb

Example:
    python step_to_glb_converter.py 5X8_COUPLER.STEP 5X8_COUPLER.glb

Requirements (install at least one):

1. FreeCAD (Recommended):
   macOS:    brew install --cask freecad
   Linux:    sudo apt install freecad
   Windows:  Download from freecadweb.org

2. CadQuery:
   conda install -c conda-forge cadquery

3. Trimesh (Required):
   pip install trimesh

After conversion, you can:
   - View the GLB file in the 3D CAD Viewer
   - Open in Blender, Three.js viewer, etc.
   - Use in AR/VR applications

Online Alternative (No Installation):
   - https://anyconv.com/step-to-stl-converter/
   - Convert STEP to STL
   - Then use: python stl_to_glb_converter.py input.stl output.glb
    """)

def main():
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    
    step_file = sys.argv[1]
    glb_file = sys.argv[2]
    
    # Check if input file exists
    if not os.path.exists(step_file):
        print(f"❌ Error: Input file not found: {step_file}")
        sys.exit(1)
    
    # Check file extension
    if not step_file.lower().endswith(('.step', '.stp')):
        print(f"❌ Error: Input file must be .step or .stp format")
        sys.exit(1)
    
    print("="*60)
    print("STEP to GLB Direct Conversion")
    print("="*60)
    print(f"Input:  {step_file}")
    print(f"Output: {glb_file}")
    print(f"Size:   {os.path.getsize(step_file) / 1024 / 1024:.2f} MB")
    print("="*60)
    print()
    
    # Try different converters
    success = False
    
    # Try FreeCAD Python module first
    if not success:
        success = convert_step_to_glb_freecad(step_file, glb_file)
    
    # Try CadQuery
    if not success:
        success = convert_step_to_glb_cadquery(step_file, glb_file)
    
    # Try FreeCAD CLI
    if not success:
        success = convert_step_to_glb_cli(step_file, glb_file)
    
    if not success:
        print("\n" + "="*60)
        print("❌ CONVERSION FAILED")
        print("="*60)
        print("\nNo suitable converter found!")
        print("\nPlease install one of the following:")
        print("  1. FreeCAD:  brew install --cask freecad")
        print("  2. CadQuery: conda install -c conda-forge cadquery")
        print("\nOr use an online converter:")
        print("  - https://anyconv.com/step-to-stl-converter/")
        print()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ CONVERSION COMPLETE!")
    print("="*60)
    print(f"\nGLB file created: {glb_file}")
    print(f"File size: {os.path.getsize(glb_file) / 1024 / 1024:.2f} MB")
    print("\nYou can now:")
    print("  - Upload this GLB to the 3D CAD Viewer")
    print("  - View in any GLB viewer")
    print("  - Use in web applications")
    print()

if __name__ == "__main__":
    main()
