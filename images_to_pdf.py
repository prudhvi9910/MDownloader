from PIL import Image
import os

def helper_func(element):
    """
    """
    value = element.split('.')[0]
    return int(value)

def delete_images(main_path, paths):
    """
    """
    for path in paths:
        filepath = os.path.join(main_path, path)
        os.remove(filepath)

def images_to_pdf(path):
    """
    """
    with os.scandir(path) as dirs:
        paths = []
        for file in dirs:
            paths.append(file.name)
        dirs.close()
    paths.sort(key=helper_func)
    img_list = []
    for file in paths:
        filepath = os.path.join(path, file)
        img = Image.open(filepath)
        im = img.convert('RGB')
        img_list.append(im)
    if len(img_list)>1:
        path_to_save = os.path.join(path, '..', 'pdf')
        if not os.path.isdir(path_to_save):
            os.makedirs(path_to_save)
        path_to_save = os.path.join(path_to_save, path.split('\\')[-1]+'.pdf')
        img_list[0].save(path_to_save, save_all=True, append_images=img_list[1:])
        delete_images(path, paths)
        return path_to_save
    return "Oka file e unapudu pdf conversion ki badhakam e, poyi chesko nen cheyanu"


if __name__ == "__main__":
    path = input("Path of files:")
    print(images_to_pdf(path))