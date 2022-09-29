import ee
from loguru import logger
from dynaconf import settings
from ClientGEE.Lapig import HelpLapig
from ClientGEE.functions import type_process, login_gee
from requests import post
from sys import exit

login_gee(ee)

# Imports GEE
#ee.Initialize()
grids = ee.FeatureCollection(
	"users/vieiramesquita/LAPIG-PASTURE/VECTORS/LANDSAT_GRID_V2_PASTURE"
)

#feature_names = ['blue_wet_p1','blue_wet_p10','blue_wet_p25','blue_wet_p75','blue_wet_p90','blue_wet_p99','green_wet_p1','green_wet_p10','green_wet_p25','green_wet_p75','green_wet_p90','green_wet_p99','red_wet_p1','red_wet_p10','red_wet_p25','red_wet_p75','red_wet_p90','red_wet_p99','rededge1_wet_p1','rededge1_wet_p10','rededge1_wet_p25','rededge1_wet_p75','rededge1_wet_p90','rededge1_wet_p99','rededge2_wet_p1','rededge2_wet_p10','rededge2_wet_p25','rededge2_wet_p75','rededge2_wet_p90','rededge2_wet_p99','rededge3_wet_p1','rededge3_wet_p10','rededge3_wet_p25','rededge3_wet_p75','rededge3_wet_p90','rededge3_wet_p99','nir_wet_p1','nir_wet_p10','nir_wet_p25','nir_wet_p75','nir_wet_p90','nir_wet_p99','rededge4_wet_p1','rededge4_wet_p10','rededge4_wet_p25','rededge4_wet_p75','rededge4_wet_p90','rededge4_wet_p99','swir1_wet_p1','swir1_wet_p10','swir1_wet_p25','swir1_wet_p75','swir1_wet_p90','swir1_wet_p99','swir2_wet_p1','swir2_wet_p10','swir2_wet_p25','swir2_wet_p75','swir2_wet_p90','swir2_wet_p99','ndvi_wet_p1','ndvi_wet_p10','ndvi_wet_p25','ndvi_wet_p75','ndvi_wet_p90','ndvi_wet_p99','ndwi_wet_p1','ndwi_wet_p10','ndwi_wet_p25','ndwi_wet_p75','ndwi_wet_p90','ndwi_wet_p99','cai_wet_p1','cai_wet_p10','cai_wet_p25','cai_wet_p75','cai_wet_p90','cai_wet_p99','cri1_wet_p1','cri1_wet_p10','cri1_wet_p25','cri1_wet_p75','cri1_wet_p90','cri1_wet_p99','ari1_wet_p1','ari1_wet_p10','ari1_wet_p25','ari1_wet_p75','ari1_wet_p90','ari1_wet_p99','rgr_wet_p1','rgr_wet_p10','rgr_wet_p25','rgr_wet_p75','rgr_wet_p90','rgr_wet_p99','psri_wet_p1','psri_wet_p10','psri_wet_p25','psri_wet_p75','psri_wet_p90','psri_wet_p99','satvi_wet_p1','satvi_wet_p10','satvi_wet_p25','satvi_wet_p75','satvi_wet_p90','satvi_wet_p99','longitude','latitude','blue_wet_min','green_wet_min','red_wet_min','rededge1_wet_min','rededge2_wet_min','rededge3_wet_min','nir_wet_min','rededge4_wet_min','swir1_wet_min','swir2_wet_min','ndvi_wet_min','ndwi_wet_min','cai_wet_min','cri1_wet_min','ari1_wet_min','rgr_wet_min','psri_wet_min','satvi_wet_min','blue_wet_max','green_wet_max','red_wet_max','rededge1_wet_max','rededge2_wet_max','rededge3_wet_max','nir_wet_max','rededge4_wet_max','swir1_wet_max','swir2_wet_max','ndvi_wet_max','ndwi_wet_max','cai_wet_max','cri1_wet_max','ari1_wet_max','rgr_wet_max','psri_wet_max','satvi_wet_max','blue_wet_median','green_wet_median','red_wet_median','rededge1_wet_median','rededge2_wet_median','rededge3_wet_median','nir_wet_median','rededge4_wet_median','swir1_wet_median','swir2_wet_median','ndvi_wet_median','ndwi_wet_median','cai_wet_median','cri1_wet_median','ari1_wet_median','rgr_wet_median','psri_wet_median','satvi_wet_median','blue_wet_amp','green_wet_amp','red_wet_amp','rededge1_wet_amp','rededge2_wet_amp','rededge3_wet_amp','nir_wet_amp','rededge4_wet_amp','swir1_wet_amp','swir2_wet_amp','ndvi_wet_amp','ndwi_wet_amp','cai_wet_amp','cri1_wet_amp','ari1_wet_amp','rgr_wet_amp','psri_wet_amp','satvi_wet_amp','blue_wet_stdDev','green_wet_stdDev','red_wet_stdDev','rededge1_wet_stdDev','rededge2_wet_stdDev','rededge3_wet_stdDev','nir_wet_stdDev','rededge4_wet_stdDev','swir1_wet_stdDev','swir2_wet_stdDev','ndvi_wet_stdDev','ndwi_wet_stdDev','cai_wet_stdDev','cri1_wet_stdDev','ari1_wet_stdDev','rgr_wet_stdDev','psri_wet_stdDev','satvi_wet_stdDev','elevation','slope']

