# folio_uuid
A python module for creating deterministic UUIDs (UUID v5) outside of FOLIO when migrating data.

# Installation
The module is uploaded to pypi. Just do    

```shell
pip install folio-uuid
```	
or   

```shell
pipenv install folio-uuid      
```

# Overview
The UUIDs (v5) are contstructed in the following way:
* The namespace is the same for all "Folio UUIDs": **8405ae4d-b315-42e1-918a-d1919900cf3f**
* The name is contstructed by the following parts, delimited by a colon (**:**)
	* **TENANT_STRING** This should be a unique, system-specific string for the target system. We recommend using the target Tenant ID (the value passed in `x-okapi-tenant` when accessing FOLIO's APIs), but you can use the system's API gateway URL, as well. **Example:** *diku*
	* **OBJECT_TYPE_NAME** This should be the name of the type of object that the ID is generated for. In plural. the *file folio_namespaces.py* in this repo has a complete list of the ones currently in use. **Example:** *items*
	* **LEGACY_IDENTIFIER** This should be the legacy identifier comming from the source system. The library will perform some normalization* of the identifier if it is a Sierra/Millennium identifier. **Example:** *i3696836*

\* The normalization strips away any dots (.), check digits and campus codes from the identifiers

# Tests/Examples
* The namespace is `*8405ae4d-b315-42e1-918a-d1919900cf3f*`
* The name, constructed as `TENANT_ID:OBJECT_TYPE_NAME:LEGACY_IDENTIFIER` would become  `diku:items:i3696836`
* The resulting UUID then becomes `9647225d-d8e9-530d-b8cc-52a53be14e26`

# Bash/linux example

```shell
uuidgen --sha1 -n 8405ae4d-b315-42e1-918a-d1919900cf3f -N diku:items:i3696836
```
To install uuidgen on a apt-enabled Linux distribution, use   

```shell
sudo apt-get install uuid-runtime
```

# Python Example
```python
def test_deterministic_uuid_generation_holdings():
   deterministic_uuid = FolioUUID(
      "diku",
      FOLIONamespaces.holdings,
      "000000167",
   )
assert "3db53ecc-37a9-521e-88fd-6ef72c710468" == str(deterministic_uuid)
```

# What happened to OKAPI_URL?
Previous versions of this library directed users to provide the target FOLIO system's OKAPI URL as the first argument (`okapi_url`) when instantiating a new `FolioUUID` class, and allowed specifying an optional `tenant_id` value that would be included in the overall string used to generate the v5 UUID. However, in most circumstances the FOLIO tenant id value is more static than the API gateway URL (eg. when migrating from an OKAPI-based FOLIO system to a Eureka-based one).

As of v1.0.0 of `folio_uuid`, the first argument has been renamed to `tenant_string`, and can be any unique string value for the target tenant. `okapi_url` and `tenant_id` are still available as keyword-only arguments, but are deprecated and will be removed in a future release. Code that used `FolioUUID` with positional-only arguments will not require any code changes. Code that used keyword arguments for `okapi_url` and `tenant_id` will continue to work, as well, but will raise deprecation warnings.


# References
Wikipedia has an [article on UUID version 5](https://en.wikipedia.org/wiki/Universally_unique_identifier#Versions_3_and_5_(namespace_name-based))

There are many browser-based tools to create singe UUIDs v5. [UUIDTools](https://www.uuidtools.com/v5) is one of them.
