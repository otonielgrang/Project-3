# CPS121 Project 3
# Written: <date> <fullname> <email>
# 
# <Include description of program here>
##
# Change each occurrence of "_" in the list below to be "Y" or "N" to indicate
# whether or not the given transformation is implemented in your program.
#
#   Can be done using just getPixels()
#   Y Altering colors of the image
#   _ Grayscale
#   Y Making darker or lighter
#   _ Sepia-toned
#   _ Posterized
#   Need nested loops
#   Y Mirrorizing
#   Y Edge detection
#   Y Chromakey (change background)
#   _ Blurring
#   Need nested loops and alter size or shape
#   Y Rotation
#   Y Cropping
#   _ Shifting
#   Other transformations
#   Y Resizing
#   Y Pixelation / mosaic effect (grid-based averaging)
#   Y Color channel attenuation / red–blue combination
# ============================================================================

import GCPictureTools as pgt
import pygame as pg
import os, sys
import traceback
import math
# ============================================================================
# ================ Start making changes after this comment ===================
# ============================================================================

# ---- SUPPORTING FUNCTIONS SHOULD GO HERE ----

def createCollage():
    """Create a collage.
 
    Returns
    -------
    Picture
        the collage.
    """
    # create "canvas" on which to make a collage.  You may exchange the
    # width and height values if you prefer a landscape orientation.
    collage = pgt.Picture(2000, 1200)

    # ---- YOUR CODE TO BUILD THE COLLAGE GOES HERE ----
    # Notice that this is **inside** the createCollage() function.  Because
    # createCollage() should be a "one-and-only-one-thing" function, you
    # should use supporting functions to do transformations, etc.  These
    # supporting functions should be defined below, after the code for this
    # function.
    
    cat = combineBR(resize(pgt.Picture('deadC.png'),400,400),resize(pgt.Picture('aliveC.png'),400,400))
    dead = lowChannel(cat,fb=0.0)
    alive = lowChannel(cat,fr=0.0)

    cat = illuminate(cat,1.3)
    dead = illuminate(dead,1.3)
    alive = illuminate(alive,1.3)

    butterfly = lowChannel(resize(pgt.Picture('butterfly.jpg'),400,400),fr=0.8,fb=0.8,fg=0.8)
    flowers = resize(pgt.Picture('flowers.jpg'),400,400)
    night = resize(pgt.Picture('night.jpg'),400,400)

    edge = edgeDetection(butterfly,colT=(0,255,0),tol = 5)
    front = chromaKey(edge,flowers,(0,255,0))
    front = chromaKey(front,night,(255,255,255))

    butterfly = chromaKey(butterfly,night,(255*0.8,255*0.8,255*0.8))
    edge = chromaKey(edge,night,(255,255,255))

    link = pgt.Picture('linkm.jpg')
    lw,lh = getSize(link)
    link = resize(cropIt(link,round(lw-(lw*0.3)),lh),400,400)
    lw,lh = getSize(link)
    plink = resize(reduceGridQuality(link,3),lw,lh)
    pplink = resize(reduceGridQuality(plink,9),lw,lh)

    meme = resize(pgt.Picture('meme.jpg'),400,1200)
    memeinv = negative(flip(meme))


    cat.copyInto(collage, 0, 0)
    alive.copyInto(collage, 400, 0)
    dead.copyInto(collage, 800, 0)

    butterfly.copyInto(collage,0,400)
    edge.copyInto(collage,400,400)
    front.copyInto(collage,800,400)

    link.copyInto(collage,0,800)
    plink.copyInto(collage,400,800)
    pplink.copyInto(collage,800,800)

    meme.copyInto(collage,1200,0)
    memeinv.copyInto(collage,1600,0)
    return resize(collage,1000,600)