feature_names = ["0_green_wet_p10_x_-30_y_-30","0_green_wet_p25_x_-30_y_-30","0_green_wet_p75_x_-30_y_-30","0_green_wet_p90_x_-30_y_-30","0_red_wet_p10_x_-30_y_-30","0_red_wet_p25_x_-30_y_-30","0_red_wet_p75_x_-30_y_-30","0_red_wet_p90_x_-30_y_-30","0_nir_wet_p10_x_-30_y_-30","0_nir_wet_p25_x_-30_y_-30","0_nir_wet_p75_x_-30_y_-30","0_nir_wet_p90_x_-30_y_-30","0_swir1_wet_p10_x_-30_y_-30","0_swir1_wet_p25_x_-30_y_-30","0_swir1_wet_p75_x_-30_y_-30","0_swir1_wet_p90_x_-30_y_-30","0_swir2_wet_p10_x_-30_y_-30","0_swir2_wet_p25_x_-30_y_-30","0_swir2_wet_p75_x_-30_y_-30","0_swir2_wet_p90_x_-30_y_-30","0_ndvi_wet_p10_x_-30_y_-30","0_ndvi_wet_p25_x_-30_y_-30","0_ndvi_wet_p75_x_-30_y_-30","0_ndvi_wet_p90_x_-30_y_-30","0_ndwi_wet_p10_x_-30_y_-30","0_ndwi_wet_p25_x_-30_y_-30","0_ndwi_wet_p75_x_-30_y_-30","0_ndwi_wet_p90_x_-30_y_-30","0_cai_wet_p10_x_-30_y_-30","0_cai_wet_p25_x_-30_y_-30","0_cai_wet_p75_x_-30_y_-30","0_cai_wet_p90_x_-30_y_-30","0_longitude_x_-30_y_-30","0_latitude_x_-30_y_-30","0_green_wet_min_x_-30_y_-30","0_red_wet_min_x_-30_y_-30","0_nir_wet_min_x_-30_y_-30","0_swir1_wet_min_x_-30_y_-30","0_swir2_wet_min_x_-30_y_-30","0_ndvi_wet_min_x_-30_y_-30","0_ndwi_wet_min_x_-30_y_-30","0_cai_wet_min_x_-30_y_-30","0_green_wet_max_x_-30_y_-30","0_red_wet_max_x_-30_y_-30","0_nir_wet_max_x_-30_y_-30","0_swir1_wet_max_x_-30_y_-30","0_swir2_wet_max_x_-30_y_-30","0_ndvi_wet_max_x_-30_y_-30","0_ndwi_wet_max_x_-30_y_-30","0_cai_wet_max_x_-30_y_-30","0_green_wet_median_x_-30_y_-30","0_red_wet_median_x_-30_y_-30","0_nir_wet_median_x_-30_y_-30","0_swir1_wet_median_x_-30_y_-30","0_swir2_wet_median_x_-30_y_-30","0_ndvi_wet_median_x_-30_y_-30","0_ndwi_wet_median_x_-30_y_-30","0_cai_wet_median_x_-30_y_-30","0_green_wet_amp_x_-30_y_-30","0_red_wet_amp_x_-30_y_-30","0_nir_wet_amp_x_-30_y_-30","0_swir1_wet_amp_x_-30_y_-30","0_swir2_wet_amp_x_-30_y_-30","0_ndvi_wet_amp_x_-30_y_-30","0_ndwi_wet_amp_x_-30_y_-30","0_cai_wet_amp_x_-30_y_-30","0_green_wet_stdDev_x_-30_y_-30","0_red_wet_stdDev_x_-30_y_-30","0_nir_wet_stdDev_x_-30_y_-30","0_swir1_wet_stdDev_x_-30_y_-30","0_swir2_wet_stdDev_x_-30_y_-30","0_ndvi_wet_stdDev_x_-30_y_-30","0_ndwi_wet_stdDev_x_-30_y_-30","0_cai_wet_stdDev_x_-30_y_-30","0_elevation_x_-30_y_-30","0_slope_x_-30_y_-30","1_green_wet_p10_x_-30_y_0","1_green_wet_p25_x_-30_y_0","1_green_wet_p75_x_-30_y_0","1_green_wet_p90_x_-30_y_0","1_red_wet_p10_x_-30_y_0","1_red_wet_p25_x_-30_y_0","1_red_wet_p75_x_-30_y_0","1_red_wet_p90_x_-30_y_0","1_nir_wet_p10_x_-30_y_0","1_nir_wet_p25_x_-30_y_0","1_nir_wet_p75_x_-30_y_0","1_nir_wet_p90_x_-30_y_0","1_swir1_wet_p10_x_-30_y_0","1_swir1_wet_p25_x_-30_y_0","1_swir1_wet_p75_x_-30_y_0","1_swir1_wet_p90_x_-30_y_0","1_swir2_wet_p10_x_-30_y_0","1_swir2_wet_p25_x_-30_y_0","1_swir2_wet_p75_x_-30_y_0","1_swir2_wet_p90_x_-30_y_0","1_ndvi_wet_p10_x_-30_y_0","1_ndvi_wet_p25_x_-30_y_0","1_ndvi_wet_p75_x_-30_y_0","1_ndvi_wet_p90_x_-30_y_0","1_ndwi_wet_p10_x_-30_y_0","1_ndwi_wet_p25_x_-30_y_0","1_ndwi_wet_p75_x_-30_y_0","1_ndwi_wet_p90_x_-30_y_0","1_cai_wet_p10_x_-30_y_0","1_cai_wet_p25_x_-30_y_0","1_cai_wet_p75_x_-30_y_0","1_cai_wet_p90_x_-30_y_0","1_longitude_x_-30_y_0","1_latitude_x_-30_y_0","1_green_wet_min_x_-30_y_0","1_red_wet_min_x_-30_y_0","1_nir_wet_min_x_-30_y_0","1_swir1_wet_min_x_-30_y_0","1_swir2_wet_min_x_-30_y_0","1_ndvi_wet_min_x_-30_y_0","1_ndwi_wet_min_x_-30_y_0","1_cai_wet_min_x_-30_y_0","1_green_wet_max_x_-30_y_0","1_red_wet_max_x_-30_y_0","1_nir_wet_max_x_-30_y_0","1_swir1_wet_max_x_-30_y_0","1_swir2_wet_max_x_-30_y_0","1_ndvi_wet_max_x_-30_y_0","1_ndwi_wet_max_x_-30_y_0","1_cai_wet_max_x_-30_y_0","1_green_wet_median_x_-30_y_0","1_red_wet_median_x_-30_y_0","1_nir_wet_median_x_-30_y_0","1_swir1_wet_median_x_-30_y_0","1_swir2_wet_median_x_-30_y_0","1_ndvi_wet_median_x_-30_y_0","1_ndwi_wet_median_x_-30_y_0","1_cai_wet_median_x_-30_y_0","1_green_wet_amp_x_-30_y_0","1_red_wet_amp_x_-30_y_0","1_nir_wet_amp_x_-30_y_0","1_swir1_wet_amp_x_-30_y_0","1_swir2_wet_amp_x_-30_y_0","1_ndvi_wet_amp_x_-30_y_0","1_ndwi_wet_amp_x_-30_y_0","1_cai_wet_amp_x_-30_y_0","1_green_wet_stdDev_x_-30_y_0","1_red_wet_stdDev_x_-30_y_0","1_nir_wet_stdDev_x_-30_y_0","1_swir1_wet_stdDev_x_-30_y_0","1_swir2_wet_stdDev_x_-30_y_0","1_ndvi_wet_stdDev_x_-30_y_0","1_ndwi_wet_stdDev_x_-30_y_0","1_cai_wet_stdDev_x_-30_y_0","1_elevation_x_-30_y_0","1_slope_x_-30_y_0","2_green_wet_p10_x_-30_y_30","2_green_wet_p25_x_-30_y_30","2_green_wet_p75_x_-30_y_30","2_green_wet_p90_x_-30_y_30","2_red_wet_p10_x_-30_y_30","2_red_wet_p25_x_-30_y_30","2_red_wet_p75_x_-30_y_30","2_red_wet_p90_x_-30_y_30","2_nir_wet_p10_x_-30_y_30","2_nir_wet_p25_x_-30_y_30","2_nir_wet_p75_x_-30_y_30","2_nir_wet_p90_x_-30_y_30","2_swir1_wet_p10_x_-30_y_30","2_swir1_wet_p25_x_-30_y_30","2_swir1_wet_p75_x_-30_y_30","2_swir1_wet_p90_x_-30_y_30","2_swir2_wet_p10_x_-30_y_30","2_swir2_wet_p25_x_-30_y_30","2_swir2_wet_p75_x_-30_y_30","2_swir2_wet_p90_x_-30_y_30","2_ndvi_wet_p10_x_-30_y_30","2_ndvi_wet_p25_x_-30_y_30","2_ndvi_wet_p75_x_-30_y_30","2_ndvi_wet_p90_x_-30_y_30","2_ndwi_wet_p10_x_-30_y_30","2_ndwi_wet_p25_x_-30_y_30","2_ndwi_wet_p75_x_-30_y_30","2_ndwi_wet_p90_x_-30_y_30","2_cai_wet_p10_x_-30_y_30","2_cai_wet_p25_x_-30_y_30","2_cai_wet_p75_x_-30_y_30","2_cai_wet_p90_x_-30_y_30","2_longitude_x_-30_y_30","2_latitude_x_-30_y_30","2_green_wet_min_x_-30_y_30","2_red_wet_min_x_-30_y_30","2_nir_wet_min_x_-30_y_30","2_swir1_wet_min_x_-30_y_30","2_swir2_wet_min_x_-30_y_30","2_ndvi_wet_min_x_-30_y_30","2_ndwi_wet_min_x_-30_y_30","2_cai_wet_min_x_-30_y_30","2_green_wet_max_x_-30_y_30","2_red_wet_max_x_-30_y_30","2_nir_wet_max_x_-30_y_30","2_swir1_wet_max_x_-30_y_30","2_swir2_wet_max_x_-30_y_30","2_ndvi_wet_max_x_-30_y_30","2_ndwi_wet_max_x_-30_y_30","2_cai_wet_max_x_-30_y_30","2_green_wet_median_x_-30_y_30","2_red_wet_median_x_-30_y_30","2_nir_wet_median_x_-30_y_30","2_swir1_wet_median_x_-30_y_30","2_swir2_wet_median_x_-30_y_30","2_ndvi_wet_median_x_-30_y_30","2_ndwi_wet_median_x_-30_y_30","2_cai_wet_median_x_-30_y_30","2_green_wet_amp_x_-30_y_30","2_red_wet_amp_x_-30_y_30","2_nir_wet_amp_x_-30_y_30","2_swir1_wet_amp_x_-30_y_30","2_swir2_wet_amp_x_-30_y_30","2_ndvi_wet_amp_x_-30_y_30","2_ndwi_wet_amp_x_-30_y_30","2_cai_wet_amp_x_-30_y_30","2_green_wet_stdDev_x_-30_y_30","2_red_wet_stdDev_x_-30_y_30","2_nir_wet_stdDev_x_-30_y_30","2_swir1_wet_stdDev_x_-30_y_30","2_swir2_wet_stdDev_x_-30_y_30","2_ndvi_wet_stdDev_x_-30_y_30","2_ndwi_wet_stdDev_x_-30_y_30","2_cai_wet_stdDev_x_-30_y_30","2_elevation_x_-30_y_30","2_slope_x_-30_y_30","3_green_wet_p10_x_0_y_-30","3_green_wet_p25_x_0_y_-30","3_green_wet_p75_x_0_y_-30","3_green_wet_p90_x_0_y_-30","3_red_wet_p10_x_0_y_-30","3_red_wet_p25_x_0_y_-30","3_red_wet_p75_x_0_y_-30","3_red_wet_p90_x_0_y_-30","3_nir_wet_p10_x_0_y_-30","3_nir_wet_p25_x_0_y_-30","3_nir_wet_p75_x_0_y_-30","3_nir_wet_p90_x_0_y_-30","3_swir1_wet_p10_x_0_y_-30","3_swir1_wet_p25_x_0_y_-30","3_swir1_wet_p75_x_0_y_-30","3_swir1_wet_p90_x_0_y_-30","3_swir2_wet_p10_x_0_y_-30","3_swir2_wet_p25_x_0_y_-30","3_swir2_wet_p75_x_0_y_-30","3_swir2_wet_p90_x_0_y_-30","3_ndvi_wet_p10_x_0_y_-30","3_ndvi_wet_p25_x_0_y_-30","3_ndvi_wet_p75_x_0_y_-30","3_ndvi_wet_p90_x_0_y_-30","3_ndwi_wet_p10_x_0_y_-30","3_ndwi_wet_p25_x_0_y_-30","3_ndwi_wet_p75_x_0_y_-30","3_ndwi_wet_p90_x_0_y_-30","3_cai_wet_p10_x_0_y_-30","3_cai_wet_p25_x_0_y_-30","3_cai_wet_p75_x_0_y_-30","3_cai_wet_p90_x_0_y_-30","3_longitude_x_0_y_-30","3_latitude_x_0_y_-30","3_green_wet_min_x_0_y_-30","3_red_wet_min_x_0_y_-30","3_nir_wet_min_x_0_y_-30","3_swir1_wet_min_x_0_y_-30","3_swir2_wet_min_x_0_y_-30","3_ndvi_wet_min_x_0_y_-30","3_ndwi_wet_min_x_0_y_-30","3_cai_wet_min_x_0_y_-30","3_green_wet_max_x_0_y_-30","3_red_wet_max_x_0_y_-30","3_nir_wet_max_x_0_y_-30","3_swir1_wet_max_x_0_y_-30","3_swir2_wet_max_x_0_y_-30","3_ndvi_wet_max_x_0_y_-30","3_ndwi_wet_max_x_0_y_-30","3_cai_wet_max_x_0_y_-30","3_green_wet_median_x_0_y_-30","3_red_wet_median_x_0_y_-30","3_nir_wet_median_x_0_y_-30","3_swir1_wet_median_x_0_y_-30","3_swir2_wet_median_x_0_y_-30","3_ndvi_wet_median_x_0_y_-30","3_ndwi_wet_median_x_0_y_-30","3_cai_wet_median_x_0_y_-30","3_green_wet_amp_x_0_y_-30","3_red_wet_amp_x_0_y_-30","3_nir_wet_amp_x_0_y_-30","3_swir1_wet_amp_x_0_y_-30","3_swir2_wet_amp_x_0_y_-30","3_ndvi_wet_amp_x_0_y_-30","3_ndwi_wet_amp_x_0_y_-30","3_cai_wet_amp_x_0_y_-30","3_green_wet_stdDev_x_0_y_-30","3_red_wet_stdDev_x_0_y_-30","3_nir_wet_stdDev_x_0_y_-30","3_swir1_wet_stdDev_x_0_y_-30","3_swir2_wet_stdDev_x_0_y_-30","3_ndvi_wet_stdDev_x_0_y_-30","3_ndwi_wet_stdDev_x_0_y_-30","3_cai_wet_stdDev_x_0_y_-30","3_elevation_x_0_y_-30","3_slope_x_0_y_-30","4_green_wet_p10_x_0_y_0","4_green_wet_p25_x_0_y_0","4_green_wet_p75_x_0_y_0","4_green_wet_p90_x_0_y_0","4_red_wet_p10_x_0_y_0","4_red_wet_p25_x_0_y_0","4_red_wet_p75_x_0_y_0","4_red_wet_p90_x_0_y_0","4_nir_wet_p10_x_0_y_0","4_nir_wet_p25_x_0_y_0","4_nir_wet_p75_x_0_y_0","4_nir_wet_p90_x_0_y_0","4_swir1_wet_p10_x_0_y_0","4_swir1_wet_p25_x_0_y_0","4_swir1_wet_p75_x_0_y_0","4_swir1_wet_p90_x_0_y_0","4_swir2_wet_p10_x_0_y_0","4_swir2_wet_p25_x_0_y_0","4_swir2_wet_p75_x_0_y_0","4_swir2_wet_p90_x_0_y_0","4_ndvi_wet_p10_x_0_y_0","4_ndvi_wet_p25_x_0_y_0","4_ndvi_wet_p75_x_0_y_0","4_ndvi_wet_p90_x_0_y_0","4_ndwi_wet_p10_x_0_y_0","4_ndwi_wet_p25_x_0_y_0","4_ndwi_wet_p75_x_0_y_0","4_ndwi_wet_p90_x_0_y_0","4_cai_wet_p10_x_0_y_0","4_cai_wet_p25_x_0_y_0","4_cai_wet_p75_x_0_y_0","4_cai_wet_p90_x_0_y_0","4_longitude_x_0_y_0","4_latitude_x_0_y_0","4_green_wet_min_x_0_y_0","4_red_wet_min_x_0_y_0","4_nir_wet_min_x_0_y_0","4_swir1_wet_min_x_0_y_0","4_swir2_wet_min_x_0_y_0","4_ndvi_wet_min_x_0_y_0","4_ndwi_wet_min_x_0_y_0","4_cai_wet_min_x_0_y_0","4_green_wet_max_x_0_y_0","4_red_wet_max_x_0_y_0","4_nir_wet_max_x_0_y_0","4_swir1_wet_max_x_0_y_0","4_swir2_wet_max_x_0_y_0","4_ndvi_wet_max_x_0_y_0","4_ndwi_wet_max_x_0_y_0","4_cai_wet_max_x_0_y_0","4_green_wet_median_x_0_y_0","4_red_wet_median_x_0_y_0","4_nir_wet_median_x_0_y_0","4_swir1_wet_median_x_0_y_0","4_swir2_wet_median_x_0_y_0","4_ndvi_wet_median_x_0_y_0","4_ndwi_wet_median_x_0_y_0","4_cai_wet_median_x_0_y_0","4_green_wet_amp_x_0_y_0","4_red_wet_amp_x_0_y_0","4_nir_wet_amp_x_0_y_0","4_swir1_wet_amp_x_0_y_0","4_swir2_wet_amp_x_0_y_0","4_ndvi_wet_amp_x_0_y_0","4_ndwi_wet_amp_x_0_y_0","4_cai_wet_amp_x_0_y_0","4_green_wet_stdDev_x_0_y_0","4_red_wet_stdDev_x_0_y_0","4_nir_wet_stdDev_x_0_y_0","4_swir1_wet_stdDev_x_0_y_0","4_swir2_wet_stdDev_x_0_y_0","4_ndvi_wet_stdDev_x_0_y_0","4_ndwi_wet_stdDev_x_0_y_0","4_cai_wet_stdDev_x_0_y_0","4_elevation_x_0_y_0","4_slope_x_0_y_0","5_green_wet_p10_x_0_y_30","5_green_wet_p25_x_0_y_30","5_green_wet_p75_x_0_y_30","5_green_wet_p90_x_0_y_30","5_red_wet_p10_x_0_y_30","5_red_wet_p25_x_0_y_30","5_red_wet_p75_x_0_y_30","5_red_wet_p90_x_0_y_30","5_nir_wet_p10_x_0_y_30","5_nir_wet_p25_x_0_y_30","5_nir_wet_p75_x_0_y_30","5_nir_wet_p90_x_0_y_30","5_swir1_wet_p10_x_0_y_30","5_swir1_wet_p25_x_0_y_30","5_swir1_wet_p75_x_0_y_30","5_swir1_wet_p90_x_0_y_30","5_swir2_wet_p10_x_0_y_30","5_swir2_wet_p25_x_0_y_30","5_swir2_wet_p75_x_0_y_30","5_swir2_wet_p90_x_0_y_30","5_ndvi_wet_p10_x_0_y_30","5_ndvi_wet_p25_x_0_y_30","5_ndvi_wet_p75_x_0_y_30","5_ndvi_wet_p90_x_0_y_30","5_ndwi_wet_p10_x_0_y_30","5_ndwi_wet_p25_x_0_y_30","5_ndwi_wet_p75_x_0_y_30","5_ndwi_wet_p90_x_0_y_30","5_cai_wet_p10_x_0_y_30","5_cai_wet_p25_x_0_y_30","5_cai_wet_p75_x_0_y_30","5_cai_wet_p90_x_0_y_30","5_longitude_x_0_y_30","5_latitude_x_0_y_30","5_green_wet_min_x_0_y_30","5_red_wet_min_x_0_y_30","5_nir_wet_min_x_0_y_30","5_swir1_wet_min_x_0_y_30","5_swir2_wet_min_x_0_y_30","5_ndvi_wet_min_x_0_y_30","5_ndwi_wet_min_x_0_y_30","5_cai_wet_min_x_0_y_30","5_green_wet_max_x_0_y_30","5_red_wet_max_x_0_y_30","5_nir_wet_max_x_0_y_30","5_swir1_wet_max_x_0_y_30","5_swir2_wet_max_x_0_y_30","5_ndvi_wet_max_x_0_y_30","5_ndwi_wet_max_x_0_y_30","5_cai_wet_max_x_0_y_30","5_green_wet_median_x_0_y_30","5_red_wet_median_x_0_y_30","5_nir_wet_median_x_0_y_30","5_swir1_wet_median_x_0_y_30","5_swir2_wet_median_x_0_y_30","5_ndvi_wet_median_x_0_y_30","5_ndwi_wet_median_x_0_y_30","5_cai_wet_median_x_0_y_30","5_green_wet_amp_x_0_y_30","5_red_wet_amp_x_0_y_30","5_nir_wet_amp_x_0_y_30","5_swir1_wet_amp_x_0_y_30","5_swir2_wet_amp_x_0_y_30","5_ndvi_wet_amp_x_0_y_30","5_ndwi_wet_amp_x_0_y_30","5_cai_wet_amp_x_0_y_30","5_green_wet_stdDev_x_0_y_30","5_red_wet_stdDev_x_0_y_30","5_nir_wet_stdDev_x_0_y_30","5_swir1_wet_stdDev_x_0_y_30","5_swir2_wet_stdDev_x_0_y_30","5_ndvi_wet_stdDev_x_0_y_30","5_ndwi_wet_stdDev_x_0_y_30","5_cai_wet_stdDev_x_0_y_30","5_elevation_x_0_y_30","5_slope_x_0_y_30","6_green_wet_p10_x_30_y_-30","6_green_wet_p25_x_30_y_-30","6_green_wet_p75_x_30_y_-30","6_green_wet_p90_x_30_y_-30","6_red_wet_p10_x_30_y_-30","6_red_wet_p25_x_30_y_-30","6_red_wet_p75_x_30_y_-30","6_red_wet_p90_x_30_y_-30","6_nir_wet_p10_x_30_y_-30","6_nir_wet_p25_x_30_y_-30","6_nir_wet_p75_x_30_y_-30","6_nir_wet_p90_x_30_y_-30","6_swir1_wet_p10_x_30_y_-30","6_swir1_wet_p25_x_30_y_-30","6_swir1_wet_p75_x_30_y_-30","6_swir1_wet_p90_x_30_y_-30","6_swir2_wet_p10_x_30_y_-30","6_swir2_wet_p25_x_30_y_-30","6_swir2_wet_p75_x_30_y_-30","6_swir2_wet_p90_x_30_y_-30","6_ndvi_wet_p10_x_30_y_-30","6_ndvi_wet_p25_x_30_y_-30","6_ndvi_wet_p75_x_30_y_-30","6_ndvi_wet_p90_x_30_y_-30","6_ndwi_wet_p10_x_30_y_-30","6_ndwi_wet_p25_x_30_y_-30","6_ndwi_wet_p75_x_30_y_-30","6_ndwi_wet_p90_x_30_y_-30","6_cai_wet_p10_x_30_y_-30","6_cai_wet_p25_x_30_y_-30","6_cai_wet_p75_x_30_y_-30","6_cai_wet_p90_x_30_y_-30","6_longitude_x_30_y_-30","6_latitude_x_30_y_-30","6_green_wet_min_x_30_y_-30","6_red_wet_min_x_30_y_-30","6_nir_wet_min_x_30_y_-30","6_swir1_wet_min_x_30_y_-30","6_swir2_wet_min_x_30_y_-30","6_ndvi_wet_min_x_30_y_-30","6_ndwi_wet_min_x_30_y_-30","6_cai_wet_min_x_30_y_-30","6_green_wet_max_x_30_y_-30","6_red_wet_max_x_30_y_-30","6_nir_wet_max_x_30_y_-30","6_swir1_wet_max_x_30_y_-30","6_swir2_wet_max_x_30_y_-30","6_ndvi_wet_max_x_30_y_-30","6_ndwi_wet_max_x_30_y_-30","6_cai_wet_max_x_30_y_-30","6_green_wet_median_x_30_y_-30","6_red_wet_median_x_30_y_-30","6_nir_wet_median_x_30_y_-30","6_swir1_wet_median_x_30_y_-30","6_swir2_wet_median_x_30_y_-30","6_ndvi_wet_median_x_30_y_-30","6_ndwi_wet_median_x_30_y_-30","6_cai_wet_median_x_30_y_-30","6_green_wet_amp_x_30_y_-30","6_red_wet_amp_x_30_y_-30","6_nir_wet_amp_x_30_y_-30","6_swir1_wet_amp_x_30_y_-30","6_swir2_wet_amp_x_30_y_-30","6_ndvi_wet_amp_x_30_y_-30","6_ndwi_wet_amp_x_30_y_-30","6_cai_wet_amp_x_30_y_-30","6_green_wet_stdDev_x_30_y_-30","6_red_wet_stdDev_x_30_y_-30","6_nir_wet_stdDev_x_30_y_-30","6_swir1_wet_stdDev_x_30_y_-30","6_swir2_wet_stdDev_x_30_y_-30","6_ndvi_wet_stdDev_x_30_y_-30","6_ndwi_wet_stdDev_x_30_y_-30","6_cai_wet_stdDev_x_30_y_-30","6_elevation_x_30_y_-30","6_slope_x_30_y_-30","7_green_wet_p10_x_30_y_0","7_green_wet_p25_x_30_y_0","7_green_wet_p75_x_30_y_0","7_green_wet_p90_x_30_y_0","7_red_wet_p10_x_30_y_0","7_red_wet_p25_x_30_y_0","7_red_wet_p75_x_30_y_0","7_red_wet_p90_x_30_y_0","7_nir_wet_p10_x_30_y_0","7_nir_wet_p25_x_30_y_0","7_nir_wet_p75_x_30_y_0","7_nir_wet_p90_x_30_y_0","7_swir1_wet_p10_x_30_y_0","7_swir1_wet_p25_x_30_y_0","7_swir1_wet_p75_x_30_y_0","7_swir1_wet_p90_x_30_y_0","7_swir2_wet_p10_x_30_y_0","7_swir2_wet_p25_x_30_y_0","7_swir2_wet_p75_x_30_y_0","7_swir2_wet_p90_x_30_y_0","7_ndvi_wet_p10_x_30_y_0","7_ndvi_wet_p25_x_30_y_0","7_ndvi_wet_p75_x_30_y_0","7_ndvi_wet_p90_x_30_y_0","7_ndwi_wet_p10_x_30_y_0","7_ndwi_wet_p25_x_30_y_0","7_ndwi_wet_p75_x_30_y_0","7_ndwi_wet_p90_x_30_y_0","7_cai_wet_p10_x_30_y_0","7_cai_wet_p25_x_30_y_0","7_cai_wet_p75_x_30_y_0","7_cai_wet_p90_x_30_y_0","7_longitude_x_30_y_0","7_latitude_x_30_y_0","7_green_wet_min_x_30_y_0","7_red_wet_min_x_30_y_0","7_nir_wet_min_x_30_y_0","7_swir1_wet_min_x_30_y_0","7_swir2_wet_min_x_30_y_0","7_ndvi_wet_min_x_30_y_0","7_ndwi_wet_min_x_30_y_0","7_cai_wet_min_x_30_y_0","7_green_wet_max_x_30_y_0","7_red_wet_max_x_30_y_0","7_nir_wet_max_x_30_y_0","7_swir1_wet_max_x_30_y_0","7_swir2_wet_max_x_30_y_0","7_ndvi_wet_max_x_30_y_0","7_ndwi_wet_max_x_30_y_0","7_cai_wet_max_x_30_y_0","7_green_wet_median_x_30_y_0","7_red_wet_median_x_30_y_0","7_nir_wet_median_x_30_y_0","7_swir1_wet_median_x_30_y_0","7_swir2_wet_median_x_30_y_0","7_ndvi_wet_median_x_30_y_0","7_ndwi_wet_median_x_30_y_0","7_cai_wet_median_x_30_y_0","7_green_wet_amp_x_30_y_0","7_red_wet_amp_x_30_y_0","7_nir_wet_amp_x_30_y_0","7_swir1_wet_amp_x_30_y_0","7_swir2_wet_amp_x_30_y_0","7_ndvi_wet_amp_x_30_y_0","7_ndwi_wet_amp_x_30_y_0","7_cai_wet_amp_x_30_y_0","7_green_wet_stdDev_x_30_y_0","7_red_wet_stdDev_x_30_y_0","7_nir_wet_stdDev_x_30_y_0","7_swir1_wet_stdDev_x_30_y_0","7_swir2_wet_stdDev_x_30_y_0","7_ndvi_wet_stdDev_x_30_y_0","7_ndwi_wet_stdDev_x_30_y_0","7_cai_wet_stdDev_x_30_y_0","7_elevation_x_30_y_0","7_slope_x_30_y_0","8_green_wet_p10_x_30_y_30","8_green_wet_p25_x_30_y_30","8_green_wet_p75_x_30_y_30","8_green_wet_p90_x_30_y_30","8_red_wet_p10_x_30_y_30","8_red_wet_p25_x_30_y_30","8_red_wet_p75_x_30_y_30","8_red_wet_p90_x_30_y_30","8_nir_wet_p10_x_30_y_30","8_nir_wet_p25_x_30_y_30","8_nir_wet_p75_x_30_y_30","8_nir_wet_p90_x_30_y_30","8_swir1_wet_p10_x_30_y_30","8_swir1_wet_p25_x_30_y_30","8_swir1_wet_p75_x_30_y_30","8_swir1_wet_p90_x_30_y_30","8_swir2_wet_p10_x_30_y_30","8_swir2_wet_p25_x_30_y_30","8_swir2_wet_p75_x_30_y_30","8_swir2_wet_p90_x_30_y_30","8_ndvi_wet_p10_x_30_y_30","8_ndvi_wet_p25_x_30_y_30","8_ndvi_wet_p75_x_30_y_30","8_ndvi_wet_p90_x_30_y_30","8_ndwi_wet_p10_x_30_y_30","8_ndwi_wet_p25_x_30_y_30","8_ndwi_wet_p75_x_30_y_30","8_ndwi_wet_p90_x_30_y_30","8_cai_wet_p10_x_30_y_30","8_cai_wet_p25_x_30_y_30","8_cai_wet_p75_x_30_y_30","8_cai_wet_p90_x_30_y_30","8_longitude_x_30_y_30","8_latitude_x_30_y_30","8_green_wet_min_x_30_y_30","8_red_wet_min_x_30_y_30","8_nir_wet_min_x_30_y_30","8_swir1_wet_min_x_30_y_30","8_swir2_wet_min_x_30_y_30","8_ndvi_wet_min_x_30_y_30","8_ndwi_wet_min_x_30_y_30","8_cai_wet_min_x_30_y_30","8_green_wet_max_x_30_y_30","8_red_wet_max_x_30_y_30","8_nir_wet_max_x_30_y_30","8_swir1_wet_max_x_30_y_30","8_swir2_wet_max_x_30_y_30","8_ndvi_wet_max_x_30_y_30","8_ndwi_wet_max_x_30_y_30","8_cai_wet_max_x_30_y_30","8_green_wet_median_x_30_y_30","8_red_wet_median_x_30_y_30","8_nir_wet_median_x_30_y_30","8_swir1_wet_median_x_30_y_30","8_swir2_wet_median_x_30_y_30","8_ndvi_wet_median_x_30_y_30","8_ndwi_wet_median_x_30_y_30","8_cai_wet_median_x_30_y_30","8_green_wet_amp_x_30_y_30","8_red_wet_amp_x_30_y_30","8_nir_wet_amp_x_30_y_30","8_swir1_wet_amp_x_30_y_30","8_swir2_wet_amp_x_30_y_30","8_ndvi_wet_amp_x_30_y_30","8_ndwi_wet_amp_x_30_y_30","8_cai_wet_amp_x_30_y_30","8_green_wet_stdDev_x_30_y_30","8_red_wet_stdDev_x_30_y_30","8_nir_wet_stdDev_x_30_y_30","8_swir1_wet_stdDev_x_30_y_30","8_swir2_wet_stdDev_x_30_y_30","8_ndvi_wet_stdDev_x_30_y_30","8_ndwi_wet_stdDev_x_30_y_30","8_cai_wet_stdDev_x_30_y_30","8_elevation_x_30_y_30","8_slope_x_30_y_30"]

