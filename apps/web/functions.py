from .models import ImagesWeb

def populate_images():
    if ImagesWeb.objects.exists():
        print("El modelo ImagesWeb ya contiene registros. El script no se ejecutará.")
        return
    
    images_data = [
        {"name": "Index_Banner", "url": "static/web/images/index/1.png", "location": "index.html"},
        {"name": "Index_Team", "url": "static/web/images/index/2.png", "location": "index.html"},
        {"name": "Index_Donate_Banner", "url": "static/web/images/index/3.png", "location": "index.html"},
        {"name": "Index_Donate", "url": "static/web/images/index/7.png", "location": "index.html"},
        {"name": "Index_Videos", "url": "static/web/images2/video-bg-2.png", "location": "index.html"},
        {"name": "Properties_Banner", "url": "static/web/images2/banner-prop.jpg", "location": "list.html"},
        {"name": "Team_Banner", "url": "static/web/images2/banner-team.jpg", "location": "team.html"},
        {"name": "Work_Banner", "url": "static/web/images2/banner-team4.jpg", "location": "work.html"},
        {"name": "Work_Contact", "url": "static/web/images2/workwithus-page.jpg", "location": "work.html"},
        {"name": "Videos_Banner", "url": "static/web/images2/banner-media.jpg", "location": "videos.html"},
        {"name": "Contact_Banner", "url": "static/web/images2/banner-contact.jpg", "location": "contact.html"},
        {"name": "Contact_Steps", "url": "static/web/images2/banner-contact.jpg", "location": "contact.html"},
        {"name": "Contact_Steps_Banner", "url": "static/web/images2/banner-contact.jpg", "location": "contact.html"},
        {"name": "Buying_Banner", "url": "static/web/images2/banner-contact.jpg", "location": "buying.html"},
        {"name": "Buying_Buy", "url": "static/web/images2/banner-contact.jpg", "location": "buying.html"},
        {"name": "Buying_Sell", "url": "static/web/images2/banner-contact.jpg", "location": "buying.html"},
        {"name": "Calculator_Banner", "url": "static/web/images2/banner-contact.jpg", "location": "calculator.html"},
    ]

    for data in images_data:
        ImagesWeb.objects.create(**data)

if __name__ == "__main__":
    populate_images()


