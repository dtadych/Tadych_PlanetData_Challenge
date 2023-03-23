# -*- coding: utf-8 -*-
'''
Created on Mon Feb 27 17:50:55 2023

@author: Dani
'''
import time
import requests
import numpy as np
from requests.auth import HTTPBasicAuth

# This class just contains scripts to build a lists of MOSAICS
class PlanetDataReader():

    @staticmethod
    # Takes a URL and optional API_KEY, and returns a json object
    def open_planet_data_url(url, API_KEY = None):
        if API_KEY is not None:
            auth = HTTPBasicAuth(API_KEY, '')
            res = requests.get(url=url, auth=auth)
        else:
            res = requests.get(url=url)
        if res.status_code != 200:
            print(url)
            raise requests.exceptions.HTTPError("Bad HTTP request %s"%res.status_code)
        json_dict = res.json()
        return json_dict
    
    @staticmethod
    def download_quad(quad_url):
        res = requests.get(url=quad_url)
        if res.status_code != 200:
            raise requests.exceptions.HTTPError("Bad HTTP request %s"%res.status_code)
        return res
    
    @staticmethod
    # The URL needs to be in the form: https://api.planet.com/basemaps/v1/mosaics
    # API_KEY: must be a valid Planet Data API_KEY. See your key at https://www.planet.com/account/#/user-settings
    def create_mosaics_list(url, API_KEY ,quad_page_size):
        mosaics_list = [] # This list is what we will return

        mosaics_json_dict = PlanetDataReader.open_planet_data_url(url, API_KEY)
        links_dict = mosaics_json_dict["_links"]
        mosaics_dict = mosaics_json_dict["mosaics"]

        mosaics_list.extend(PlanetDataReader.__from_mosaics_dict_to_list(mosaics_dict, quad_page_size))
        
        while "_next" in links_dict: # If so, a sub-sequent request needs to be made
            new_url = links_dict["_next"]
            mosaics_json_dict = PlanetDataReader.open_planet_data_url(new_url)
            links_dict = mosaics_json_dict["_links"]
            mosaics_dict = mosaics_json_dict["mosaics"]
            mosaics_list.extend(PlanetDataReader.__from_mosaics_dict_to_list(mosaics_dict, quad_page_size))

        return mosaics_list 
    
    @staticmethod
    # This method transforms a mosaic_dict (received from a mosaic request) into a list of mosaics
    def __from_mosaics_dict_to_list(mosaics_dict, quad_page_size):
        mosaics_list = []
        for mosaic_element_dict in mosaics_dict:
            links_dict = mosaic_element_dict["_links"]
            bbox = mosaic_element_dict["bbox"]
            coord_system = mosaic_element_dict["coordinate_system"]
            datatype = mosaic_element_dict["datatype"]
            first_acquired = mosaic_element_dict["first_acquired"]
            grid_dict = mosaic_element_dict["grid"]
            moisaic_id = mosaic_element_dict["id"]
            interval = mosaic_element_dict["interval"]
            item_types = mosaic_element_dict["item_types"]
            last_acquired = mosaic_element_dict["last_acquired"]
            zoom_level = mosaic_element_dict["level"]
            name = mosaic_element_dict["name"]
            product_type = mosaic_element_dict["product_type"]
            quad_download = mosaic_element_dict["quad_download"]
            new_mosaic = Mosaic(links_dict, bbox, coord_system, datatype, first_acquired, grid_dict, moisaic_id, interval, item_types, last_acquired, zoom_level, name, product_type, quad_download, quad_page_size)
            mosaics_list.append(new_mosaic)
        return mosaics_list

    @staticmethod
    # The URL needs to be in the form: https://api.planet.com/basemaps/v1/mosaics/{mosaic_name}/quads?api_key={your_key}&bbox={lx},{ly},{ux},{uy}
    def create_quads_list(url, mosaic_id, mosaic_name):
        quads_list = [] # This list is what we will return

        quads_json_dict = PlanetDataReader.open_planet_data_url(url)
        links_dict = quads_json_dict["_links"]
        quads_dict = quads_json_dict["items"]

        quads_list.extend(PlanetDataReader.__from_quads_dict_to_list(quads_dict, mosaic_id, mosaic_name))
        i = 1
        
        while "_next" in links_dict: # If so, a sub-sequent request needs to be made
            new_url = links_dict["_next"]
            quads_json_dict = PlanetDataReader.open_planet_data_url(new_url)
            links_dict = quads_json_dict["_links"]
            quads_dict = quads_json_dict["items"]
            quads_list.extend(PlanetDataReader.__from_quads_dict_to_list(quads_dict, mosaic_id, mosaic_name))
            i += 1
            if np.mod(i, 10) == 0: print(len(quads_list))
        
        return quads_list 

    @staticmethod
    # This method transforms a quad_dict (received from a quad request) into a list of quads
    def __from_quads_dict_to_list(quads_dict, mosaic_id ,mosaic_name):
        quads_list = []
        for quad_element_dict in quads_dict:
            links_dict = quad_element_dict["_links"]
            bbox = quad_element_dict["bbox"]
            quad_id = quad_element_dict["id"]
            percent_covered = quad_element_dict["percent_covered"]
            new_quad = Quad(links_dict, bbox, quad_id, percent_covered, mosaic_id, mosaic_name)
            quads_list.append(new_quad)
        return quads_list

