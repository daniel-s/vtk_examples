#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk

refresh_rate = 60 # In Hertz

def callback_func(caller, timer_event):
    # We rotate the arrow by 1 degree in the Z direction.
    # This creates a nice counterclockwise motion
    # for the default camera postion/direction.
    # It is possible to speed/slow the motion by changing
    # this value, or the refresh rate.
    actor.RotateZ(1)
    # This needs to be called to render the updated actor
    # orientation.
    window.Render()

# These next few lines are pretty standard.
# Create an arrow, polydata mapper, and actor.
arrow = vtk.vtkArrowSource()
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(arrow.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create the window, renderer, and interactor.
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

# The interactor needs to be initialised before we
# can create a timer or add observers.
interactor.Initialize()
# The repeating timer takes the interval in 1/1000th
# of a second. Each time it fires off a TimerEvent.
interactor.CreateRepeatingTimer(int(1/refresh_rate))

# In python you can add an observer directly like this.
# In other languages there is a layer of indireciton where
# a vtkCallbackCommand is created, and the function is set
# in the vtkCallbackCommand.

# We set the callback function to be called for each
# activation of the timer.
interactor.AddObserver("TimerEvent", callback_func)

# The default position of the camera
# is a little too close to see the entire
# motion of the arrow. Zoom out a litle.
cam = renderer.GetActiveCamera()
cam.SetPosition(0,0,5)
    
window.SetSize(500, 500)
window.Render()
interactor.Start()
