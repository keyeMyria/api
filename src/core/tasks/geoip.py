"""Tasks for updating GeoIP database."""
import os
import json
from celery import shared_task
from django.conf import settings
import requests
import shutil
import logging

log = logging.getLogger(__name__)
path = 'http://geolite.maxmind.com/download/geoip/database/'
city = 'GeoLite2-City.tar.gz'  # noqa
country = 'GeoLite2-Country.tar.gz'  # noqa
out_dir = os.path.join(settings.REPO_PATH, 'tmp', 'geoip')
versions_file = os.path.join(out_dir, 'versions.json')
os.makedirs(out_dir, exist_ok=True)


@shared_task
def download_geoip_databases():
    """Download City and Country databases"""
    # First, check if file was updated
    # Get current versions
    city_version = ''
    country_version = ''
    versions = {}
    if os.path.isfile(versions_file):
        versions = json.load(open(versions_file, 'r'))
        city_version = versions.get('city', '')
        country_version = versions.get('country', '')

    # If we had a file already - check new version
    r = requests.head(path + city)
    # 'GeoLite2-City_20170905.tar.gz'
    filename = r.headers['content-disposition'].split('=')[1]
    # '20170905'
    new_city_version = filename.split('_')[1][:-7]

    if new_city_version > city_version or city_version is None:
        log.debug('Downloading {} version of GeoIP-City...'.format(
            new_city_version
        ))
        r = requests.get(path + city, stream=True)
        if r.status_code == 200:
            with open(os.path.join(out_dir, city), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        versions['city'] = new_city_version
    else:
        log.debug('GeoIP-City {} is up to date'.format(
            city_version
        ))

    # Country
    r = requests.head(path + country)
    # 'GeoLite2-City_20170905.tar.gz'
    filename = r.headers['content-disposition'].split('=')[1]
    # '20170905'
    new_country_version = filename.split('_')[1][:-7]

    if new_country_version > country_version or country_version == '':
        log.debug('Downloading {} version of GeoIP-Country...'.format(
            new_country_version
        ))
        r = requests.get(path + country, stream=True)
        if r.status_code == 200:
            with open(os.path.join(out_dir, country), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
        versions['country'] = new_country_version
    else:
        log.debug('GeoIP-Country {} is up to date'.format(
            country_version
        ))

    # Update versions
    with open(versions_file, 'w') as outfile:
        json.dump(versions, outfile)


@shared_task
def extract_geoip_databases():
    versions = json.load(open(versions_file, 'r'))
    city_version = versions.get('city', '')
    country_version = versions.get('country', '')

    dirs = (
        'GeoLite2-Country_'+country_version,
        'GeoLite2-City_'+city_version,
    )

    # GeoLite2-Country_20170905
    for d in dirs:
        if os.path.isdir(os.path.join(out_dir, d)):
            log.debug('Already extracted {}'.format(d))
        else:
            archive = os.path.join(out_dir, d.split('_')[0])+'.tar.gz'
            log.debug('Extracting {}...'.format(archive))
            import tarfile
            tar = tarfile.open(archive, "r:gz")
            tar.extractall(out_dir)
            tar.close()

        # update links
        target = d
        link_name = os.path.join(
            out_dir,
            d.split('_')[0].split('-')[1].lower()
        )
        try:
            os.symlink(target, link_name)
        except OSError as e:
            os.remove(link_name)
            os.symlink(target, link_name)


@shared_task
def update_geoip_databases():
    """Full update of GeoIP database.

    https://dev.maxmind.com/geoip/geoip2/geolite2/

    1. Download City and Country databases
    2. Extract
    3. Update Nginx config
    4. Reload Nginx

    """
    download_geoip_databases()
    extract_geoip_databases()
