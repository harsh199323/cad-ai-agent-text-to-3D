import warnings
warnings.filterwarnings("ignore")

import trimesh
import torch
import numpy as np
from meshgpt_pytorch import MeshTransformer
import os  # Required for directory and path operations

def process_mesh(faces_coordinates, vertices_per_face=3):
    """
    Processes MeshGPT output to extract unique vertices and corresponding face indices.
    
    Args:
        faces_coordinates: The raw face coordinates from the model.
        vertices_per_face: Number of vertices per face (default is 3 for triangles).
    
    Returns:
        tuple: (vertices, faces) containing unique vertices and face indices.
    """
    faces_coordinates = faces_coordinates.squeeze(0)
    num_faces = faces_coordinates.shape[0]
    all_vertices = faces_coordinates.reshape(-1, 3)
    unique_vertices, indices = np.unique(all_vertices, axis=0, return_inverse=True)
    faces = indices.reshape(num_faces, vertices_per_face)
    return unique_vertices, faces

def save_rendering(render_path, faces_coordinates, vertices_per_face=3):
    """
    Saves the generated 3D mesh to the specified file path.
    
    Args:
        render_path (str): Path where the mesh will be saved (e.g., "output/sphere.obj").
        faces_coordinates: The raw face coordinates from the model.
        vertices_per_face: Number of vertices per face (default is 3).
    """
    try:
        vertices, faces = process_mesh(faces_coordinates, vertices_per_face)
        print(f"🔍 Original Faces Coordinates Shape: {faces_coordinates.shape}")
        print(f"✅ Processed Vertices Shape: {vertices.shape}")
        print(f"✅ Processed Faces Shape: {faces.shape}")
        if faces.max() >= len(vertices):
            raise ValueError(f"❌ Face indices exceed vertex count! Max index: {faces.max()}, Vertex Count: {len(vertices)}")
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        mesh.export(render_path)
        print(f"✅ Mesh saved to {render_path}")
    except Exception as e:
        print(f"❌ Error while saving rendering: {e}")

# Load Model
print("⏳ Loading model...")
device = "cuda" if torch.cuda.is_available() else "cpu"

try:
    transformer = MeshTransformer.from_pretrained("MarcusLoren/MeshGPT-preview").to(device)
except Exception as e:
    print(f"❌ Error loading MeshGPT model: {e}")
    exit(1)

# Get user input
user_input = input("🎨 Describe the object (e.g., sofa, bed, etc.): ")

try:
    # Generate the mesh
    with torch.amp.autocast('cuda', enabled=(device == 'cuda')):
        output = transformer.generate(texts=[user_input], temperature=0.0)

    faces_coordinates = output[0].cpu().numpy()

    # Sanitize user input for filename (replace spaces with underscores)
    file_name = user_input.replace(" ", "_")
    output_folder = "output"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the full file paths
    obj_path = os.path.join(output_folder, f"{file_name}.obj")
    stl_path = os.path.join(output_folder, f"{file_name}.stl")

    # Save the OBJ file
    save_rendering(obj_path, faces_coordinates, vertices_per_face=3)

    # Load the OBJ file and convert to STL
    mesh = trimesh.load_mesh(obj_path)
    if not isinstance(mesh, trimesh.Trimesh):
        raise TypeError("❌ Error: Mesh object is not a valid Trimesh instance!")
    mesh.export(stl_path)
    print(f"✅ Rendering saved as '{stl_path}'")

except Exception as e:
    print(f"❌ Error during mesh generation: {e}")