# End Imports GEE
Lapig = HelpLapig(ee)

trainSamples_cultivado = ee.FeatureCollection('users/vieiramesquita/mapbiomas_col3_1_all_stages_12_03_2018_past_cultivado_QGIS_new_pampa_v2')
trainSamples_natural = ee.FeatureCollection('users/vieiramesquita/mapbiomas_col3_1_all_stages_12_03_2018_past_natural_QGIS')

trainSamples_cultivado_col6_edit = ee.FeatureCollection('users/vieiramesquita/LAPIG-PASTURE/VECTORS/mapbiomas_col6_all_stages_10_06_2021_past_cultivado_and_natural_QGIS_v4')

def getNeibArea(path,row):
	path = int(path)
	row = int(row)

	neitiles = []
	neitilesT = []

	for pInc in range(path-1, path+2):
		for rInc in range(row-1,row+2):
			if path == 1 and pInc == 0:
				pInc = 233
			elif path == 233 and pInc == 234:
				pInc = 1

			neitiles.append(f"{pInc}/{rInc}")
			neitilesT.append(f"T{pInc:03}{rInc:03}")

	return neitilesT,neitiles

def clipCollection(img):
	 wrsProps = ee.Number(img.get('WRS_PATH')).int().format().cat('/').cat(ee.Number(img.get('WRS_ROW')).int().format())
	 gridSelect = grids.filter(ee.Filter.eq('SPRNOME',wrsProps))
	 return img.clip(gridSelect).reproject(img.select('B2').projection())

