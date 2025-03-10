import requests
import json
import time


def facebookPost(product):
    print(product)
    ACCESS_TOKEN = 'EAAHabAEq3VQBOwYEUStOyZA6iiWUZB4E0o7f4wTSoienRm56v1vkewjnYjpL0NZCBF60TLmqZCFtyD0ESJZBZBP20sUF2vjx80GKnLBqqppsn15tlTXXLjl6I2CX1ZAoYPzZAGvMMv5npimc5dpJ6rEeyyvgNZATjZBcM1LIasyRtxPQbZBfrZC6CFs8Am8Wedw588mZB8WRKVJVns0bxKRYF'
    PAGE_ID = '473895905817736'
    url = f'https://graph.facebook.com/{PAGE_ID}/feed'

    # Data scraped (replace these with your actual data from scraping)
    item_name = product['product_name']
    item_price = product['price']
    item_sizes = product['sizes']
    image_src_arr = product['img_urls']

    # Caption for the post
    caption = f"Check out our latest item: {item_name}\nPrice: {item_price}\nSizes: {item_sizes}"

    # Step 1: Upload image to Facebook (unpublished)
    photo_payload = {
        'url': image_src_arr,
        'published': False,  # Important for scheduling
        'access_token': ACCESS_TOKEN
    }
    photo_response = requests.post(
        f'https://graph.facebook.com/v19.0/{PAGE_ID}/photos', data=photo_payload)
    photo_data = photo_response.json()

    if 'id' in photo_data:
        photo_id = photo_data['id']
        print(f"Image uploaded successfully! Photo ID: {photo_id}")
    else:
        print("Error uploading image:", photo_response.text)
        exit()

    # Prepare the payload for the post
    payload = {
        'message': caption,
        'attached_media': json.dumps([{'media_fbid': photo_id}]),
        'scheduled_publish_time': int(time.time()) + (30 * 24 * 60 * 60),
        'published': False,  # Important for scheduling
        'access_token': ACCESS_TOKEN
    }

    print(json.dumps([{'media_fbid': photo_id}]))

    # Send the request to Facebook Graph API to upload the image and post
    response = requests.post(url, data=payload)

    # Check if the post was successful
    if response.status_code == 200:
        print("Post successful!")
        post_id = response.json()['id']
        print(f"Post ID: {post_id}")
    else:
        print("Error posting to Facebook:", response.text)
