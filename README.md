# folio_uuid
A python module for creating deterministic UUIDs (UUID v5) outside of FOLIO when migrating data.

# Installation
The module is uploaded to pypi. Just do    

	pip install folio-uuid
	
or   

	pipenv install folio-uuid      

# Overview
The UUIDs (v5) are contstructed in the following way:
* The namespace is the same for all "Folio UUIDs": **8405ae4d-b315-42e1-918a-d1919900cf3f**
* The name is contstructed by the following parts, delimited by a colon (**:**)
	* **OKAPI_URL** This should be the full OKAPI Url including https. **Example:** *https://okapi-bugfest-juniper.folio.ebsco.com*
	* **OBJECT_TYPE_NAME** This should be the name of the type of object that the ID is generated for. In plural. the *file folio_namespaces.py* in this repo has a complete list of the ones currently in use. **Example:** *items*
	* **LEGACY_IDENTIFIER** This should be the legacy identifier comming from the source system. The library will perform some normalization* of the identifier if it is a Sierra/Millennium identifier. **Example:** *i3696836*

\* The normalization strips away any dots (.), check digits and campus codes from the identifiers

# Tests/Examples
* The namespace is *8405ae4d-b315-42e1-918a-d1919900cf3f*
* The name, constructed as *OKAPI_URL:OBJECT_TYPE_NAME:LEGACY_IDENTIFIER* would become  *https://okapi-bugfest-juniper.folio.ebsco.com:items:i3696836*
* The resulting UUID then becomes *9647225d-d8e9-530d-b8cc-52a53be14e26*

# Bash/linux example
![image](https://user-images.githubusercontent.com/1894384/141293255-a692c61f-4b80-4748-8187-b8bdabe9befa.png)

	uuidgen --sha1 -n 8405ae4d-b315-42e1-918a-d1919900cf3f -N https://okapi-bugfest-juniper.folio.ebsco.com:items:i3696836
To install uuidgen on a apt-enabled Linux distribution, use   

	sudo apt-get install uuid-runtime

# Python Example
	def test_deterministic_uuid_generation_holdings():
	    deterministic_uuid = FolioUUID(
		"https://okapi-bugfest-juniper.folio.ebsco.com",
		FOLIONamespaces.holdings,
		"000000167",
	    )
	    assert "a0b4c8a2-01fd-50fd-8158-81bd551412a0" == str(deterministic_uuid)
	    
	    
# References
Wikipedia has an [article on UUID version 5](https://en.wikipedia.org/wiki/Universally_unique_identifier#Versions_3_and_5_(namespace_name-based))

There are many browser-based tools to create singe UUIDs v5. [UUIDTools](https://www.uuidtools.com/v5) is one of them.
