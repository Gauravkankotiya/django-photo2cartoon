from pathlib import Path
import os
############### for rest api ##################
from rest_framework.decorators import api_view
from rest_framework.response import Response
############### image conversion#############
from imageupload.test_from_code import transform
from tqdm import tqdm_notebook
from imageupload.Transformer import Transformer
import torchvision.transforms as transforms
from PIL import Image
import torch
import base64

######## For adding features
from cartoon_add.app import cartoonize

BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(['GET', 'POST'])
def img_list(request):
    s = request.POST.get('style')
    row_img = request.FILES.get('image')
    user_id = request.POST.get('id')
    
   
    
    styles = ["Hosoda", "Hayao", "Shinkai", "Paprika"]

    if s=='Normal':
        
        output300 = Image.open(row_img)
        address = os.path.join(
        BASE_DIR / 'media/cartoonize' / f"cartoonized{str(user_id)+str(row_img)}")
        output300 = output300.save(address)
        res ={
        "url": f"{address}"
    }
        return Response(res) 
    
    elif s== 'Modern':
        img_name = cartoonize(row_img)
        cartoonized_img_name = os.path.join(BASE_DIR / 'media/cartoonize' / f"cartoonized{str(user_id)+str(row_img)}")
        img_name.save(cartoonized_img_name)
        res ={
            "url": f"{cartoonized_img_name}"}
        return Response(res)
    
    elif s not in styles:
        s = 'Hosoda'

    

    models = {}

    for style in tqdm_notebook(styles):
        model = Transformer()
        model.load_state_dict(torch.load(os.path.join(
            BASE_DIR / "static/pretrained_models/", style + '_net_G_float.pth')))

        model.eval()
        models[style] = model

    
    style = s
    load_size = 1000
    output300 = transform(models, style, row_img, load_size)
    address = os.path.join(
        BASE_DIR / 'media/cartoonize' / f"cartoonized{str(user_id)+str(row_img)}")
    output300 = output300.save(address)
    res ={
        "url": f"{address}"
    }
    ######### For converting and returning bitstring of image (no storage usage) ###########
    # with open(address, "rb") as image2string:
    #     converted_string = base64.b64encode(image2string.read())
    # os.remove(address)
    # return Response(converted_string)

    return Response(res)