# This class contains the information of all the links to download all mosaics in Planet Data
class Mosaic(object):
    def __init__(self, links_dict, bbox, coord_system, datatype, first_acquired, grid_dict, moisaic_id, interval, item_types, last_acquired, zoom_level, name, product_type, quad_download, quad_page_size):
        if "_self" in links_dict:
            self.self_link = links_dict["_self"]                    # Link to access current mosaic
        if "quads" in links_dict:
            self.quad_list_link =  links_dict["quads"]+"&_page_size=%s"%quad_page_size # Link to access a list of all Quads in the mosaic
        if "tiles" in links_dict:
            self.png_tiles_template_link = links_dict["tiles"]      # Link with a template to access PNGs, looking like: https://tiles.planet.com/basemaps/v1/planet-tiles/{mosaic_name}/gmap/{zoom}/{x}/{y}.png?api_key={YOUR_API_KEY}
        self.bbox = bbox
        self.coord_system = coord_system
        self.datatype = datatype
        self.first_acquired = first_acquired
        self.grid_dict = grid_dict
        self.id = moisaic_id
        self.interval = interval
        self.item_types = item_types
        self.last_acquired = last_acquired
        self.zoom_level = zoom_level
        self.name = name
        self.product_type = product_type
        self.quad_download = quad_download

    def __str__(self):
        return "Mosaic '%s' with zoom [%s] and name \"%s\""%(self.id, self.zoom_level, self.name)
    
    def __repr__(self):
        return str(self)
    
class Quad(object):
    def __init__(self, links_dict, bbox, quad_id, percent_covered, mosaic_id, mosaic_name):
        if "_self" in links_dict:
            self.self_link = links_dict["_self"]                    # Link to access current quad
        if "download" in links_dict:
            self.download_link = links_dict["download"]             # Link to download current quad in TIFF
        if "items" in links_dict:
            self.items_link = links_dict["items"]                   # TODO: I havent been able to figure out what these Items are
        if "thumbnail" in links_dict:
            self.thumbnail_link = links_dict["thumbnail"]           # Link to download a PNG thumbnail of the TIFF
        self.bbox = bbox
        self.id = quad_id
        self.percent_covered = percent_covered                      # Percent of the area with non-null values
        self.mosaic_id = mosaic_id                                  # Parent Mosaic ID
        self.mosaic_name = mosaic_name                              # Parent Mosaic Name
    
    def __str__(self):
        return "Quad '%s' with cover of [%s]"%(self.id, self.percent_covered)
    
    def __repr__(self):
        return str(self)