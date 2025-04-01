# 🤖 CAD AI Agent - Text to 3D Model Generation

## 🌟 Overview
This project combines AI and 3D modeling to transform text descriptions into fully-realized 3D CAD models. With a simple prompt like "milk carton" or "gun," the system generates detailed 3D models ready for printing or further design work.

The project consists of two integrated components:
- **`cad_builder`**: Converts natural language descriptions into 3D CAD specifications
- **`custom_meshgpt`**: Transforms these specifications into visual 3D models using a transformer-based architecture

## ✨ Key Features
- ⚡ Text-to-3D generation powered by state-of-the-art AI
- 🔄 Multi-view training for improved object recognition
- 📊 Automated data processing and prompt creation
- 🖼️ High-quality 3D model rendering and export
- 🧰 Simple batch interface for model generation

## 📋 Sample Results

<table>
  <tr>
    <td align="center" width="50%"><b>Milk Carton</b></td>
    <td align="center" width="50%"><b>Gun</b></td>
  </tr>
  <tr>
    <td><a href="custom_meshgpt/output/gun.stl"><img src="custom_meshgpt/output/gun.stl" alt="3D Model of Gun"/></a></td>
    <td><a href="https://github.com/harsh199323/cad-ai-agent-text-to-3D/blob/1478a03eea0bae9cb6626ce118f262d05bf26f55/custom_meshgpt/output/milk_carton.stl"><img src="https://github.com/harsh199323/cad-ai-agent-text-to-3D/blob/main/custom_meshgpt/output/gun.stl" alt="3D Model of Milk Carton"/></a></td>
  </tr>
  <tr>
    <td colspan="2">
      <p align="center"><i>Models generated from simple text prompts using the CAD AI Agent</i></p>
    </td>
  </tr>
</table>

## 📂 Project Structure
```
├── cad_builder
│   ├── README.md
│   ├── setup.py
│   ├── requirements.txt
│   ├── data_processors
│   │   ├── create_prompts.py
│   │   ├── data_loader_raw.py
│   │   └── data_loader_prepared.py
│   ├── utils
│   └── scripts
│       ├── create_views.py
│       └── download_data.py
│
├── custom_meshgpt
│   ├── README.md
│   ├── setup.py
│   ├── create_3d_model.bat
│   └── main.py
│   └── output
│
└── gitignore
└── README.md
```

## 🛠️ Installation & Setup

### ✅ Requirements
- Python 3.10 – 3.12
- CUDA-compatible GPU (recommended for faster processing)

### 🔹 Setup for `cad_builder`

```bash
# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate   # Linux/macOS
.\venv\Scripts\activate    # Windows

# Install dependencies
pip install -r cad_builder/requirements.txt

# Install package
cd cad_builder
python setup.py install
```

### 🔹 Setup for `custom_meshgpt`

```bash
cd custom_meshgpt
install_package.bat
```

## 🚀 Usage Guide

### 🔸 Creating CAD Models from Prompts

1. **Load and save STL files**
   ```bash
   python cad_builder/scripts/download_data.py
   ```

2. **Generate multiple views from STL files**
   ```bash
   python cad_builder/scripts/create_views.py
   ```

3. **Create prompts for AI model**
   ```bash
   python cad_builder/cad_builder/data_processors/create_prompts.py
   ```

### 🔸 Generating 3D Models with MeshGPT

1. **Start the model generation process**
   ```bash
   cd custom_meshgpt
   .\create_3d_model.bat
   ```

2. **Enter a description** when prompted (e.g., "milk carton", "gun", "chair")

3. **Retrieve your model** from the `custom_meshgpt/output` directory

### 🔸 Example Generation Process

```
(cad_env) PS D:\path\to\custom_meshgpt> .\create_3d_model.bat
⌛ Loading model...
loading saved model at version 1.2.17, but current package version is 1.7.0
⌛ Loading model...
loading saved model at version 1.2.17, but current package version is 1.7.0
🎨 Describe the object (e.g., sofa, bed, etc.): milk carton
61%|████████████████████████████                | 912/1500 [00:34<00:22, 26.38it/s]
🔵 Original Faces Coordinates Shape: (1, 152, 3, 3)
✅ Processed Vertices Shape: (87, 3)
✅ Processed Faces Shape: (152, 3)
✅ Mesh saved to output\milk_carton.obj
✅ Rendering saved as 'output\milk_carton.stl'
```

## 🧠 Technical Approach

### 🔹 Natural Language to 3D Model Pipeline
The system uses a sophisticated pipeline to convert text descriptions into 3D models:

1. **Text Input** → User provides simple description
2. **Prompt Processing** → Text is converted to structured input
3. **AI Generation** → MeshGPT generates 3D mesh coordinates
4. **Rendering** → Model is visualized and exported

### 🔹 Multi-View Training Strategy
The system learns object characteristics from multiple 2D perspectives:

- Front, side, top, and isometric views are generated for training data
- Multiple perspectives help the model understand 3D relationships
- Enhanced accuracy in reproducing complex geometric features

### 🔹 Mesh Transformation Technology
The MeshGPT model serves as the core technology:

- Generates vertices and faces for complex 3D shapes
- Handles a wide range of object types (furniture, containers, tools, etc.)
- Optimizes mesh topology for printing and visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a pull request

## 🏆 Technologies Used

- **Python** - Core programming language
- **PyTorch** - Deep learning framework
- **Hugging Face Transformers** - Model architecture
- **Trimesh** - 3D rendering and manipulation
- **CUDA** - GPU acceleration

## 📝 Notes

- Model version mismatch (1.2.17 vs 1.7.0) doesn't affect functionality
- Generation speed depends on GPU capability (~25-26 iterations/second on standard hardware)
- Objects are processed by generating vertices and faces for complex 3D shapes
- Current sample outputs include everyday objects like milk cartons and more complex items like guns
