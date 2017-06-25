from __future__ import print_function 
from ImageAnalyzer import ImageAnalyzer
from MemeRanker import MemeRanker

if __name__ == '__main__':
    # Test ImageAnalyzer 
    
    imgAnalyzer = ImageAnalyzer()
    print('ok')

    img_path = 'C:/git/AI-Hackathon-Challenge/captionGen/media/photos/test.jpg'

    length, top_sorted_results, original_results = imgAnalyzer.decode_emotion(img_path)
    print(length)
    print(top_sorted_results)
    print(original_results)
    print("=======emotion=======")

    title, description, keywords = imgAnalyzer.decode_context(img_path)
    print(keywords)
    print("====context======")

    # print(length)
    # print(top_sorted_results)
    # print(original_results)
    # print(title)
    # print(description)
    # print(keywords)

    print("====Analyzer test success==")

    memeRanker = MemeRanker("C:/git/AI-Hackathon-Challenge/Quotes Database/quotes_analysis_results.p")

    print('===Ranker loaded success=====')

    query = imgAnalyzer.decode_image(img_path)
    print(query)
    print("generated query")

    lines = memeRanker.recommend_lines(query)

    print("ranked lines returned!!!")
    print()
    print(lines)

    