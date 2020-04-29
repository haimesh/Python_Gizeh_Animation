from tkinter import *
from tkinter.ttk import *
import numpy as np
import gizeh as gz
import moviepy.editor as mpy
import pyglet

DURATION = 2.0

def animation1(t):

    W,H = 480,480
    ncircles = 20

    surface = gz.Surface(W,H)

    for i in range(ncircles):
        angle = 2*np.pi*(1.0*i/ncircles+t/DURATION)
        center = W*( 0.5+ gz.polar2cart(0.1,angle))
        circle = gz.circle(r= W*(1.0-1.0*i/ncircles),
                              xy= center, fill= (i%2,i%2,i%2))
        circle.draw(surface)

    return surface.get_npimage()

def animation2(t):

    W = H = 480
    nballs=60

    radii = np.random.randint(.1*W,.2*W, nballs)
    colors = np.random.rand(nballs,3)
    centers = np.random.randint(0,W, (nballs,2))

    surface = gz.Surface(W,H)
    for r,color, center in zip(radii, colors, centers):
        angle = 2*np.pi*(t/DURATION*np.sign(color[0]-.5)+color[1])
        xy = center+gz.polar2cart(W/5,angle)
        gradient = gz.ColorGradient(type="radial",
                     stops_colors = [(0,color),(1,color/10)],
                     xy1=[0.3,-0.3], xy2=[0,0], xy3 = [0,1.4])
        ball = gz.circle(r=1, fill=gradient).scale(r).translate(xy)
        ball.draw(surface)
    return surface.get_npimage()

def animation3(t):

    W = H = 480
    NDISKS_PER_CYCLE = 8
    SPEED = .05
    dt = 1.0*DURATION/2/NDISKS_PER_CYCLE # delay between disks
    N = int(NDISKS_PER_CYCLE/SPEED) # total number of disks
    t0 = 1.0/SPEED # indicates at which avancement to start

    surface = gz.Surface(W,H)
    for i in range(1,N):
        a = (np.pi/NDISKS_PER_CYCLE)*(N-i-1)
        r = np.maximum(0, .05*(t+t0-dt*(N-i-1)))
        center = W*(0.5+ gz.polar2cart(r,a))
        color = 3*((1.0*i/NDISKS_PER_CYCLE) % 1.0,)
        circle = gz.circle(r=0.3*W, xy = center,fill = color,
                              stroke_width=0.01*W)
        circle.draw(surface)
    contour1 = gz.circle(r=.65*W,xy=[W/2,W/2], stroke_width=.5*W)
    contour2 = gz.circle(r=.42*W,xy=[W/2,W/2], stroke_width=.02*W,
                            stroke=(1,1,1))
    contour1.draw(surface)
    contour2.draw(surface)
    return surface.get_npimage()

def animation4(t):

    W = H = 480
    WSQ = W/4 
    a = np.pi/8 
    points = [(0,0),(1,0),(1-np.cos(a)**2,np.sin(2*a)/2),(0,0)]
    surface = gz.Surface(W,H)
    for k, (c1,c2) in enumerate([[(.7,0.05,0.05),(1,0.5,0.5)],
                                [(0.05,0.05,.7),(0.5,0.5,1)]]):

        grad = gz.ColorGradient("linear",xy1=(0,0), xy2 = (1,0),
                               stops_colors= [(0,c1),(1,c2)])
        r = min(np.pi/2,max(0,np.pi*(t-DURATION/3)/DURATION))
        triangle = gz.polyline(points,xy=(-0.5,0.5), fill=grad,
                        angle=r, stroke=(1,1,1), stroke_width=.02)
        square = gz.Group([triangle.rotate(i*np.pi/2)
                              for i in range(4)])
        squares = (gz.Group([square.translate((2*i+j+k,j))
                            for i in range(-3,4)
                            for j in range(-3,4)])
                   .scale(WSQ)
                   .translate((W/2-WSQ*t/DURATION,H/2)))

        squares.draw(surface)

    return surface.get_npimage()




def generateAnimation(animation_type):

    if animation_type == 1:
        clip = mpy.VideoClip(animation1, duration=DURATION)
    elif animation_type == 2:
        clip = mpy.VideoClip(animation2, duration=DURATION)
    elif animation_type == 3:
        clip = mpy.VideoClip(animation3, duration=DURATION)
    elif animation_type == 4:
        clip = mpy.VideoClip(animation4, duration=DURATION)

    clip.write_videofile("anim.mp4",fps=15)

    window= pyglet.window.Window(480, 480, "ANIMATION")
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load('anim.mp4')
    
    player.queue(MediaLoad)
    player.play()
    
    
    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(0,0)

    pyglet.app.run()



window = Tk()

window.title("170423107002 - Python OEP")

window.geometry("550x550")

Label(window,text = "Python Programming(2180711) OEP", foreground = "red",font =('Verdana', 20)).pack()

ani1_thumbnil = PhotoImage(file = r"ani1_thumbnil.PNG").subsample(2, 2) 

ani2_thumbnil = PhotoImage(file = r"ani2_thumbnil.PNG").subsample(2, 2) 

ani3_thumbnil = PhotoImage(file = r"ani3_thumbnil.PNG").subsample(2, 2) 

ani4_thumbnil = PhotoImage(file = r"ani4_thumbnil.PNG").subsample(2, 2) 

btn1 = Button(window,text =  "Animation 1", image= ani1_thumbnil, compound = LEFT , command = lambda:generateAnimation(1))

btn2 = Button(window,text =  "Animation 2", image= ani2_thumbnil, compound = LEFT, command = lambda:generateAnimation(2))

btn3 = Button(window,text =  "Animation 3", image= ani3_thumbnil, compound = LEFT, command =  lambda:generateAnimation(3))

btn4 = Button(window,text =  "Animation 4", image= ani4_thumbnil, compound = LEFT, command =  lambda:generateAnimation(4))

btn1.pack(pady=10)
btn2.pack(pady=10)
btn3.pack(pady=10)
btn4.pack(pady=10)

window.mainloop()