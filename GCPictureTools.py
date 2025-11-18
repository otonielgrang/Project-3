"""
File Name: GCPictureTools.py
Date: 2024-08-01
Description: provide functions to work with pictures based on pygame package

Improvement Log
2024-10-3: add display method to show the picture until user closes the window.
2024-10-27: add Pixel class; add save method in Picture class to save image into a file
2025-07-24: minor typo fixes, update on Github, add Makefile
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "yes"
import pygame as pg
from pygame import Color

# Predefined colors

black   = Color(  0,  0,  0)
red     = Color(255,  0,  0)
green   = Color(  0,255,  0)
blue    = Color(  0,  0,255)
cyan    = Color(  0,255,255)
magenta = Color(255,  0,255)
yellow  = Color(255,255,  0)
white   = Color(255,255,255)


def demo():
  """
  Demo the basic usage of these tools.
  Display 4 different graphic images
  Hit enter key to change to the next, and to exit
  """
  canvas = Picture(500, 500, "light yellow")
  canvas.show()
  input("Press Enter")
  for x in range(0, canvas.getWidth(), 20):
    for y in range(0, canvas.getHeight(), 30):
      canvas.addRectFilled(10, 15, x, y, "light blue")
  canvas.repaint()
  input("Press Enter")
  for x in range(0, canvas.getWidth(), 30):
    for y in range(0, canvas.getHeight(), 30):
      canvas.addLine("green", x, y, y, x, 2)
  canvas.repaint()
  input("Press Enter")
  for x in range(0, canvas.getWidth(), 35):
    for y in range(0, canvas.getHeight(), 35):
      canvas.addOval(30, 20, x, y, "red")
  canvas.repaint()
  input("Press Enter")

def makeLighter(color:pg.Color, f:float=1.15):
  """
  Sample function to make given picture lighter
  Shade up by 1.15, but don't go over 255 for each value
  """
  r = min(255, color.r*f)
  g = min(255, color.g*f)
  b = min(255, color.b*f)
  return pg.Color((r, g, b))



#boolean for if changes should update automatically or not
class autoUpdate():
  autoUpdateBool = False

  def __init__(self):
    """
    Initializer function
    """
    autoUpdateBool = False

  def getAutoUpdate(self):
    """
    Getter
    """
    return self.autoUpdateBool
  
  def setAutoUpdate(self, status):
     """
     Setter
     """
     self.autoUpdateBool = status

class Picture:
  window = None
  image = None
  size = None
  title = ''
  magnification = 1
  autoUpdate = autoUpdate()

  def __init__(self, *args, **kwargs):
      """
      Initializer

      Args:
        If none, then make picture with default size (100 x 100)
          and color (white)
        If one string parameter - filename or path to a file
          then make a picture made from this file
        If one image parameter - pre-existing image to clone
          make a copy of the input picture
        If two integer parameters - assume these are width and height
          make a picture with given size and default color (white)
        If third parameter - a color as string (default: "white")

      Returns:
        Nothing
      """
      size = (100, 100)
      if len(args) == 0:
          # no parameters, make screen with default size and color
          num_bytes = 3 * size[0] * size[1]
          self.size = size
          self.image = pg.image.frombytes(bytes([0]*num_bytes), size, 'RGB')
          self.image.fill("white")
      elif len(args) == 1:
          if isinstance(args[0], str):
              # one string parameter - filename or path to a file
              self.image = pg.image.load(args[0])
              self.size = self.image.get_size()
              self.title = args[0]
          elif isinstance(args[0], Picture):
              # one image parameter - pre-existing image to clone
              self.image = args[0].image.copy()
              self.size = args[0].size
              self.title = args[0].title
              self.magnification = args[0].magnification
      elif (len(args) == 2 and \
          isinstance(args[0], int) and isinstance(args[1], int)) or \
            len(args) == 3:
          # two integer parameters - assume these are width and height
          # third parameter is a color
          c = pg.Color(255, 255, 255) if len(args) == 2 else args[2]
          w, h = int(args[0]), int(args[1])
          num_bytes = 3 * w * h
          self.size = (w, h)
          self.image = pg.image.frombytes(bytes([0]*num_bytes), \
                                          self.size, 'RGB')
          self.image.fill(c)
      else:
          print("Unable to create image")
  
  def show(self, title=None):
    """
    Shows the given image

    Args:
      title (string) - title of the image

    Returns:
      Nothing
    """
    if title is not None:
      self.title = title
    mag_image, mag_size = self.magnify()
    self.window = pg.display.set_mode(mag_size)
    self.window.blit(mag_image, (0, 0))
    pg.display.set_caption(self.title)
    pg.display.update()
    pg.event.pump()

  def display(self, title=None):
    """
    Display the given image until user close the window

    Args:
      title (string) - title of the image

    Returns:
      Nothing
    """
    if title is not None:
      self.title = title
    mag_image, mag_size = self.magnify()
    self.window = pg.display.set_mode(mag_size)
    self.window.blit(mag_image, (0, 0))
    pg.display.set_caption(self.title)

    # paint screen one time
    pg.display.flip()
    status = True
    while (status):
      # iterate over the list of Event objects
      # that was returned by pygame.event.get() method.
      for i in pg.event.get():
          # if event object type is QUIT
          # then quitting the display
          if i.type == pg.QUIT:
              status = False

  def magnify(self, title=None):
    """
    Magnifies a given image

    Args:
      None

    Returns:
      Nothing
    """
    orig_size = self.image.get_size()
    mag_size = (orig_size[0] * self.magnification,
                orig_size[1] * self.magnification)
    mag_image = pg.transform.scale(self.image, mag_size)
    return mag_image, mag_size

  def repaint(self):
    """
    Updates an image
    """
    if (os.name=="nt"):
      self.show()
    mag_image, mag_size = self.magnify()
    self.window.blit(mag_image, (0, 0))
    pg.display.flip()
    pg.event.pump()
  
  def close(self):
    """
    Closes image
    """
    pg.quit()

  def copyInto(self, dest, x, y):
    """
    Copies a given image onto another image

    Args:
      dest (Picture) - picture where the image is to be copied
      x (int) - x position of the image
      y (int) - y position of the image

    Returns:
      nothing
    """
    img = self.image
    dest.image.blit(img, (x, y))
    if self.autoUpdate.autoUpdateBool:
      pg.display.update()

  def save(self, filename):
    """
    save this image into a file

    Args:
      filename - the name of the file where the image is to be saved

    Returns:
      nothing
    """
    pg.image.save(self.image, filename)


  def getAllLocations(self):
    """
    Returns a list of coordinates of all the pixels in a picture
    (moving up to down, left to right)
    """
    newList = []
    for x in range(self.getWidth()):
      for y in range(self.getHeight()):
        newList.append((x, y))
    return newList

  def getPixels(self):
    """
    Returns a list with all the pixels in a picture
    (moving up to down, left to right)
    """
    newList = []
    for x in range(self.getWidth()):
      for y in range(self.getHeight()):
        newList.append(Pixel(self, x, y))
    return newList

  def getPixel(self, x, y):
    """
    Returns the pixel at (x, y) in a picture
    """
    return Pixel(self, x, y)

  def getMagnification(self):
    """
    Returns the magnification of an image
    """
    return self.magnification
  
  def setMagnification(self, magnification):
    """
    Sets the magnification for an image

    Args:
      magnification (int, float) - magnification to be set

    Returns:
      Nothing
    """
    self.magnification = magnification
  
  def getWidth(self):
    """
    Returns the width of an image
    """
    return self.image.get_width()
    
  def getHeight(self):
    """
    Returns the height of an image
    """  
    return self.image.get_height()
  
  def getColor(self, x, y):
    """
    Gets the color (RGBA) of a pixel  
    
    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
    
    Returns:
      color of the pixel
    """ 
    return pg.Color(self.image.get_at((x, y))[0:3])
  
  def getColorRGB(self, x, y):
    """
    Gets the RGB values of the color of a pixel
    
    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
    
    Returns:
      the R, G, B values of the color of the pixel
    """ 
    return self.image.get_at((x, y))[0:3]
  
  def setColor(self, x, y, color):
    """
    Sets the color of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
      color (Color) - the color the pixel will be set

    Returns:
      Nothing
     """
    self.image.set_at((x,y), color)
    if self.autoUpdate.autoUpdateBool:
      pg.display.update()

  def getRed(self, x, y):
    """
    Returns the red value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel

    Returns:
      value of red
    """
    c = pg.Color(self.getColor(x, y))
    return c.r
  
  def getGreen(self, x, y):
    """
    Returns the green value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel

    Returns:
      value of green
    """
    c = pg.Color(self.getColor(x, y))
    return c.g
  
  def getBlue(self, x, y):
    """
    Returns the blue value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel

    Returns:
      value of blue
    """
    c = pg.Color(self.getColor(x, y))
    return c.b
  
  def setRed(self, x, y, red):
    """
    Sets the red value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
      red (int) - the red value to be set

    Returns:
      Nothing    
    """
    color = self.getColor(x,y)
    r = red
    g = color.g
    b = color.b
    self.image.set_at((x,y), (r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def setGreen(self, x, y, green):
    """
    Sets the green value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
      green (int) - the green value to be set

    Returns:
      Nothing    
    """
    color = self.getColor(x,y)
    r = color.r
    g = green
    b = color.b
    self.image.set_at((x,y), (r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def setBlue(self, x, y, blue):
    """
    Sets the blue value of a pixel

    Args:
      x (int) - the x position of the pixel
      y (int) - the y position of the pixel
      blue (int) - the blue value to be set

    Returns:
      Nothing    
    """
    color = self.getColor(x,y)
    r = color.r
    g = color.g
    b = blue
    self.image.set_at((x,y), (r, g, b))
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()
  
  def addLine(self, acolor, x1, y1, x2, y2, width=1):
    """
    Draws a line onto a given surface

    Args:
      acolor (Color) - color of the line
      x1 (int) - beginning x position of the line
      y1 (int) - beginning y position of the line
      x2 (int) - ending x position of the line
      y2 (int) - ending y position of the line
      width (int) - thickness of the line

    Returns:
      Nothing
    """
    img = self.image
    pg.draw.line(img, acolor, (x1, y1), (x2, y2), width)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addRectFilled(self, width, height, x, y, acolor="red"):
    """
    Draws a filled rectangle onto a given surface

    Args:
      width (int) - width of the rectangle (in pixels)
      height (int) - height of the rectangle (in pixels)
      x (int) - the x position of the top left corner of the rectangle
      y (int) - the y position of the top left corner of the rectangle
      acolor (Color, int, str, tuple) - the color of the rectangle

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.rect(img, acolor, newRect)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addRect(self, width, height, x, y, acolor="red", linew=1):
    """
    Draws a rectangle onto a given surface
    
    Args:
      width (int) - width of the rectangle (in pixels)
      height (int) - height of the rectangle (in pixels)
      x (int) - the x position of the top left corner of the rectangle
      y (int) - the y position of the top left corner of the rectangle
      acolor (Color, int, str, tuple) - the color of the rectangle
      linew (int) - width of the outline of the rectangle

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.rect(img, acolor, newRect, linew)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addOvalFilled(self, width, height, x, y, acolor="red"):
    """
    Draws a filled oval onto a given surface

    Args:
      width (int) - width of the oval (in pixels)
      height (int) - height of the oval (in pixels)
      x (int) - the x position of the oval
      y (int) - the y position of the oval
      acolor (Color, int, str, tuple) - the color of the oval

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.ellipse(img, acolor, newRect)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()

  def addOval(self, width, height, x, y, acolor="red", linew=1):
    """
    Draws an oval onto a given surface

    Args:
      width (int) - width of the oval (in pixels)
      height (int) - height of the oval (in pixels)
      x (int) - the x position of the oval
      y (int) - the y position of the oval
      acolor (Color, int, str, tuple) - the color of the oval
      linew (int) - width of the outline of the oval

    Returns:
      Nothing
    """
    newRect = pg.Rect((x,y), (width, height))
    img = self.image
    pg.draw.ellipse(img, acolor, newRect, linew)
    if self.autoUpdate.autoUpdateBool:
      pg.display.flip()
     
