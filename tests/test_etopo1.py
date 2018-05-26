
from pylab import *
import numpy
from clawpack.geoclaw import topotools

extent = [-125,-124, 48, 48.5]

def test_etopo1_topo(make_plot=False, save=False):
    topo1 = topotools.read_netcdf('etopo1', extent=extent, verbose=True)

    topo10 = topotools.read_netcdf('etopo1', extent=extent, 
                                   coarsen=10, verbose=True)
    fname = 'data/etopo1_10min.asc'
    if save:
        topo10.write(fname, topo_type=3, Z_format='%.0f')
        print('Created %s' % fname)

    topo10input = topotools.Topography()
    topo10input.read(fname, topo_type=3)
    
    assert numpy.allclose(topo10.Z, topo10input.Z), \
           "topo10.Z does not agree with archived data"
    
    if make_plot:
        figure(figsize=(12,5))
        ax1 = subplot(1,2,1)
        topo1.plot(axes=ax1)
        title('1 minute etopo1 data')
        ax10 = subplot(1,2,2)
        topo10.plot(axes=ax10)
        title('10 minute etopo1 data')
        pname = 'etopo1_test_plot.png'
        savefig(pname)
        print('Created %s' % pname)
    
def test_etopo1_xarray():

    import xarray
    topo10,topo10_xarray = topotools.read_netcdf('etopo1', extent=extent, 
                                                 return_xarray=True,
                                                 coarsen=10, verbose=True)
    fname = 'data/etopo1_10min.asc'
    topo10input = topotools.Topography()
    topo10input.read(fname, topo_type=3)
    
    assert numpy.allclose(topo10_xarray['z'], topo10input.Z), \
           "topo10_xarray['z'] does not agree with archived data"
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "plot" in sys.argv[1].lower():
            test_etopo1_topo(make_plot=True)
        elif bool(sys.argv[1]):
            test_etopo1_topo(save=True)
    else:
        # Run tests
        test_etopo1_topo()
        try:
            import xarray
            test_etopo1_xarray()
        except:
            print("Skipping test_etopo1_xarray since xarray not installed")

        print("All tests passed.")

