#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk

# The cylinder and the transformation that will be performed on it.
cylinder = vtk.vtkCylinderSource()
transform = vtk.vtkTransform()

# Setup the transform here.
# We just set one rotation around the x-axis, but the
# transform can be anything.
transform.RotateX(45)

# Here we calculate the normals for all surfaces in the cylinder.
norms_before = vtk.vtkPolyDataNormals()
norms_before.ComputeCellNormalsOn()
norms_before.SetInputConnection(cylinder.GetOutputPort())
# This actually forces the calculations to happen. Is important
# to call before the next line when we actually read that data.
norms_before.Update()

# It happens that tuple with index 6 is the correct one for the *default*
# cylinder. If you change the cylinder source (increase resolution or something)
# it may require finding the correct index again. THIS IS AN UGLY HACK.
orientation_before = norms_before.GetOutput().GetCellData().GetNormals().GetTuple(6)
print(orientation_before)
# The default orientation is going to be (0, 1, 0) before transformations.

# Apply the transformation.
trans_filter = vtk.vtkTransformFilter()
trans_filter.SetTransform(transform)
trans_filter.SetInputConnection(cylinder.GetOutputPort())

norms_after = vtk.vtkPolyDataNormals()
norms_after.ComputeCellNormalsOn()
norms_after.SetInputConnection(trans_filter.GetOutputPort())
norms_after.Update()

orientation_after = norms_after.GetOutput().GetCellData().GetNormals().GetTuple(6)
# We expect to get a vector of (0, 0, 1) for a 90 degree rotation around
# the x-axis.
print(orientation_after)
