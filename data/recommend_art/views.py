from http.client import HTTPResponse
import os
import jwt

from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from .models import ChangedPainting, DetailRecommendedPainting, FavoriteStyle, Painting, RecommendedPainting, SelectedPainting, UploadImage

from django.http import HttpResponse
from django.views.decorators.http import require_safe
from django.core.paginator import Paginator

from .serializers.painting import PaintingListSerializer, LikePaintSerailizer, PhotoSerializer
from .cbf_recommend import art_recommend
from .like_recommend import recommend_like_painting, find_sim_painting_item


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework import authentication, exceptions

from PIL import Image
# from .cycleGAN.model import CycleGAN
# from .cycleGAN.checkpoint import load_checkpoint
# from .cycleGAN.load_data import PhotoDataset, stringtoRGB

from .change_photo import change_p, image_encode_base64

from torch.utils.data import DataLoader
# Create your views here.
import base64
from .jwt_secret_key import JWT_SECRET_KEY, jwt_options
from django.contrib.auth import authenticate


@require_safe
@api_view(['GET'])
def index(request):
    paintings = get_list_or_404(Painting.objects.order_by('-painting_id'))
    # art_recommend()
    # print(paintings)
    serializer = PaintingListSerializer(paintings, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def recommend_detail_painting(request):
    try:
        art_recommend(20)
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=404)

@api_view(['GET', 'POST'])
def main_recommend_painting(request):
    # try:
    user, token = request.META['HTTP_AUTHORIZATION'].split(' ')
    user_decode = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS512"])
    # user_decode['id']
    selected_painting = SelectedPainting.objects.filter(member_id = user_decode['id'])
    user_recommend_painting = set()
    for painting_object in selected_painting:
        detail_recommend_painting = DetailRecommendedPainting.objects.filter(detail_painting=painting_object.painting.painting)
        user_recommend_painting.update(detail_recommend_painting)

    for paint in user_recommend_painting:
        recommended_painting = RecommendedPainting()
        recommended_painting.member_id = user_decode['id']
        recommended_painting.painting = paint.recommended_painting_id
        recommended_painting.save()
    return HttpResponse(status=200)
    # except:
    #     return HttpResponse(status=404)

@api_view(['GET', 'POST'])
def like_recommend_painting(request, pk):
    painting = Painting.objects.get(paintingId = pk)
    print(painting)
    # recommend_like_painting()
    item_sim_df = recommend_like_painting()
    like_rmd_lst = find_sim_painting_item(item_sim_df, painting.title, 20)
    rmd_id_lst = set()
    for rmd_title in like_rmd_lst:
        art = Painting.objects.get(title=rmd_title)
        rmd_id_lst.add(art)
    if len(rmd_id_lst) < 20:
        recommend_painting = DetailRecommendedPainting.objects.filter(detail_painting=pk)
        for rmd_id in recommend_painting:
            rmd_id_lst.add(rmd_id.recommended_painting_id)
            if len(rmd_id_lst) == 20:
                break
    rmd_id_lst = list(rmd_id_lst)
    serializer = LikePaintSerailizer(rmd_id_lst, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def change_photo(request, pk):
    # member_ID 받아오기 위꺼 참고 모르시는거 있으면 물어보세용!
    BASE_PATH = os.path.dirname((os.path.abspath(__file__)))
    painting = Painting.objects.get(paintingId=pk)
    base64_string = change_p(painting.artist, request.data['image'], 1)
    image_path = 'data:image/png;base64,' + base64_string #url에 저장할 것
    return HttpResponse(status=200)
    # return


@api_view(['POST'])
def test(request, format=None):
    serializers = PhotoSerializer(data = request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




