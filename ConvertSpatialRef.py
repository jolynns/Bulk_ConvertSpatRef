#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      jolynn
#
# Created:     15/09/2016
# Copyright:   (c) jolynn 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    # import arcpy
    import arcpy
    import sys
    arcpy.env.overwriteOutput = True

# Get input
    # Get the directory where the files are
    workingDir = arcpy.GetParameterAsText(0)

    # Get the name of file to define spatial reference
    defineSRF = arcpy.GetParameterAsText(1)


# Make some functions
    # write a function to get spatial reference from a file
    def getSR(targetSRF):
        try:
            desc = arcpy.Describe(targetSRF)
            spatialRef = desc.spatialReference
            return spatialRef
        except:
            arcpy.AddError("Unable to get Spatial Reference: skipping")
            arcpy.AddMessage(arcpy.GetMessages())

    # write a function to rename a file
    def renameFile(fullName):
        try:
            import os.path
            fName, extension = os.path.splitext(fullName)
            return fName + "_projected" + extension
        except:
            arcpy.AddError("Unable to rename file %s" % fullName)
            arcpy.AddMessage(arcpy.GetMessages())

# define global variables
    # get spatial ref of target file to use as spatial reference input
    try:
        targetSR = getSR(defineSRF)
    except:
        arcpy.AddError("Error getting Spatial Reference from %s" % defineSRF)
        arcpy.AddMessage(arcpy.GetMessages())
        # exit because if we don't have the SR then the rest doesn't matter
        sys.exit(1)

    #set the workspace
    try:
        arcpy.env.workspace = workingDir
    except:
        arcpy.AddError("Please confirm path and that forward slashes are used")
        arcpy.AddMessage(arcpy.GetMessages())
        print arcpy.GetMessags()

    # Initialize an empty list to hold reprojected files
    reprojectedFiles = []

# Process files
    # List all feature classes in current working directory and loop over them
    fcList = arcpy.ListFeatureClasses()
    for featureClass in fcList:
        # Get spatial reference for current featureClass and convert if needed
        currentSR = getSR(featureClass)
        if currentSR.name != targetSR.name:
            try:
                outputFC = renameFile(featureClass)
                arcpy.Project_management(featureClass, outputFC, targetSR)
                reprojectedFiles.append(featureClass)
            except:
                arcpy.AddError("Unable to convert Spatial Reference for %s" % featureClass)
                arcpy.AddMessage(arcpy.GetMessages())
        else:
            pass
##            print str(currentSR.name) + " is equal to " + str(targetSR.name)

# finished with our loop, lets print the results
    listProjected = ', '.join(reprojectedFiles)
    arcpy.AddMessage("Files converterd: %s" % listProjected)
##    print "file converted:", listProjected


if __name__ == '__main__':
    main()
