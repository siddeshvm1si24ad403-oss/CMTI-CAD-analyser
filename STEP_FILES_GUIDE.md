# How to Use STEP Files with the 3D CAD Viewer

## The Issue
STEP (.step, .stp) files are complex CAD formats that require specialized libraries to read. The basic Python libraries don't support them natively.

## ✅ Quick Solutions (Choose One)

### Option 1: Convert STEP to STL Online (Fastest - 2 minutes)
1. Go to any of these free converters:
   - https://anyconv.com/step-to-stl-converter/
   - https://www.greentoken.de/onlineconv.aspx
   - https://products.aspose.app/3d/conversion/step-to-stl

2. Upload your STEP file
3. Download the converted STL file
4. Upload the STL to our 3D CAD Viewer

### Option 2: Use FreeCAD (Free Desktop Software)
```bash
# Install FreeCAD
brew install --cask freecad

# Open FreeCAD
# File → Open → Select your STEP file
# File → Export → Choose "STL Mesh (*.stl)"
# Save the file
```

Then upload the STL to the viewer.

### Option 3: Use the Conversion Script
```bash
# Install FreeCAD first (see Option 2)

# Set Python path
export PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib:$PYTHONPATH

# Run converter
python convert_step_to_stl.py Part1.STEP Part1.stl

# Upload Part1.stl to the viewer
```

### Option 4: Install Professional STEP Support (Advanced)

For direct STEP support in the app, install pythonocc:

```bash
# Using conda (recommended)
conda install -c conda-forge pythonocc-core

# Then the app could theoretically read STEP directly
# (requires additional code integration)
```

## 🎯 Recommended Workflow

**For now, the easiest approach is:**

1. **Convert STEP → STL** using one of the methods above
2. **Upload the STL** to our 3D CAD Viewer
3. The viewer will then convert STL → OBJ → GLB automatically

## Why STL Instead of STEP?

- **STL** is a mesh format (triangles) - simple and universal
- **STEP** is a parametric CAD format - contains curves, surfaces, features
- Converting STEP to STL "flattens" it into a mesh
- You lose parametric data but gain universal compatibility

## File in Your Downloads

Your `Part1.STEP` file can be converted using any of the methods above. The online converters are the fastest!

## Future Enhancement

If you frequently work with STEP files, we can enhance the app to:
1. Auto-detect STEP files
2. Suggest online converters
3. Integrate FreeCAD backend for server-side conversion
4. Add pythonocc support for native STEP reading

For now, a quick online conversion is the easiest path! 🚀