def createWebPage(imageFile, webPageFile):
    """Create web page that contains the collage.
    Parameter: imageFile - the image file name 
    Parameter: webPageFile - the finename of the output web page 
    Returns
    -------
    nothing
    """
    with  open(webPageFile, "wt") as f:
    
    # ---- YOUR CODE TO BUILD THE Webpage with the COLLAGE GOES HERE ----
        f.write(createDocType())
        f.write(startHTML())
        f.write("<head>\n")
        f.write("<title> CPS121 PROJECT 3 | Otoniel Matute</title>\n")
        f.write("</head>\n")
        f.write(startBody())
        f.write(createHeading('Here I present my Collage:',1))
        f.write(createParagraph('It was created using a wide range of image-processing techniques, including color manipulation, geometric transformations, pixel-level resampling, and edge-based compositing.'))
        f.write(createImage(imageFile,'collage'))
        f.write(endBody())
        f.write(endHTML())

        print("output file:", f.name)
    
### In the next lines: related html creation functions.

def createDocType():
    return '<!DOCTYPE html>\n'

def startHTML():
    return '<html>\n\n'

def endHTML():
    return '</html>\n\n'
def startBody():
    return '<body>\n\n'

def endBody():
    return '</body>\n\n'

def createParagraph(string):
    string = f'<p>{string}</p>\n'
    return string

def createHead(string):
    string = '<head><title>'+string+'</title></head>\n\n'
    return string

def createHeading(string,n):
    string = f'<h{n}> {string} </h{n}>\n'
    return string

def createLink(link,name):
    string = f'<a href="{link}">{name}]</a>'
    return string

def createImage(source,alt):
    string = f'<img src="{source}" alt="{alt}"/>'
    return string
def reduceGridQuality(pic = pgt.Picture, kernel=1):
    '''
    Purpose:
    Reduce the Image quality using a kernel to take the avarage color of pixels, inserting them in a new image.

    Arguments:
    pic (pgt.Picture):
        Picture to bre reduced
    Kernel (Int):
        Size (width,length) of kernel, has to be odd. Ex 1x1 or 3x3
    ...
    paramN (type):
        Description of this parameter.

    Returns:
    newPic (pgt.Picture):
        Returns the new reduced picture.

    Raises:
    ExceptionType:
        Condition under which this exception is raised.
    AnotherExceptionType:
        Explanation of when this other exception may occur.
    '''
    
    w,h = getSize(pic)
    if kernel <= 0:
        raise ValueError("kernel must be a positive integer")
    if kernel % 2 == 0:
        raise ValueError("kernel must be an odd integer")
    if kernel > w or kernel > h:
        raise ValueError("kernel size cannot be larger than the image dimensions")
    
    nw,nh = w//kernel,h//kernel
    copy = pgt.Picture(pic)
    newPic = pgt.Picture(nw,nh)
    for ix in range(nw):
        for iy in range(nh):
            newPic.setColor(ix, iy, NKernel(copy,kernel,(ix,iy),(w,h)))

    return newPic



def NKernel(pic,kernel,cord,p_size):

     # Cordinates of the center of the kernel relative to pic
    radius = kernel//2
    w,h = p_size
    cx, cy  = cord[0] * kernel + radius , cord[1] * kernel+radius

    x_start = max(cx - radius, 0)
    x_end = min(cx + radius, w -1)

    y_start = max(cy - radius, 0)
    y_end = min(cy + radius, h - 1)

    r_array,g_array,b_array = [],[],[]

    for iy in range(y_start, y_end + 1):
        for ix in range(x_start , x_end +1 ):
            r, g, b = pic.getColorRGB(ix, iy)
            r_array.append(r)
            g_array.append(g)
            b_array.append(b)

    rs,gs,bs = sum(r_array)/len(r_array),sum(g_array)/len(g_array),sum(b_array)/len(b_array)
    return tuple(round(v) for v in (rs, gs, bs))

def gCalc(old, new):
    '''
    Purpose:
        Compute the start and end indices (exclusive) for a centered crop.

    Arguments:
        old (int):
            Original size (width or height) of the image.
        new (int):
            Desired new size (width or height) for the crop.

    Returns:
        (int, int):
            A pair (start, end).
    '''
    start = old // 2 - new // 2
    end = start + new          # Carefull end is Exclusive
    return start, end