class Pixel:

  def __init__(self, picture, x, y):
      """
      Initializer

      Args:
        picture: picture that contains this pixel
        x: column index
        y: row index

      Returns:
        a pixel instance at (x, y) in picture
      """
      self.pic = picture
      self.x = x
      self.y = y

  def getX(self):
    """
    Gets the column index (x) of the pixel

    Args:
      none

    Returns:
      column index (nonnegative integer)
    """
    return self.x

  def getY(self):
    """
    Gets the row index (y) of the pixel

    Args:
      none

    Returns:
      row index (nonnegative integer)
    """
    return self.y

  def getPicture(self):
    """
    Gets the picture the pixel is part of

    Args:
      none

    Returns:
      the Picture object of the pixel
    """
    return self.pic

  def getColor(self):
    """
    Gets the color (RGBA) of the pixel

    Args:
      none

    Returns:
      color of the pixel
    """
    return self.pic.getColor(self.x, self.y)
  
  def getColorRGB(self):
    """
    Gets the RGB values of the color of the pixel

    Args:
      none

    Returns:
      the R, G, B values of the color of this pixel
    """
    return self.pic.getColorRGB(self.x, self.y)

  def setColor(self, color):
    """
    Sets the color of the pixel

    Args:
      color (Color) - the color the pixel will be set

    Returns:
      Nothing
     """
    self.pic.setColor(self.x, self.y, color)

  def getRed(self):
    """
    Returns the red value of the pixel

    Args:
      none

    Returns:
      value of red
    """
    return self.pic.getRed(self.x, self.y)

  def setRed(self, red):
    """
    Sets the red value of the pixel

    Args:
      red (int) - the red value to be set

    Returns:
      Nothing
    """
    self.pic.setRed(self.x, self.y, red)

  def getGreen(self):
    """
    Returns the green value of the pixel

    Args:
      none

    Returns:
      value of green
    """
    return self.pic.getGreen(self.x, self.y)

  def setGreen(self, green):
    """
    Sets the green value of the pixel

    Args:
      green (int) - the green value to be set

    Returns:
      Nothing
    """
    self.pic.setGreen(self.x, self.y, green)

  def getBlue(self):
    """
    Returns the blue value of the pixel

    Args:
      none

    Returns:
      value of blue
    """
    return self.pic.getBlue(self.x, self.y)

  def setBlue(self, blue):
    """
    Sets the blue value of the pixel

    Args:
      blue (int) - the blue value to be set

    Returns:
      Nothing
    """
    self.pic.setBlue(self.x, self.y, blue)



if __name__ == "__main__":

  demo()
