from cad_builder.data_processors.data_loader_raw import download_and_save_data, get_annotations


annotations = get_annotations(100)
download_and_save_data(data=annotations)