def cropIt(pic, nWidth, nHeight):
    '''
    Purpose:
        Create a centered crop of the given picture with the desired width
        and height.

    Arguments:
        pic (pgt.Picture):
            Original picture to be cropped.
        nWidth (int):
            Width of the cropped image.
        nHeight (int):
            Height of the cropped image.

    Returns:
        npic (pgt.Picture):
            A new picture containing the centered crop.

    Raises:
        ValueError:
            If the requested crop size is larger than the original image.
    '''
    width,height = getSize(pic)
     

   
    if nWidth > width or nHeight > height:
        raise ValueError("Crop size cannot be larger than the original image")

 
    x1, x2 = gCalc(width, nWidth)   # x in [x1, x2)
    y1, y2 = gCalc(height, nHeight) # y in [y1, y2)

    
    nPic = pgt.Picture(nWidth, nHeight)

   
    new_y = 0
    for y in range(y1, y2):
        new_x = 0
        for x in range(x1, x2):
            color = pic.getColor(x, y)
            nPic.setColor(new_x, new_y, color)
            new_x += 1
        new_y += 1

    return nPic

def resize(pic = pgt.Picture, n_width=0 ,n_height=0):
    '''
    Purpose:
        Resize an image from its original size to a new width and height
        using area based recalculation. Each pixel in the new image corresponds
        to a fractional rectangle in the original image

    Arguments:
        pic (pgt.Picture):
            The original picture to be resized
        n_width (int):
            The desired width of the output image. Must be greater than 0
        n_height (int):
            The desired height of the output image. Must be greater than 0

    Returns:
        new (pgt.Picture):
            A new picture object containing the resized image

    Raises:
        ValueError:
            Raised if n_width or n_height is less than or equal to zero
    '''
    if n_width <= 0 or n_height <=0:
        raise ValueError('New size must be positive')
    
    copy = pgt.Picture(pic)
    new = pgt.Picture(n_width,n_height)

    width,height = getSize(copy)
     

    sx = width / n_width
    sy = height /n_height
    
    for iy in range(n_height):
        for ix in range(n_width):
            new.setColor(ix,iy, sampleAreaColor(copy,(width,height), (ix,iy), (sx,sy)))
    return new

def sampleAreaColor(pic = pgt.Picture, size = () ,new_cord = (), s_cord = ()): 
    '''
    Purpose:
        Compute the color of a single pixel in the resized image using
        area resampling. The function uses a rectangular area
        in the original image that corresponds to the target pixel and
        computes a weighted average of all overlapping source pixels.
        Weights are proportional to the area of overlap between each
        source pixel and the sampling rectangle.

    Arguments:
        pic (pgt.Picture):
            The original image being sampled
        size (tuple[int, int]):
            (width, height) of the original image.
        new_cord (tuple[int, int]):
            (nx, ny) coordinates of the pixel in the new image
        s_cord (tuple[float, float]):
            (sx, sy) scale factors describing how much of the original
            image corresponds to a single pixel in the new image

    Returns:
        tuple[int, int, int]:
            An (R, G, B) tuple representing the weighted color of the
            sampling region.

    '''


    w, h = size
    
    nx,ny = new_cord

    sx,sy = s_cord
    cs = sx * sy

    x0 = nx * sx 
    y0 = ny * sy

    x1 = x0 + sx
    y1 = y0 + sy

    x_start = max(math.floor(x0), 0)
    x_end = min(math.floor(x1) , w -1)

    y_start = max(math.floor(y0), 0)
    y_end = min(math.floor(y1) , h - 1)

    r_sum,g_sum,b_sum = 0,0,0

    for iy in range(y_start,y_end+1):
        for ix in range(x_start,x_end+1):
            overlap_x = min(x1,ix +1) - max(x0, ix) 

            if overlap_x < 0:
                continue

            overlap_y = min(y1,iy +1) - max(y0, iy) 

            if overlap_y < 0:
                continue

            weight = (overlap_x * overlap_y) / (cs) # Area of the overlap in that pixel, divided by the total area of the sample

            r, g, b = pic.getColorRGB(ix, iy)

            r_sum += (r*weight)
            g_sum += (g*weight)
            b_sum += (b*weight)

   

    return tuple(round(v) for v in (r_sum, g_sum, b_sum))


