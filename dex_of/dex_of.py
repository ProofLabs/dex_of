# DexOF - DEXter openfoam interface.
# Stevens Institute of Technology
# Pitz & Pochiraju
# December 13 - 2021
# Release 0.1
#
import numpy as np
from stl import mesh
import math
import sys
import os
import json
import kajiki

def parse_args_any(args):
    pos = []
    named = {}
    key = None
    for arg in args:
        if key:
            if arg.startswith('--'):
                named[key] = True
                key = arg[2:]
            else:
                named[key] = arg
                key = None
        elif arg.startswith('--'):
            key = arg[2:]
        else:
            pos.append(arg)
    if key:
        named[key] = True
    return (pos, named)

def dex2dict(filename):
    # lame version of dex parser to extract what's needed
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    dexdict = {}
    for line in lines:
        if not line.startswith('*'):
            words = line.split(',')
            dexdict[words[0]]=words[-1]
    return dexdict

def find_mins_maxs(obj):
    minx = obj.x.min()
    maxx = obj.x.max()
    miny = obj.y.min()
    maxy = obj.y.max()
    minz = obj.z.min()
    maxz = obj.z.max()
    return minx, maxx, miny, maxy, minz, maxz

def translate(_solid, xt, yt, zt):
    xitems = 0, 3, 6
    yitems = 1, 4, 7
    zitems = 2, 5, 8
    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, xitems] += xt
    _solid.points[:, yitems] += yt
    _solid.points[:, zitems] += zt

def scale(_solid, xs, ys, zs):
    xitems = 0, 3, 6
    yitems = 1, 4, 7
    zitems = 2, 5, 8
    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, xitems] *= xs
    _solid.points[:, yitems] *= ys
    _solid.points[:, zitems] *= zs

# Arg1 is the original file, arg 2 is the AOA, Arg 3 is the final file

def stlPrep(configdict):
#    print("usage python stlPrep.py orig.stl aoa_degrees final.stl ")
    infile = configdict['infile']
    aoa = float(configdict['aoa'])
    outfile = configdict['outfile']
    scalex = float(configdict['scalex'])
    scaley = float(configdict['scaley'])
    scalez = float(configdict['scalez'])

    your_mesh = mesh.Mesh.from_file(infile)

    volume, cog, inertia = your_mesh.get_mass_properties()
    # print("Volume                                  = {0}".format(volume))
    # print("Position of the center of gravity (COG) = {0}".format(cog))
    # print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    # print("                                          {0}".format(inertia[1,:]))
    # print("                                          {0}".format(inertia[2,:]))
    # print("Bounding Box")
    # print (find_mins_maxs(your_mesh))

    translate(your_mesh,-cog[0],-cog[1],-cog[2])
    scale(your_mesh,scalex,scaley,scalez)
    your_mesh.rotate([0,0,1],math.radians(float(aoa)))

    volume, cog, inertia = your_mesh.get_mass_properties()
    # print("Volume                                  = {0}".format(volume))
    # print("Position of the center of gravity (COG) = {0}".format(cog))
    # print("Inertia matrix at expressed at the COG  = {0}".format(inertia[0,:]))
    # print("                                          {0}".format(inertia[1,:]))
    # print("                                          {0}".format(inertia[2,:]))
    # print("Bounding Box")
    # print (find_mins_maxs(your_mesh))
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(your_mesh)
    bbox = [minx,maxx,miny,maxy,minz,maxz]

    lref = maxx-minx

    # Use PAREA TO get the projections  parea -

    your_mesh.save("temp.stl")
    #
    # parea needs ascii stl - mesh.save() produces binary!
    # boo! convert it to ascci and give it to parea
    # stl2ascii --> apt-get install numpy-stl (not pip install)
    #
    cmd = "stl2ascii temp.stl " + outfile
    os.system(cmd)
    cmd = "parea -yz -stl " + outfile
    outpa = os.popen(cmd).read()
    #print("Lref Aref")
    #print(lref)
    aref = float(outpa.split(":")[1])
    # print("lref = %s" % lref)
    # print("Aref = %s" % float(aref))
    # print("**done**")
    return {'outfile':outfile,'lref': lref, 'aref': aref,'volume':volume,
        'cog':cog,'inertia':inertia,'boundingbox':bbox}

def kajiki_it(templfile,outfile,problemdict):
    with open(templfile) as templ:
        data=templ.read()
    Template = kajiki.TextTemplate(data)
    outlines = Template(problemdict).render()
    with open(outfile,'w') as outfile:
        outfile.write(outlines)
    return outlines

