import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1320,2868
B='/tmp/fonts/taj700.ttf'; M='/tmp/fonts/taj500.ttf'
def frame(src,t1,t2,out):
    c=Image.new('RGB',(W,H),(83,52,32))
    g=Image.new('L',(1,H));
    for y in range(H): g.putpixel((0,y),int(40*(1-y/H)))
    c=Image.composite(Image.new('RGB',(W,H),(120,80,50)),c,g.resize((W,H)))
    d=ImageDraw.Draw(c)
    f1=ImageFont.truetype(B,104); f2=ImageFont.truetype(M,58)
    d.text((W/2,250),t1,font=f1,fill=(247,239,226),anchor='mm',direction='rtl',language='ar')
    d.text((W/2,380),t2,font=f2,fill=(230,205,170),anchor='mm',direction='rtl',language='ar')
    s=Image.open(src).convert('RGB'); sw=1040; sh=int(s.height*sw/s.width); s=s.resize((sw,sh),Image.LANCZOS)
    x=(W-sw)//2; y=520
    m=Image.new('L',(sw,sh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,sw,sh),70,fill=255)
    sh_=Image.new('L',(W,H),0); ImageDraw.Draw(sh_).rounded_rectangle((x,y+20,x+sw,y+sh+20),70,fill=150); sh_=sh_.filter(ImageFilter.GaussianBlur(40))
    c=Image.composite(Image.new('RGB',(W,H),(30,18,10)),c,sh_)
    fr=Image.new('L',(sw+28,sh+28),0); ImageDraw.Draw(fr).rounded_rectangle((0,0,sw+27,sh+27),84,fill=255)
    c.paste((25,15,8),(x-14,y-14),fr)
    c.paste(s,(x,y),m)
    c.save(out,quality=95)
if __name__=='__main__':
    frame(*sys.argv[1:])
