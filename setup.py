import os

#CORE ISSUER
# Account that issues custom asset
core_iss_public = os.environ.get('CORE_ISS_PUBLIC')
core_iss_secret = os.environ.get('CORE_ISS_SECRET')

#CORE DISTRIBUTOR
# Account that distributes custom asset
core_dist_public = os.environ.get('CORE_DIST_PUBLIC')
core_dist_secret = os.environ.get('CORE_DIST_SECRET')

#ISSX
# Secondary issuer account
issx_public = os.environ.get('ISSX_PUBLIC')
issx_secret = os.environ.get('ISSX_SECRET')

#DISTX TEST
# Distribution account
distx_public = os.environ.get('DISTX_PUBLIC')
distx_secret = os.environ.get('DISTX_SECRET')
