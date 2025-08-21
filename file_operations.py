import os

def add_suffix(file_path, suffix):
    """Adds a suffix to the filename before the extension."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"
    
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}{suffix}{ext}"
    new_file_path = os.path.join(directory, new_filename)
    
    try:
        os.rename(file_path, new_file_path)
        return f"Renamed: {filename} -> {new_filename}"
    except OSError as e:
        return f"Error renaming {filename}: {e}"

def remove_suffix(file_path, suffix):
    """Removes a specific suffix from the filename before the extension."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"

    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    
    if name.endswith(suffix):
        new_name = name[:-len(suffix)]
        new_filename = f"{new_name}{ext}"
        new_file_path = os.path.join(directory, new_filename)
        try:
            os.rename(file_path, new_file_path)
            return f"Renamed: {filename} -> {new_filename}"
        except OSError as e:
            return f"Error renaming {filename}: {e}"
    else:
        return f"Error: Suffix '{suffix}' not found in {filename}"

def add_prefix(file_path, prefix):
    """Adds a prefix to the filename."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"
    
    directory, filename = os.path.split(file_path)
    new_filename = f"{prefix}{filename}"
    new_file_path = os.path.join(directory, new_filename)
    
    try:
        os.rename(file_path, new_file_path)
        return f"Renamed: {filename} -> {new_filename}"
    except OSError as e:
        return f"Error renaming {filename}: {e}"

def remove_prefix(file_path, prefix):
    """Removes a specific prefix from the filename."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"

    directory, filename = os.path.split(file_path)
    
    if filename.startswith(prefix):
        new_filename = filename[len(prefix):]
        new_file_path = os.path.join(directory, new_filename)
        try:
            os.rename(file_path, new_file_path)
            return f"Renamed: {filename} -> {new_filename}"
        except OSError as e:
            return f"Error renaming {filename}: {e}"
    else:
        return f"Error: Prefix '{prefix}' not found in {filename}"

def find_and_replace(file_path, find_text, replace_text):
    """Finds and replaces text in the filename (excluding extension)."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"

    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)

    if find_text in name:
        new_name = name.replace(find_text, replace_text)
        new_filename = f"{new_name}{ext}"
        new_file_path = os.path.join(directory, new_filename)
        try:
            os.rename(file_path, new_file_path)
            return f"Renamed: {filename} -> {new_filename}"
        except OSError as e:
            return f"Error renaming {filename}: {e}"
    else:
        return f"Error: Find text '{find_text}' not found in {filename}"

def change_extension(file_path, old_extension, new_extension):
    """Changes the extension of the file only if it matches the old extension."""
    if not os.path.exists(file_path):
        return f"Error: File not found - {file_path}"

    directory, filename = os.path.split(file_path)
    name, current_ext = os.path.splitext(filename)

    # Normalize extensions to ensure they start with a dot
    if not old_extension.startswith('.'):
        old_extension = '.' + old_extension
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    if current_ext == old_extension:
        new_filename = f"{name}{new_extension}"
        new_file_path = os.path.join(directory, new_filename)
        try:
            os.rename(file_path, new_file_path)
            return f"Renamed: {filename} -> {new_filename}"
        except OSError as e:
            return f"Error renaming {filename}: {e}"
    else:
        return f"Skipped: {filename} (extension did not match '{old_extension}')"