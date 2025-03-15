from PIL import Image, ImageDraw, ImageFont


def generate_photo(zp, title):
    if len(title) > 28:
        image = Image.open("image.jpg")
        first_line = ''
        second_line = ''
        count = 0

        # Разделение строки на две
        for i in title:
            count += 1
            if count <= 28:
                first_line += i
            else:
                second_line += i

        font = ImageFont.truetype("Trigram.ttf", 60)
        font2 = ImageFont.truetype("Trigram.ttf", 40)
        drawer = ImageDraw.Draw(image)
        drawer.text((150, 400), first_line, font=font, fill='white')
        drawer.text((150, 460), second_line, font=font, fill='white')
        drawer.text((150, 600), zp, font=font2, fill='white')

        image.save('new_img.jpg')

    else:
        image = Image.open("image.jpg")

        font = ImageFont.truetype("Trigram.ttf", 60)
        font2 = ImageFont.truetype("Trigram.ttf", 40)
        drawer = ImageDraw.Draw(image)
        drawer.text((150, 400), title, font=font, fill='white')
        drawer.text((150, 500), zp, font=font2, fill='white')

        image.save('new_img.jpg')



