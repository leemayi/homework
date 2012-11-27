from PIL import Image, ImageDraw, ImageFont

def make_bmp():
    im = Image.new('1', (100, 100))
    #im = Image.new('L', (100, 100))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 80)
    sz = draw.textsize('A', font=font)
    pos = map(lambda i: 50-i/2, sz)
    draw.text(pos, 'A', 255, font=font)
    #im.show()
    im.save('A.bmp')

def show_bmp():
    from PIL import Image
    im = Image.open('A.bmp')
    im.show()
    data = list(im.getdata())
    print len(data)
    print data[25*100:25*100+100]

#make_bmp()
show_bmp()

