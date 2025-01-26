def filter_source_files(files: dict, valid_files: list, extensions: list) -> tuple:
    """
    Filter files and valid_files based on allowed extensions.

    Args:
        files (dict): Dictionary of file paths and their content.
        valid_files (list): List of valid file paths.
        extensions (list): List of file extensions to include.

    Returns:
        tuple: Filtered files and valid_files.
    """
    filtered_files = {
        path: content
        for path, content in files.items()
        if any(path.endswith(ext) for ext in extensions)
    }
    filtered_valid_files = [
        file for file in valid_files if any(file.endswith(ext) for ext in extensions)
    ]
    return filtered_files, filtered_valid_files
