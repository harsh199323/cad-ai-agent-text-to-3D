import os
import requests
import objaverse.xl as oxl
from cad_builder.utils import find_project_root


def get_annotations(number_stl_files):
    project_root = find_project_root(os.path.dirname(__file__))
    download_dir = os.path.join(project_root, f'cad_builder/data/raw/annotations')
    os.makedirs(download_dir, exist_ok=True)
    annotations = oxl.get_annotations(
        download_dir=download_dir
    )
    annotations = annotations[(annotations["fileType"]=="stl") &
                              (annotations["source"]=="github")]
    sampled_df = annotations.sample(number_stl_files, random_state=42)
    return sampled_df

def download_and_save_data(data):
    project_root = find_project_root(os.path.dirname(__file__))
    download_dir = os.path.join(project_root, f'cad_builder/data/raw/stl')
    os.makedirs(download_dir, exist_ok=True)

    urls = data['fileIdentifier']

    for _, url in enumerate(urls):
        if url.startswith("https://"):
            url = url.replace("/blob/", "/")
            url = url.replace("https://", "https://raw.")
            filename = os.path.basename(url)
            filepath = os.path.join(download_dir, filename)

            try:
                response = requests.get(url)
                response.raise_for_status() 

                with open(filepath, "wb") as file:
                    file.write(response.content)
                print(f"Downloaded {filename} to {filepath}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to download {url}: {e}")





