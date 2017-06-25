from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_protect
from .forms import PhotoForm
from .models import Photo
from .MemeRanker import MemeRanker
from .ImageAnalyzer import ImageAnalyzer

# Create your views here.
def index(request):

   return render(request, 'imagemovie/index.html',{})


@csrf_protect
def getcap_ajax(request):
   form = PhotoForm(request.POST, request.FILES)
   if form.is_valid():
      photo = form.save()
      url = '/media/photos/test.jpg'
      caption,return_path =  get_quote('.'+photo.file.url)
      # caption = ["The whole problem with the world is that fools and fanatics are always so certain of themselves, and wiser people so full of doubts.",
      #            "The greater danger for most of us lies not in setting our aim too high and falling short, but in setting our aim too low, and achieving our mark.",
      #            "I can write better than anybody who can write faster, and I can write faster than anybody who can write better."]
      data = {'is_valid': True,'caption': caption,'name': photo.file.name, 'url': return_path}
   else:
      data = {'is_valid': False}
   return JsonResponse(data)


def get_quote(imgpath):
   imgAnalyzer = ImageAnalyzer()
   print('ok')

   img_path = imgpath

   length, top_sorted_results, original_results = imgAnalyzer.decode_emotion(img_path)

   print("emotion")

   title, description, keywords = imgAnalyzer.decode_context(img_path)

   print("context")

   # print(length)
   # print(top_sorted_results)
   # print(original_results)
   # print(title)
   # print(description)
   # print(keywords)

   print("Analyzer test success")

   memeRanker = MemeRanker("../Quotes Database/quotes_analysis_results.p")

   print('Ranker loaded success')

   query = imgAnalyzer.decode_image(img_path)

   print("generated query")

   lines = memeRanker.recommend_lines(query)

   print("ranked lines returned!!!")
   print()
   print(lines)
   lines=[l[0] for l in lines]
   return lines,query['path_name']
