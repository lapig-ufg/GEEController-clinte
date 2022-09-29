import ee
from loguru import logger
from dynaconf import settings
from ClientGEE.Lapig import HelpLapig
from ClientGEE.functions import type_process, login_gee
from requests import post
from sys import exit

login_gee(ee)

# Imports GEE
grids = ee.FeatureCollection(
    "users/vieiramesquita/LAPIG-PASTURE/VECTORS/LANDSAT_GRID_V2_PASTURE"
)


# End Imports GEE
Lapig = HelpLapig(ee)

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
   return img.clip(gridSelect)

def generate_image(name, class_year):

    trainSamples = ee.FeatureCollection('users/vieiramesquita/LAPIG-PASTURE/VECTORS/mapbiomas_col6_brazil_training_samples_enh_PCI_MatoGrosso')

    landsatWRSPath = name[1:4]
    landsatWRSRow = name[4:7]

    rfNTrees = 200
    rfBagFraction = 0.5
    rfVarPersplit = 26
    neitilesT, neitiles = getNeibArea(landsatWRSPath,landsatWRSRow)
    neibRegion = [grids.filter(ee.Filter.inList('TILE_T',neitilesT)),neitiles] 
    classFieldName = 'class2020C'

    samplingArea = neibRegion[0]
    neighborhoodArea = neibRegion[1]
    classificationArea = grids.filter(ee.Filter.eq('TILE_T',name))

    Collections = {
         'L8':"LANDSAT/LC08/C02/T1_TOA",
         'L5':"LANDSAT/LT05/C02/T1_TOA",
         'L7':"LANDSAT/LE07/C02/T1_TOA"
    }

    startDate = f"{class_year - 1}-07-01"
    endDate = f"{class_year + 1}-06-30"

    landsatBandsWet = ['green_wet','red_wet','nir_wet', 'swir1_wet','swir2_wet','ndvi_wet','ndwi_wet','cai_wet']
    landsatBandsWetAmp = ['green_wet_amp','red_wet_amp','nir_wet_amp', 'swir1_wet_amp','swir2_wet_amp','ndvi_wet_amp','ndwi_wet_amp','cai_wet_amp']

    if int(class_year) > 2012:
        sat = 'L8'
        collection = Collections['L8']
        mask_exp = "(b('QA_PIXEL') == 21824 || b('QA_PIXEL') == 21952)"

    elif int(class_year) in (2000,2001,2002,2012):
        sat = 'L5_7'
        collection = Collections['L7']
        mask_exp = "(b('QA_PIXEL') == 5440 || b('QA_PIXEL') == 5504)"

    #elif int(class_year) < 1990:
    #    sat = 'L5_7'
    #    collection = "LANDSAT/LT05/C01/T1_TOA"
    #    mask_exp = "(b('BQA') == 672)"

    else:
        sat = 'L5_7'
        collection = Collections['L5']
        mask_exp = "(b('QA_PIXEL') == 5440 || b('QA_PIXEL') == 5504)"

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
            .map(maskClouds)
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
    try:
        mainScene = ee.Image(neibCollection.clip(classificationArea))

        features = [mainScene, neibCollection]
    except:
        logger.exception('mainScene error')
        exit(1)
 
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

    trainSamplesFeeded = features[1].sampleRegions(**{
        'collection': trainSamples.filterBounds(samplingArea).filter(ee.Filter.neq(classFieldName,None)),
        'properties': [classFieldName],
        'scale': 30,
        'tileScale': 16
    })

    classifier = classifier.train(trainSamplesFeeded, classFieldName,mainScene.bandNames())

    classification = features[0].classify(classifier).select(0)

    return (
        classificationArea.geometry().bounds(),
        ee.Image(classification).multiply(10000).int16(),
    )


def get_Exports(version, num, full_name):
    class_year, name, class_type  = full_name.split(';')
    class_year = int(class_year)
    ROI, image = generate_image(name,class_year)
    task = ee.batch.Export.image.toCloudStorage(
        **{
            "image": image,
            "description": f"pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",
            "bucket": "mapbiomas-public-temp",
            "fileNamePrefix": f"COLECAO/LANDSAT/PASTURE/pastureMapping_LS_Col7_{class_year}_LAPIG_{name}_{class_type}",
            "region": ROI,
            "scale": 30,
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
        return task.id, post(f"{settings.SERVER}/task/update?key={settings.KEYAPI}", json=rest)
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
        return 'None', post(f"{settings.SERVER}/task/update?key={settings.KEYAPI}", json=rest)