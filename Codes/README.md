# This is the repo for SIH 2018 unconncted villages task

The repo has shape files and their dependencies for Villages and Road Netwroks. 
Apart from these it has a Shape Details.ipynb file that has the initial reading and rendering of the shape files.

## Shape Details.ipynb functions

#### **getVillagePoints(shape-object)** : - 
takes a shape object and returns a list of points (all Villages)

#### **displayPoints(village-points)** : - 
takes a list of village-points and plots them as black dots

#### **getFieldsAndRecords(shape-object)** : - 
returns the fields and records of a corresponding shape object

#### **addRoadPoints(record-index, shapes)** : - 
takes the list of shapes and record index and adds the geometric points of the corresponding shape to the global variable allRoadPoints

#### **plotRoadpoints(all-road-points, village-points)** : - 
takes list of roads' points and villae points and plots them (calls displayPoints to plot villages)

#### **showRoadDetails(road-fields, road-records, road-shapes)** : - 
runs through all the records in roads, then iterates through all fields for each record and displays them. Also it adds the road-type for each road to a global variable allRoadTypes (calls addRoadPoints)

#### **findDistances(village-points)** : - 
takes the village points and computes the distance of each village from every point on every road and returns a dictionary with villages as keys

#### **findClosestn(road-shapes,  dictionary-village-distances, road-records, n=5)** : -
takes the road shapes, the dictionary created in findDistances() and road records and returns a list of list containing the indices of the closest 5 roads to each village

#### **plotClosestn(road-shapes, village-minimums, village-points)** : -
takes the road shapes, village points and closest n roads indices found from findClosestn() and plots them

#### **plotIntersections()** : - 
finds the intersections of roads and plots them on the map