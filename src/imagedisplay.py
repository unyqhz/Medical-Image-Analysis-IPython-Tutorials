import matplotlib.pyplot as plt
from matplotlib import gridspec
import SimpleITK as sitk
    
def myshow(img, title=None, margin=0.05, dpi=80, usespacing=True ):
    nda = sitk.GetArrayFromImage(img)
    
    if usespacing:
      spacing = img.GetSpacing()
    else:
      spacing = [1,1]
      
    if nda.ndim == 3:
        # fastest dim, either component or x
        c = nda.shape[-1]
        
        # the the number of components is 3 or 4 consider it an RGB image
        if not c in (3,4):
            nda = nda[nda.shape[0]//2,:,:]
    
    elif nda.ndim == 4:
        c = nda.shape[-1]
        
        if not c in (3,4):
            raise Runtime("Unable to show 3D-vector Image")
            
        # take a z-slice
        nda = nda[nda.shape[0]//2,:,:,:]
            
    ysize = nda.shape[0]
    xsize = nda.shape[1]
   
    
    # Make a figure big enough to accomodate an axis of xpixels by ypixels
    # as well as the ticklabels, etc...
    figsize = (1 + margin) * ysize / dpi, (1 + margin) * xsize / dpi

    fig = plt.figure(figsize=figsize, dpi=dpi)
    # Make the axis the right size...
    ax = fig.add_axes([margin, margin, 1 - 2*margin, 1 - 2*margin])
    
    extent = (0, xsize*spacing[0], ysize*spacing[1], 0)
    
    t = ax.imshow(nda,extent=extent,interpolation=None)
    
    if nda.ndim == 2:
        t.set_cmap("gray")
    
    if(title):
        plt.title(title)
        
        
def myshow3d(img, xslices=[], yslices=[], zslices=[], title=None, margin=0.05, dpi=80):
    size = img.GetSize()
    img_xslices = [img[s,:,:] for s in xslices]
    img_yslices = [img[:,s,:] for s in yslices]
    img_zslices = [img[:,:,s] for s in zslices]
  
    maxlen = max(len(img_xslices), len(img_yslices), len(img_zslices))
  
      
    img_null = sitk.Image([0,0], img.GetPixelIDValue(), img.GetNumberOfComponentsPerPixel())
  
    img_slices = []
    d = 0
  
    if len(img_xslices):
	img_slices += img_xslices + [img_null]*(maxlen-len(img_xslices))
	d += 1
      
    if len(img_yslices):
	img_slices += img_yslices + [img_null]*(maxlen-len(img_yslices))
	d += 1
    
    if len(img_zslices):
	img_slices += img_zslices + [img_null]*(maxlen-len(img_zslices))
	d +=1
  
    if maxlen != 0:
	if img.GetNumberOfComponentsPerPixel() == 1:
	    img = sitk.Tile(img_slices, [maxlen,d])
	#TODO check in code to get Tile Filter working with VectorImages
	else:
	    img_comps = []
	    for i in range(0,img.GetNumberOfComponentsPerPixel()):
		img_slices_c = [sitk.VectorIndexSelectionCast(s, i) for s in img_slices]
		img_comps.append(sitk.Tile(img_slices_c, [maxlen,d]))
	    img = sitk.Compose(img_comps)
	    
    
    myshow(img, title, margin, dpi)