def generate_image(name, class_year,class_type):


	landsatWRSPath = name[1:4]
	landsatWRSRow = name[4:7]

	rfNTrees = 100
	rfBagFraction = 0.5
	rfVarPersplit = 26
	neitilesT, neitiles = getNeibArea(landsatWRSPath,landsatWRSRow)
	neibRegion = [grids.filter(ee.Filter.inList('TILE_T',neitilesT)),neitiles] 
	#classFieldName = f'cons_{class_year}'

	samplingArea = neibRegion[0]
	neighborhoodArea = neibRegion[1]
	classificationArea = grids.filter(ee.Filter.eq('TILE_T',name))


	Collections = {
		'L8':"LANDSAT/LC08/C02/T1_TOA",
		'L7':"LANDSAT/LT05/C02/T1_TOA",
		'L5':"LANDSAT/LE07/C02/T1_TOA"
	}

	landsatBandsWet = ['green_wet','red_wet','nir_wet', 'swir1_wet','swir2_wet','ndvi_wet','ndwi_wet','cai_wet'];
	landsatBandsWetAmp = ['green_wet_amp','red_wet_amp','nir_wet_amp', 'swir1_wet_amp','swir2_wet_amp','ndvi_wet_amp','ndwi_wet_amp','cai_wet_amp'];

	def spectralFeatures(image):
		ndvi = Lapig.expression_select(image, sat, "NDVI")
		ndwi = Lapig.expression_select(image, sat, "NDWI")
		cai = Lapig.expression_select(image, sat, "CAI")

		return image.addBands([ndvi, ndwi, cai])

	def onlyWetSeasonNei(image):
		seasonMask = image.select("ndvi_wet").gte(wetThresholdNei)
		return image.mask(seasonMask)

	def maskClouds(img):

		qaImage = img.expression(mask_exp).add(img.lte(0))

		return img.mask(qaImage)

	SRTM = Lapig.getSRTM()
	elevation = SRTM["elevation"]
	slope = SRTM["slope"]
	#######################################


	trainSamplesFeeded = ee.FeatureCollection([])
	
	listYearsApp = []
	
	if int(class_year) == 2018:
		
		listYearsApp = [2016,2017,2018,2019]
		
	elif int(class_year) == 2019:
		
		listYearsApp = [2017,2018,2019,2020]
		
	elif int(class_year) == 2020:
		
		listYearsApp = [2017,2018,2019,2020]
		
	elif int(class_year) == 2021:
		
		listYearsApp = [2017,2018,2019,2020,2021]
	
	for year_images in listYearsApp:

		startDate = f"{year_images - 1}-07-01"
		endDate = f"{year_images + 1}-06-30"

		if int(class_year) > 2012:
			sat = 'L8'
			collection = Collections['L8']
			mask_exp = "(b('QA_PIXEL') == 21824 || b('QA_PIXEL') == 21952)"

		elif int(class_year) in (2000,2001,2002,2012):
			sat = 'L5_7'
			collection = Collections['L7']
			mask_exp = "(b('QA_PIXEL') == 5440 || b('QA_PIXEL') == 5504)"

		elif int(class_year) < 1990:
			sat = 'L5_7'
			collection = "LANDSAT/LT05/C01/T1_TOA"
			mask_exp = "(b('BQA') == 672)"

		else:
			sat = 'L5_7'
			collection = Collections['L5']
			mask_exp = "(b('QA_PIXEL') == 5440 || b('QA_PIXEL') == 5504)"

		neibData = []

		for i in neighborhoodArea:
	
			sceneInfo = i.split("/")
			query_SPRNOME = f'{int(sceneInfo[0])}/{int(sceneInfo[1])}'
			spectralDataNei = (
				ee.ImageCollection(collection).filterMetadata(
					"WRS_PATH", "equals", int(sceneInfo[0])
				)
				.filterMetadata("WRS_ROW", "equals", int(sceneInfo[1]))
				.filterDate(startDate, endDate)
				.map(spectralFeatures)
				.map(clipCollection)
				.select(Lapig.getExpression(sat,'bands'))
			)
						
			wetThresholdNei = spectralDataNei.select("NDVI").reduce(
				ee.Reducer.percentile([25])
			)
	
			wetSpectralDataNei = spectralDataNei.select(
				Lapig.getBands(sat), landsatBandsWet
			).map(onlyWetSeasonNei)
	
			temporalData = Lapig.getLatLong(
				 Lapig.temporalPercs(wetSpectralDataNei,[10, 25, 75, 90])
			).addBands(
				[
					 Lapig.temporalFeatures(wetSpectralDataNei, landsatBandsWetAmp),
					elevation,
					slope,
				]
			)
	
			bandSize = ee.Number(temporalData.bandNames().size())
	
			neibData.append(temporalData.set({"BandNumber": bandSize}))
	
		neibCollection = (
			ee.ImageCollection(neibData)
			.filter(ee.Filter.gt("BandNumber", 4))
			.mosaic()
			.clip(samplingArea)
		)
	
		satPxSize = 30
		window = 1
		windowSize = satPxSize*window
		

		def rename_bands(bands_names,suffix):
			def retrieve_BandName(band):
				return ee.String(band).cat(suffix)
			
			return bands_names.map(retrieve_BandName)
		
		def translate_features(x,y):
	
			suffix = f"_x_{x}_y_{y}"
			return ee.Image(neibCollection).translate(x,y,'meters').rename(rename_bands(neibCollection.bandNames(),suffix))
		
		pxPosList = [translate_features(x,y) 
				for x in range(windowSize*-1,windowSize+1,satPxSize) 
				for y in range(windowSize*-1,windowSize+1,satPxSize)]

		rtv_shifted = ee.ImageCollection(ee.List(pxPosList).flatten()).toBands()

		if (year_images < 2021):

			if (year_images > 2017):

				if class_type == 'planted':
					classField = f'cons_{year_images}'
				elif class_type == 'natural':
					classField = f'cons_{year_images}n'
				else:
					exit(1)

				trainSamples = trainSamples_cultivado_col6_edit.select([classField], ['classValues']).filterBounds(samplingArea)
			
			else:
				classField = f'cons_{year_images}'

				if class_type == 'planted':
					trainSamples = trainSamples_cultivado.select([classField], ['classValues']).filterBounds(samplingArea)
				elif class_type == 'natural':
					trainSamples = trainSamples_natural.select([classField], ['classValues']).filterBounds(samplingArea)
				else:
					exit(1)

			trainSamplesFeeded_year = rtv_shifted.sampleRegions(**{
				'collection': trainSamples.filter(ee.Filter.neq('classValues', None)),
				'properties': ['classValues'],
				'scale': 30,
				'tileScale': 16
			});

			trainSamplesFeeded = ee.FeatureCollection(trainSamplesFeeded).merge(trainSamplesFeeded_year)
			
		if int(class_year) == int(year_images):
			mainScene =rtv_shifted.clip(classificationArea)

	features = mainScene
	
 	#######################################/

	classifier = ee.Classifier.smileRandomForest(
		rfNTrees,
		rfVarPersplit, 
		1,
		rfBagFraction,
		None,
		int(class_year)
		)
	classifier = classifier.setOutputMode("PROBABILITY")

	classifier = classifier.train(trainSamplesFeeded, 'classValues' ,feature_names);

	classification = features.classify(classifier).select(0)

	#task = ee.batch.Export.image.toDrive(\
	#	image = ee.Image(classification).multiply(10000).int16(),\
	#	crs = "EPSG:4326",\
	#	region =	classificationArea.geometry().bounds(),\
	#	description = f"pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",\
	#	folder = "mapbiomas-public-temp",\
	#	fileNamePrefix = f"pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",\
	#	scale = 30,\
	#	maxPixels = 1.0e13,\
	#	)
	#
	#task.start()

	return (
		classificationArea.geometry().bounds(),
		ee.Image(classification).multiply(10000).int16(),
	)

def get_Exports(version, num, full_name):
	class_year, name, class_type	= full_name.split(';')

	ROI, image = generate_image(name,class_year, class_type)
	task = ee.batch.Export.image.toCloudStorage(
		**{
			"image": image,
			"description": f"pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",
			"bucket": "mapbiomas-public-temp",
			"fileNamePrefix": f"COLECAO/LANDSAT/PASTURE/pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",
			"region": ROI,
			"scale": 30,
			#"shardSize":32,
			"maxPixels": 1.0e13,
		}
	)
	try:
		task.start()
		rest = {
			"id_": f"{version}_{full_name}",
			"version": version,
			"name": full_name,
			"state": type_process(task.state),
			"task_id": task.id,
			"num": num,
			"client": settings.CLIENT
		}
		return task.id, post(f"{settings.SERVER}/task/update", json=rest)
	except Exception as e:
		rest = {
			"id_": f"{version}_{full_name}",
			"version": version,
			"name": full_name,
			"state": 'None',
			"task_id": task.id,
			"num": num,
			"client": settings.CLIENT
		}
		logger.warning(f'Error ao exporta, dados recebidp{rest} error:{e}')
		return 'None', post(f"{settings.SERVER}/task/update", json=rest)