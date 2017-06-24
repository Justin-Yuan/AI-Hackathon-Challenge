from __future__ import print_function 
from ImageAnalyzer import ImageAnalyzer

if __name__ == '__main__':
    # Test ImageAnalyzer 
    
    imgAnalyzer = ImageAnalyzer()
    print('ok')

    img_path = '../imgs/test2.jpg'

    emotion_result = imgAnalyzer.get_emotion(img_path)
    print(emotion_result)

    print()
    context_result = imgAnalyzer.get_context(img_path)
    print(context_result)
    print()

    length, top_sorted_results = imgAnalyzer.decode_emotion(img_path)

    print("emotion")

    title, description, keywords = imgAnalyzer.decode_context(img_path)

    print("context")

    print(length)
    print(top_sorted_results)
    print(title)
    print(description)
    print(keywords)

    