def chromaKey(fg_pic = pgt.Picture,bg_pic = pgt.Picture ,key = (0,0,0),tol = 20):

    fg_w,fg_h = getSize(fg_pic)
    bg_w,bg_h = getSize(bg_pic)

    Kr,Kg,Kb = key

    if  fg_w != bg_w or  fg_h != bg_h:
        raise ValueError('The Pictures size should be the same')
    
    Outp = pgt.Picture(fg_w,fg_h)

    for iy in range(fg_h):
        for ix in range(fg_w):
            Fr, Fg, Fb = fg_pic.getColorRGB(ix, iy)
            Br, Bg, Bb = bg_pic.getColorRGB(ix,iy)
            
            dis = distance(colors=((Fr, Fg, Fb),(Kr,Kg,Kb)),euclid=True)

            if dis < tol:
                Outp.setColor(ix,iy,(Br,Bg,Bb))
            else:
                Outp.setColor(ix,iy,(Fr,Fg,Fb))
    return Outp


# EXTRACTED FROM LAB 9. Authors: Otoniel Matute, Jimin Lim
def R90R(pic):
   
   w,h = getSize(pic)
   
   canvas = pgt.Picture(h, w)
   for y in range(w):
      for x in range(h):
         color = pic.getColor(y,x)
         canvas.setColor(w-1-x, y, color)
   return canvas

def R90L(pic):
   '''Rotate A picture 90 degrees to the left.
      Args:
         pic: Picture to be rotated.
      Returns:
         rPic: Picutre rotated.
   '''
   w,h = getSize(pic)
    

   canvas = pgt.Picture(h, w)
   for y in range(w):
      for x in range(h):
         color = pic.getColor(y,x)
         canvas.setColor(x, w-1-y, color)
   
   return canvas

def Rotate(pic, direction, t):
   '''Rotate A picture N number of times 90 degrees to the left or right.
      Args:
         pic: Picture to be rotated.
         Direction: Left or Right.
         t: Number of times to be rotated.
      Returns:
         rPic: Picutre rotated.
   '''
   copypic = pgt.Picture(pic)

   if direction != 'l' and direction != 'r':
      print('Invalid Direction')

   direction, t = efficientLogic(direction,t)
   for _ in range(t):

      if direction ==  'r':
         copypic = R90R(copypic)

      if direction ==  'l':
         copypic = R90L(copypic)
   return copypic

def efficientLogic(D, T):
   '''Logic for a more efficient rotation without uneccesary iterations.
      Args:
         D: Left or Right.
         T: Number of times to be rotated.
      Returns:
         eD: Efficient Direction
         eT: Efficient Rotation Times.
         As a tuple
   '''
   eT = T % 4
   eD = D
   if eT == 3:
      if eD == 'r':
         eD = 'l'
      elif eD == 'l':
         eD = 'r'
      eT = 1
   
   return (eD,eT)
#########################################################

def edgeDetection(pic=pgt.Picture,tol=20,colT= (0,0,0),colF = (255,255,255)):
    w,h = getSize(pic)
    out = pgt.Picture(w,h)

    for iy in range(h-1):
        for ix in range(w-1):
            pix_source = pic.getPixel(ix,iy)
            source_color = pix_source.getColorRGB()
            pix_R =pic.getPixel(ix+1,iy)
            pix_D = pic.getPixel(ix,iy+1)
            R_dis = distance((pix_R.getColorRGB(),source_color),True)
            D_dis = distance((pix_D.getColorRGB(),source_color),True)
            if R_dis> tol or D_dis > tol:
                out.setColor(ix,iy,colT)
            else:
                out.setColor(ix,iy,colF)
    return(out)