def computational_domain(problemdict):
    bb = problemdict['boundingbox']
    xlength = bb[1]-bb[0]
    ylength = bb[3]-bb[2]
    zlength = bb[5]-bb[4]
    #
    DomainSizeXFront = float(problemdict['DomainSizeXFront'])
    DomainSizeXBack = float(problemdict['DomainSizeXBack'])
    xmin = -xlength*DomainSizeXFront
    xmax = xlength*DomainSizeXBack
    #
    DomainSizeYTop= float(problemdict['DomainSizeYTop'])
    DomainSizeYBot = float(problemdict['DomainSizeYBot'])
    ymin = -ylength*DomainSizeYTop
    ymax = ylength*DomainSizeYBot
    #
    DomainSizeZLeft = float(problemdict['DomainSizeZLeft'])
    DomainSizeZRight = float(problemdict['DomainSizeZRight'])
    zmin = -zlength*DomainSizeZLeft
    zmax = zlength*DomainSizeZRight
    # set up domain grid
    nxgrid = int((xmax-xmin)/float(problemdict['cellSizeX']))
    nygrid = int((ymax-ymin)/float(problemdict['cellSizeY']))
    nzgrid = int((zmax-zmin)/float(problemdict['cellSizeZ']))
    #
    xlocinside = xmax - 0.01*(xmax-xmin)
    ylocinside = ymax - 0.01*(ymax-ymin)
    zlocinside = zmax - 0.01*(zmax-zmin)

    return {'xmin':xmin, 'xmax':xmax,
            'ymin':ymin,'ymax':ymax,'zmin':zmin,'zmax':zmax,
            'nxgrid':nxgrid,'nygrid':nygrid,'nzgrid':nzgrid,
            'xlocinside':xlocinside,'ylocinside':ylocinside,'zlocinside':zlocinside}


# Run stl2ascii on this.
def setup_of(problemdict):
    # check if casefolder exists if not create it.
    casefolder = problemdict['current_dir']+"/OF_default_casefolder"
    if 'casefoldername' in problemdict:
        casefolder = problemdict['current_dir']+"/"+problemdict['casefoldername']
    if not os.path.exists(casefolder):
        os.makedirs(casefolder)
    else:
        print("Warning: Casefolder already exists, files will be overwritten")

    # create files that need to be templated
    ofcopycmd  = 'cp -r ' + problemdict['dexof_path']+"/ofTemplate/* " + casefolder
    print("Copying::",ofcopycmd)
    #os.system('cp -r ofTemplate/* '+ casefolder)
    os.system(ofcopycmd)
    # move stl file into the casefolder
    outfile = problemdict['current_dir']+"/"+problemdict['outfile']
    stlmovecmd = 'cp '+outfile+' ' + casefolder+'/constant/triSurface/UUV.stl'
    os.system(stlmovecmd)
    # First copy the STL File in the right place
    templatesdict={'0.orig/k_templ.txt':'0.orig/k','0.orig/omega_templ.txt':'0.orig/omega','0.orig/U_templ.txt':'0.orig/U',
    'system/blockMeshDict_templ.txt': 'system/blockMeshDict','system/decomposeParDict.6_templ.txt': 'system/decomposeParDict.6',
    'system/snappyHexMeshDict_templ.txt':'system/snappyHexMeshDict',
    'system/forceCoeffs_templ.txt':'system/forceCoeffs','system/fvSolution_templ.txt':'system/fvSolution',
                   'system/controlDict_templ.txt':'system/controlDict', 'system/forceCoeffs_templ.txt':'system/forceCoeffs',
                   'constant/transportProperties_templ.txt':'constant/transportProperties'}
    for key in templatesdict:
        kajiki_it(casefolder+"/"+key,casefolder+"/"+templatesdict[key],problemdict)
    # write input definition json into the casefolder
    with open(casefolder+"/problem_def.json", "w") as outfile:
        keys_values = problemdict.items()
        new_d = {str(key): str(value) for key, value in keys_values}
        json.dump(new_d, outfile,indent=4)
    print("Case folder (%s) has been created " % casefolder)
    print("Problem definition %s/problem_def.json is written into the case folder"%casefolder)

# Use command line arguments e.g --aoa  5 to overide values in dex file --casefile
#out = stlPrep(sys.argv[1],sys.argv[2],sys.argv[3])
#print(out)

pos,named = parse_args_any(sys.argv)

if (len(pos) != 2 ):
    print("Usage: python dex_of <config.dex> --infile foo.stl")
    exit()
print ("Dex_of called with arguments:")
print(f" Positional Arguments: {pos}")
print(f" Named Arguments: {named}")

dexof_path = os.path.dirname(os.path.realpath(__file__))
print("Path: ",dexof_path)
current_dir = os.path.abspath(os.getcwd())

# dex file is postional 0
configdict = dex2dict(pos[1])
configdict['dexof_path'] = dexof_path
configdict['current_dir']= current_dir
# overwrite named named arguments from dict -ignore new arguments
if (len(pos) != 2):
    print("First positional argument is needed.\n Program looks for a .dex file")
    exit()

if len(named) != 0 :
    for key in named:
        if key in configdict:
            configdict[key]=named[key]
            print("Updated valued for %s given in dex file with command line" % key)

problemdict = stlPrep(configdict)
problemdict.update(configdict)
problemdict.update(computational_domain(problemdict))
setup_of(problemdict)
print("**** ALL DONE ****")
# do the overwrite.