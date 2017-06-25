from __future__ import print_function 
from ImageAnalyzer import ImageAnalyzer
from MemeRanker import MemeRanker


def get_dominant_sentiment(instance, top=1):
    """ get the top sentiments in an detected instance 
    """
    sent_score_pairs = [(key, instance['scores'][key]) for key in instance['scores']]
    sent_score_pairs.sort(key=lambda x: x[1], reverse=True)
    return sent_score_pairs[:top]

def get_bounding_box(instance):
    """ return a dictionary of format {'top': , 'left': , 'width': , 'height': } 
        representing the bounding box of the detected instance 
    """
    return instance['faceRectangle']


if __name__ == '__main__':
    # Test ImageAnalyzer 
    
    imgAnalyzer = ImageAnalyzer()
    print('ok')

    img_path = '../imgs/test2.jpg'

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
    print()


    # Retrieving bounding boxes for emotional faces 

    results = query['original_results']
    # print(results)
    # print("getting bounding box and dominant sentiment")

    sentiment_and_box = []   # a list of detected items, each item is a tuple
                            # tuple is (a list, a dictionary)
                            # the list is the top sentiments tuples (by default 1, so it's just an one-element list of the top sentiment and its score)
                            # the dictionary is the geo information of the bounding box, {'top': , 'left': , 'width': , 'height': }

    for instance in results:
        sentiment_and_box.append((get_dominant_sentiment(instance), get_bounding_box(instance)))
        
    # Now you can use sentiment_and_box to plot the bounding boxes and dominant sentiments 
    print(sentiment_and_box)
    print("get bounding box and dominant sentiment success")

    print()

    lines = memeRanker.recommend_lines(query)

    print("ranked lines returned!!!")
    print()
    print(lines)

    