def distance(colors=((0,0,0),(0,0,0)), euclid = False, other = ((0,0),(0,0))):

    
    dis = 0
    
    if euclid:
        r,g,b = colors[0]
        r1,g1,b1 = colors[1]

        if 255 < r < 0 or 255 < g < 0 or 255< b < 0:
            raise ValueError('Color out of range: [0,255]')
        if 255 < r1 < 0 or 255 < g1 < 0 or 255 < b1 < 0:
            raise ValueError('Color out of range: [0,255]')
        dr,dg,db = r-r1,g-g1,b-b1
        dis = math.sqrt(dr*dr + dg*dg + db*db)
    else:
        v1,v2 = other[0]
        v3,v4 = other[1]
        dv1,dv2 =v1-v3,v2-v4
        dis = math.sqrt(dv1*dv1 + dv2*dv2)
    return dis

def combineBR(picR=pgt.Picture,picB=pgt.Picture):

    rW,rH = getSize(picR)
    bW,bH = getSize(picB)

    if rW != bW or rH != bH:
        raise ValueError('The pictures size should be the same.')
    out = pgt.Picture(rW,rH)
    for iy in range(rH):        
        for ix in range(rW):
            r = sum(picR.getColorRGB(ix,iy))/3
            b = sum(picB.getColorRGB(ix,iy))/3
            out.setColor(ix,iy,(r*0.5,0,b))
    return out

def lowChannel(pic = pgt.Picture, fr = 1.0, fg = 1.0 , fb = 1.0):

    if not (0 <= fr <= 1):
        raise ValueError("fr must be between 0 and 1")
    if not (0 <= fg <= 1):
        raise ValueError("fg must be between 0 and 1")
    if not (0 <= fb <= 1):
        raise ValueError("fb must be between 0 and 1")
    
    w,h = getSize(pic)
    out = pgt.Picture(w,h)
    for iy in range(h):
        for ix in range(w):
            r,g,b = pic.getColorRGB(ix,iy)
            out.setColor(ix,iy,(r*fr,g*fg,b*fb))
    return out
def illuminate(pic = pgt.Picture, lum = 1.0):

    w,h = getSize(pic)
    out = pgt.Picture(w,h)

    for iy in range(h):
        for ix in range(w):
            r,g,b = pic.getColorRGB(ix,iy)
            r = round(min(255, r * lum))
            g = round(min(255, g * lum))
            b = round(min(255, b * lum))
            out.setColor(ix,iy,(r,g,b))
    return out

def flip(pic = pgt.Picture):


    w,h = getSize(pic)

    out = pgt.Picture(w,h)
    for iy in range(h):
        for ix in range(w):
            r,g,b = pic.getColorRGB(ix,iy)
            out.setColor(w-ix-1,iy,(r,g,b))
    return out
def negative(pic = pgt.Picture):

    w,h = getSize(pic)
    out = pgt.Picture(pic)

    for iy in range(h):
        for ix in range(w):
            r,g,b = pic.getColorRGB(ix,iy)
            r = max(0,255-r)
            g = max(0,255-g)
            b = max(0,255-b)
            out.setColor(ix,iy,(r,g,b))
    return out
def createSimPic(size = (100,100),color = (255,255,255)):

    w,h = size
    pic = pgt.Picture(w,h)
    for iy in range(h):
        for ix in range(w):
            pic.setColor(ix,iy,color)
    return pic
def getSize(pic = pgt.Picture):
    return (pic.getWidth(),pic.getHeight())
# ============================================================================
# ============== Do NOT make any changes below this comment ==================
# ============================================================================


if __name__ == '__main__':

    # first command line argument, if any, is name of image file for output
    # second command line argument, if any, is name of the output html file namezx 
    
    

    collageFile = None
    htmlFileName = "webpage.html"  #Default name

    if len(sys.argv) > 1:
        collageFile = sys.argv[1]
    if len(sys.argv) > 2:
        htmlFileName = sys.argv[2]    

    # temporarily set media path to project directory
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # create the collage
    
    collage = createCollage()
    #collage.display()

    try:
        # either show collage on screen or write it to file
        if collageFile is None:
            collage.display()
            input('Press Enter to quit...')
        else:
            print(f'Saving collage to {collageFile}')
            collage.save(collageFile)
            createWebPage(collageFile, htmlFileName)
    except:
        print('Could not show or save picture')

