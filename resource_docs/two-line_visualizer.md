**Two-Line Visualizer**



*​	This is useful for plotting any Two-Line elements of satellite data and especially KickSat-2 data!*

- [ ] ​	TODO: add example of KickSat-2 Two-Line elements. 



Example Data: <http://celestrak.com/NORAD/archives/>

Data spec: <http://en.wikipedia.org/wiki/Two-line_element_set>

Vis tool: <http://www.paraview.org/>

Python examples: <http://www.vtk.org/Wiki/VTK/Examples/Python>

If you have ubuntu, do:

```
sudo apt-get install paraview
sudo apt-get install python-vtk
```

Then loop through the data like:

```
with open('met2-17.txt') as fh:
  for line in fh.readlines():
    words = line.split()
```

do whatever math you need to build your points and data lists, and then create the vtkpolydata file with some points and data:

```
import vtk

points = vtk.vtkPoints()

scalars = vtk.vtkDoubleArray()
scalars.SetName("scalars")
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(num_points)

vectors = vtk.vtkDoubleArray()
vectors.SetName("vectors")
vectors.SetNumberOfComponents(3)
vectors.SetNumberOfTuples(num_points)

for i in range(num_points):
    x,y,z = my_point_coords_list[i]
    points.InsertNextPoint((x,y,z))
    vectors.SetTuple3(i, *my_vectors[i])
    scalars.SetTuple1(i, my_scalars[i])

polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.GetPointData().SetScalars(scalars)
polydata.GetPointData().SetVectors(vectors)

writer = vtk.vtkXMLPolyDataWriter()
writer.SetInput(polydata)
writer.SetFileName('out.vtp')
writer.Write()
```



When you visualize in paraview you can use the glyph filter and set the properties based on the scalars and vectors arrays.



You should get something like this:*

- [ ] ​	TODO: add image.